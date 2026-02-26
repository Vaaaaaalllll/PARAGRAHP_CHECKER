# WARNING: template code, may need edits
#!/usr/bin/env python3
"""Main CLI entry point for Paragraph Checker."""

import click
import sys
from pathlib import Path
from src.checker import ParagraphChecker
from src.display import ResultDisplay


@click.command()
@click.option(
    "--input",
    "-i",
    "text_input",
    help="Text to analyze (enclose in quotes)",
    type=str,
)
@click.option(
    "--file",
    "-f",
    "file_path",
    help="Path to text file to analyze",
    type=click.Path(exists=True),
)
@click.option(
    "--output",
    "-o",
    help="Output file path for results (optional)",
    type=click.Path(),
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Show detailed explanations",
)
def main(text_input, file_path, output, verbose):
    """Analyze text for grammar, spelling, and style issues."""
    
    # Validate input
    if not text_input and not file_path:
        click.echo("Error: Please provide either --input or --file")
        click.echo("Example: python src/main.py --input 'Your text here'")
        sys.exit(1)
    
    # Get text content
    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
            click.echo(f"Analyzing file: {file_path}\n")
        except Exception as e:
            click.echo(f"Error reading file: {e}")
            sys.exit(1)
    else:
        text = text_input
    
    # Initialize checker
    try:
        click.echo("Initializing Paragraph Checker...")
        checker = ParagraphChecker()
        click.echo("Analysis in progress...\n")
        
        # Analyze text
        results = checker.analyze(text)
        
        # Display results
        display = ResultDisplay(verbose=verbose)
        display.show_results(results, text)
        
        # Save to file if requested
        if output:
            display.save_to_file(results, text, output)
            click.echo(f"\nResults saved to: {output}")
        
    except Exception as e:
        click.echo(f"Error during analysis: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

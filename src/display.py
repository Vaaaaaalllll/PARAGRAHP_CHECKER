# WARNING: template code, may need edits
"""Display and formatting utilities for analysis results."""

from typing import Dict, Any, List
from colorama import Fore, Style, init
from src.models.issue import Issue, Severity
import json

# Initialize colorama
init(autoreset=True)


class ResultDisplay:
    """Handles displaying analysis results to the user."""
    
    def __init__(self, verbose: bool = False):
        """Initialize the display handler.
        
        Args:
            verbose: Whether to show detailed explanations
        """
        self.verbose = verbose
        
        # Color mapping for severity
        self.severity_colors = {
            Severity.ERROR: Fore.RED,
            Severity.WARNING: Fore.YELLOW,
            Severity.SUGGESTION: Fore.CYAN
        }
    
    def show_results(self, results: Dict[str, Any], text: str):
        """Display analysis results to console.
        
        Args:
            results: Analysis results dictionary
            text: Original text
        """
        print("\n" + "="*80)
        print(f"{Fore.GREEN}PARAGRAPH ANALYSIS RESULTS{Style.RESET_ALL}")
        print("="*80 + "\n")
        
        # Show statistics
        self._show_statistics(results.get('statistics', {}))
        
        # Show summary
        self._show_summary(results.get('summary', {}))
        
        # Show issues
        issues = results.get('issues', [])
        if issues:
            print(f"\n{Fore.YELLOW}ISSUES FOUND:{Style.RESET_ALL}\n")
            self._show_issues(issues)
        else:
            print(f"\n{Fore.GREEN}✓ No issues found! Great job!{Style.RESET_ALL}\n")
    
    def _show_statistics(self, stats: Dict[str, Any]):
        """Display text statistics."""
        if not stats:
            return
        
        print(f"{Fore.CYAN}TEXT STATISTICS:{Style.RESET_ALL}")
        print(f"  Words: {stats.get('word_count', 0)}")
        print(f"  Sentences: {stats.get('sentence_count', 0)}")
        print(f"  Average sentence length: {stats.get('avg_sentence_length', 0)} words")
        print(f"  Reading level: {stats.get('reading_level', 'N/A')}")
        print(f"  Readability: {stats.get('readability_interpretation', 'N/A')}")
        print()
    
    def _show_summary(self, summary: Dict[str, Any]):
        """Display issue summary."""
        total = summary.get('total_issues', 0)
        
        print(f"{Fore.CYAN}SUMMARY:{Style.RESET_ALL}")
        print(f"  Total issues found: {total}")
        
        if total > 0:
            by_type = summary.get('by_type', {})
            if by_type:
                print("\n  Issues by type:")
                for issue_type, count in by_type.items():
                    print(f"    - {issue_type}: {count}")
            
            by_severity = summary.get('by_severity', {})
            if by_severity:
                print("\n  Issues by severity:")
                for severity, count in by_severity.items():
                    color = self._get_severity_color_by_name(severity)
                    print(f"    {color}- {severity}: {count}{Style.RESET_ALL}")
    
    def _show_issues(self, issues: List[Issue]):
        """Display individual issues."""
        for i, issue in enumerate(issues, 1):
            color = self.severity_colors.get(issue.severity, Fore.WHITE)
            
            print(f"{color}{'─'*80}{Style.RESET_ALL}")
            print(f"{color}Issue #{i} - {issue.severity.value} - {issue.issue_type.value}{Style.RESET_ALL}")
            print(f"{color}{'─'*80}{Style.RESET_ALL}\n")
            
            print(f"  {Fore.WHITE}Problem:{Style.RESET_ALL} {issue.message}")
            print(f"  {Fore.WHITE}Context:{Style.RESET_ALL} {issue.context}")
            
            if self.verbose:
                print(f"\n  {Fore.WHITE}Explanation:{Style.RESET_ALL}")
                print(f"    {issue.explanation}")
                
                print(f"\n  {Fore.GREEN}💡 Learning Tip:{Style.RESET_ALL}")
                for line in issue.learning_tip.split('\n'):
                    print(f"    {line}")
            
            if issue.suggested_fix:
                print(f"\n  {Fore.WHITE}Suggestion:{Style.RESET_ALL} {issue.suggested_fix}")
            
            print()
    
    def _get_severity_color_by_name(self, severity_name: str) -> str:
        """Get color by severity name."""
        if severity_name == 'Error':
            return Fore.RED
        elif severity_name == 'Warning':
            return Fore.YELLOW
        else:
            return Fore.CYAN
    
    def save_to_file(self, results: Dict[str, Any], text: str, filepath: str):
        """Save results to a file.
        
        Args:
            results: Analysis results
            text: Original text
            filepath: Output file path
        """
        output_data = {
            'original_text': text,
            'statistics': results.get('statistics', {}),
            'summary': results.get('summary', {}),
            'issues': [issue.to_dict() for issue in results.get('issues', [])]
        }
        
        # Determine format by extension
        if filepath.endswith('.json'):
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
        else:
            # Plain text format
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("PARAGRAPH ANALYSIS RESULTS\n")
                f.write("="*80 + "\n\n")
                
                f.write("ORIGINAL TEXT:\n")
                f.write(text + "\n\n")
                
                f.write("STATISTICS:\n")
                for key, value in output_data['statistics'].items():
                    f.write(f"  {key}: {value}\n")
                
                f.write("\nISSUES:\n")
                for i, issue in enumerate(output_data['issues'], 1):
                    f.write(f"\nIssue #{i}:\n")
                    for key, value in issue.items():
                        f.write(f"  {key}: {value}\n")

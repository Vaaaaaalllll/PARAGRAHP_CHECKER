# WARNING: template code, may need edits
# Paragraph Checker

A simple grammar and writing analysis tool that helps you learn by identifying issues in your writing without automatically fixing them.

## Features

- Grammar error detection
- Spelling mistakes identification
- Punctuation issues
- Style suggestions
- Readability analysis
- Educational feedback to help you learn

## Installation

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## Usage

### Command Line

```bash
python src/main.py --input "Your paragraph here"
```

Or from a file:

```bash
python src/main.py --file path/to/essay.txt
```

### As a Module

```python
from src.checker import ParagraphChecker

checker = ParagraphChecker()
results = checker.analyze("Your paragraph here.")
checker.display_results(results)
```

## Output Format

The tool provides:
- **Issue Type**: Grammar, Spelling, Punctuation, Style
- **Location**: Position in text
- **Problem**: What's wrong
- **Explanation**: Why it's an issue
- **Learning Tip**: How to fix it yourself

## Project Structure

```
paragraph_checker/
├── src/              # Source code
├── tests/            # Unit tests
├── examples/         # Example texts
└── docs/             # Documentation
```

## License

MIT License

# WARNING: template code, may need edits
# Paragraph Checker - Usage Guide

## Basic Usage

### Command Line Interface

#### Analyze text directly:
```bash
python src/main.py --input "Your text here"
```

#### Analyze a file:
```bash
python src/main.py --file examples/sample_essay.txt
```

#### Save results to a file:
```bash
python src/main.py --file essay.txt --output results.txt
```

#### Verbose mode (detailed explanations):
```bash
python src/main.py --file essay.txt --verbose
```

### Python API

```python
from src.checker import ParagraphChecker

# Initialize checker
checker = ParagraphChecker()

# Analyze text
text = "Your paragraph here."
results = checker.analyze(text)

# Access results
print(f"Total issues: {results['summary']['total_issues']}")

for issue in results['issues']:
    print(f"- {issue.message}")
    print(f"  Tip: {issue.learning_tip}")
```

## Understanding Results

### Issue Types

1. **Grammar**: Grammatical errors (subject-verb agreement, tense, etc.)
2. **Spelling**: Misspelled words
3. **Punctuation**: Punctuation errors
4. **Style**: Style improvements (passive voice, weak words)
5. **Clarity**: Clarity issues (long sentences, wordy phrases)
6. **Word Choice**: Word choice suggestions

### Severity Levels

- **Error** (Red): Definite mistakes that should be fixed
- **Warning** (Yellow): Likely issues that need attention
- **Suggestion** (Cyan): Optional improvements for better writing

### Statistics

The tool provides:
- Word count
- Sentence count
- Average sentence length
- Reading level (Flesch-Kincaid grade)
- Readability score

## Learning Tips

Each issue includes:

1. **Problem**: What's wrong
2. **Context**: Where it appears in your text
3. **Explanation**: Why it's an issue
4. **Learning Tip**: How to fix it yourself
5. **Suggestion**: Possible corrections (for reference)

## Best Practices

1. **Review all issues**: Don't just fix errors; understand them
2. **Read learning tips**: They help you avoid similar mistakes
3. **Check context**: Make sure suggestions fit your intent
4. **Consider suggestions**: Not all suggestions must be followed
5. **Rerun after fixes**: Verify your corrections

## Examples

### Example 1: Grammar Error

**Input**: "She don't like apples."

**Output**:
- Issue: Grammar error
- Problem: Subject-verb agreement
- Tip: Use "doesn't" with third-person singular subjects
- Suggestion: "She doesn't like apples."

### Example 2: Style Improvement

**Input**: "The ball was thrown by John."

**Output**:
- Issue: Passive voice
- Problem: Less direct writing
- Tip: Make the actor (John) the subject
- Suggestion: "John threw the ball."

### Example 3: Clarity Issue

**Input**: "In order to succeed, you must try."

**Output**:
- Issue: Wordy phrase
- Problem: "In order to" is unnecessarily wordy
- Tip: Use simpler alternatives
- Suggestion: "To succeed, you must try."

## Output Formats

### Console Output
Colorized, easy-to-read format with issue details

### Text File
Plain text format with all information

### JSON File
Structured data for programmatic use:
```bash
python src/main.py --file essay.txt --output results.json
```

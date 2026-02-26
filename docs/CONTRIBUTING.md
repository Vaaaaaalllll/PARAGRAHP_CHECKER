# WARNING: template code, may need edits
# Contributing to Paragraph Checker

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/paragraph_checker.git
   cd paragraph_checker
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

## Development Workflow

1. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes

3. Run tests:
   ```bash
   pytest tests/
   ```

4. Commit your changes:
   ```bash
   git add .
   git commit -m "Description of changes"
   ```

5. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

6. Create a Pull Request

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and single-purpose
- Maximum line length: 88 characters (Black formatter)

## Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for good test coverage
- Test edge cases

## Adding New Analyzers

1. Create a new file in `src/analyzers/`
2. Implement the analyzer class
3. Add tests in `tests/test_analyzers.py`
4. Update `src/analyzers/__init__.py`
5. Integrate into `src/checker.py`

## Adding New Issue Types

1. Add to `IssueType` enum in `src/models/issue.py`
2. Update display colors in `src/display.py` if needed
3. Document in `docs/USAGE.md`

## Documentation

- Update README.md for user-facing changes
- Update USAGE.md for new features
- Add docstrings to new code
- Include examples where helpful

## Pull Request Guidelines

- Provide clear description of changes
- Reference related issues
- Include tests
- Update documentation
- Keep PRs focused and atomic

## Code Review Process

1. Automated tests must pass
2. Code review by maintainer
3. Address feedback
4. Approval and merge

## Questions?

Open an issue for:
- Bug reports
- Feature requests
- Questions about contributing

Thank you for contributing!

# WARNING: template code, may need edits
"""Spelling analysis using pyspellchecker."""

from spellchecker import SpellChecker
from typing import List
import re
from src.models.issue import Issue, IssueType, Severity


class SpellingAnalyzer:
    """Analyzes text for spelling errors."""
    
    def __init__(self):
        """Initialize the spelling analyzer."""
        self.spell = SpellChecker()
    
    def analyze(self, text: str, doc=None) -> List[Issue]:
        """Analyze text for spelling issues.
        
        Args:
            text: The text to analyze
            doc: Optional spaCy doc object for better tokenization
            
        Returns:
            List of spelling-related issues
        """
        issues = []
        
        # Use spaCy tokens if available, otherwise split by words
        if doc:
            words = [(token.text, token.idx) for token in doc if token.is_alpha]
        else:
            words = [(m.group(), m.start()) for m in re.finditer(r'\b[a-zA-Z]+\b', text)]
        
        for word, position in words:
            # Skip very short words and proper nouns (capitalized)
            if len(word) <= 2:
                continue
            
            word_lower = word.lower()
            
            # Check if misspelled
            if word_lower not in self.spell:
                # Get suggestions
                suggestions = self.spell.candidates(word_lower)
                
                if suggestions:
                    suggestion_list = list(suggestions)[:3]  # Top 3 suggestions
                    
                    issue = Issue(
                        issue_type=IssueType.SPELLING,
                        severity=Severity.ERROR,
                        position=position,
                        length=len(word),
                        message=f"Possible spelling error: '{word}'",
                        explanation=f"The word '{word}' may be misspelled. Did you mean one of these?",
                        learning_tip=self._create_spelling_tip(word, suggestion_list),
                        context=self._get_context(text, position, len(word)),
                        suggested_fix=", ".join(suggestion_list)
                    )
                    
                    issues.append(issue)
        
        return issues
    
    def _get_context(self, text: str, offset: int, length: int, window: int = 30) -> str:
        """Extract context around the error."""
        start = max(0, offset - window)
        end = min(len(text), offset + length + window)
        
        context = text[start:end]
        error_start = offset - start
        error_end = error_start + length
        
        highlighted = (
            context[:error_start] + 
            ">>>" + context[error_start:error_end] + "<<<" + 
            context[error_end:]
        )
        
        return highlighted.strip()
    
    def _create_spelling_tip(self, word: str, suggestions: List[str]) -> str:
        """Create an educational tip for spelling."""
        base_tip = "When unsure about spelling, try these strategies:\n"
        base_tip += "1. Break the word into syllables and sound it out\n"
        base_tip += "2. Look for common prefixes and suffixes\n"
        base_tip += "3. Remember similar words you know how to spell\n"
        
        if suggestions:
            base_tip += f"\nFor '{word}', consider: {', '.join(suggestions)}"
        
        return base_tip

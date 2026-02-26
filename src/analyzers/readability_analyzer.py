# WARNING: template code, may need edits
"""Readability and text statistics analysis."""

import textstat
from typing import Dict, Any


class ReadabilityAnalyzer:
    """Analyzes text readability and provides statistics."""
    
    def analyze(self, text: str) -> Dict[str, Any]:
        """Calculate readability metrics.
        
        Args:
            text: The text to analyze
            
        Returns:
            Dictionary of readability statistics
        """
        if not text or not text.strip():
            return {}
        
        stats = {
            'word_count': textstat.lexicon_count(text, removepunct=True),
            'sentence_count': textstat.sentence_count(text),
            'character_count': len(text),
            'syllable_count': textstat.syllable_count(text),
            'avg_sentence_length': self._safe_divide(
                textstat.lexicon_count(text, removepunct=True),
                textstat.sentence_count(text)
            ),
            'flesch_reading_ease': textstat.flesch_reading_ease(text),
            'flesch_kincaid_grade': textstat.flesch_kincaid_grade(text),
            'difficult_words': textstat.difficult_words(text),
        }
        
        # Add interpretation
        stats['reading_level'] = self._interpret_reading_level(
            stats['flesch_kincaid_grade']
        )
        stats['readability_interpretation'] = self._interpret_flesch_score(
            stats['flesch_reading_ease']
        )
        
        return stats
    
    def _safe_divide(self, numerator: float, denominator: float) -> float:
        """Safely divide two numbers."""
        if denominator == 0:
            return 0.0
        return round(numerator / denominator, 2)
    
    def _interpret_reading_level(self, grade: float) -> str:
        """Interpret Flesch-Kincaid grade level."""
        if grade < 6:
            return "Elementary school level"
        elif grade < 9:
            return "Middle school level"
        elif grade < 13:
            return "High school level"
        elif grade < 16:
            return "College level"
        else:
            return "Graduate school level"
    
    def _interpret_flesch_score(self, score: float) -> str:
        """Interpret Flesch Reading Ease score."""
        if score >= 90:
            return "Very easy to read (5th grade level)"
        elif score >= 80:
            return "Easy to read (6th grade level)"
        elif score >= 70:
            return "Fairly easy to read (7th grade level)"
        elif score >= 60:
            return "Standard/Average (8th-9th grade level)"
        elif score >= 50:
            return "Fairly difficult to read (10th-12th grade level)"
        elif score >= 30:
            return "Difficult to read (College level)"
        else:
            return "Very difficult to read (Graduate level)"

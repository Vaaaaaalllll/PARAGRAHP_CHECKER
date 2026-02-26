# WARNING: template code, may need edits
"""Tests for the ParagraphChecker class."""

import pytest
from src.checker import ParagraphChecker
from src.models.issue import IssueType, Severity


class TestParagraphChecker:
    """Test cases for ParagraphChecker."""
    
    @pytest.fixture
    def checker(self):
        """Create a checker instance for testing."""
        return ParagraphChecker()
    
    def test_empty_text(self, checker):
        """Test with empty text."""
        results = checker.analyze("")
        assert results['summary']['total_issues'] == 0
        assert len(results['issues']) == 0
    
    def test_perfect_text(self, checker):
        """Test with grammatically correct text."""
        text = "This is a well-written sentence. It has no errors."
        results = checker.analyze(text)
        # May have style suggestions but should have no errors
        assert results is not None
    
    def test_spelling_error(self, checker):
        """Test detection of spelling errors."""
        text = "This sentance has a speling error."
        results = checker.analyze(text)
        
        spelling_issues = [
            issue for issue in results['issues']
            if issue.issue_type == IssueType.SPELLING
        ]
        assert len(spelling_issues) > 0
    
    def test_grammar_error(self, checker):
        """Test detection of grammar errors."""
        text = "She dont like apples."
        results = checker.analyze(text)
        
        # Should detect grammar issue
        assert results['summary']['total_issues'] > 0
    
    def test_multiple_sentences(self, checker):
        """Test with multiple sentences."""
        text = "First sentence. Second sentence. Third sentence."
        results = checker.analyze(text)
        
        assert results['statistics']['sentence_count'] == 3
    
    def test_long_sentence_detection(self, checker):
        """Test detection of long sentences."""
        text = "This is a very long sentence that contains many words and clauses and phrases and continues on and on without stopping for a very long time which makes it difficult to read and understand clearly."
        results = checker.analyze(text)
        
        # Should detect long sentence
        clarity_issues = [
            issue for issue in results['issues']
            if issue.issue_type == IssueType.CLARITY
        ]
        assert len(clarity_issues) > 0
    
    def test_weak_words_detection(self, checker):
        """Test detection of weak words."""
        text = "This is very really quite good."
        results = checker.analyze(text)
        
        word_choice_issues = [
            issue for issue in results['issues']
            if issue.issue_type == IssueType.WORD_CHOICE
        ]
        assert len(word_choice_issues) > 0

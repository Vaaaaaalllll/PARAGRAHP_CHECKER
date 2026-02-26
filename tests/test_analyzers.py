# WARNING: template code, may need edits
"""Tests for analyzer modules."""

import pytest
import spacy
from src.analyzers.spelling_analyzer import SpellingAnalyzer
from src.analyzers.style_analyzer import StyleAnalyzer
from src.analyzers.readability_analyzer import ReadabilityAnalyzer
from src.models.issue import IssueType


class TestSpellingAnalyzer:
    """Test cases for SpellingAnalyzer."""
    
    @pytest.fixture
    def analyzer(self):
        return SpellingAnalyzer()
    
    def test_correct_spelling(self, analyzer):
        """Test with correctly spelled text."""
        text = "The quick brown fox jumps."
        issues = analyzer.analyze(text)
        assert len(issues) == 0
    
    def test_misspelled_word(self, analyzer):
        """Test with misspelled word."""
        text = "The quik brown fox."
        issues = analyzer.analyze(text)
        assert len(issues) > 0
        assert any('quik' in issue.message.lower() for issue in issues)


class TestStyleAnalyzer:
    """Test cases for StyleAnalyzer."""
    
    @pytest.fixture
    def analyzer(self):
        nlp = spacy.load("en_core_web_sm")
        return StyleAnalyzer(nlp)
    
    @pytest.fixture
    def nlp(self):
        return spacy.load("en_core_web_sm")
    
    def test_weak_word_detection(self, analyzer, nlp):
        """Test detection of weak words."""
        text = "This is very good."
        doc = nlp(text)
        issues = analyzer.analyze(text, doc)
        
        weak_word_issues = [
            issue for issue in issues
            if issue.issue_type == IssueType.WORD_CHOICE
        ]
        assert len(weak_word_issues) > 0
    
    def test_wordy_phrase_detection(self, analyzer, nlp):
        """Test detection of wordy phrases."""
        text = "In order to succeed, you must try."
        doc = nlp(text)
        issues = analyzer.analyze(text, doc)
        
        clarity_issues = [
            issue for issue in issues
            if issue.issue_type == IssueType.CLARITY
        ]
        assert len(clarity_issues) > 0
    
    def test_long_sentence_detection(self, analyzer, nlp):
        """Test detection of long sentences."""
        text = "This is a very long sentence with many words that continues on and on and on and on and on and on and on and on and on making it difficult to read."
        doc = nlp(text)
        issues = analyzer.analyze(text, doc)
        
        long_sentence_issues = [
            issue for issue in issues
            if 'Long sentence' in issue.message
        ]
        assert len(long_sentence_issues) > 0


class TestReadabilityAnalyzer:
    """Test cases for ReadabilityAnalyzer."""
    
    @pytest.fixture
    def analyzer(self):
        return ReadabilityAnalyzer()
    
    def test_basic_statistics(self, analyzer):
        """Test basic text statistics."""
        text = "This is a test. It has two sentences."
        stats = analyzer.analyze(text)
        
        assert stats['sentence_count'] == 2
        assert stats['word_count'] > 0
        assert 'flesch_reading_ease' in stats
    
    def test_empty_text(self, analyzer):
        """Test with empty text."""
        stats = analyzer.analyze("")
        assert stats == {}
    
    def test_readability_interpretation(self, analyzer):
        """Test readability interpretation."""
        text = "The cat sat on the mat."
        stats = analyzer.analyze(text)
        
        assert 'reading_level' in stats
        assert 'readability_interpretation' in stats

# WARNING: template code, may need edits
"""Tests for data models."""

import pytest
from src.models.issue import Issue, IssueType, Severity


class TestIssue:
    """Test cases for Issue model."""
    
    def test_issue_creation(self):
        """Test creating an issue."""
        issue = Issue(
            issue_type=IssueType.GRAMMAR,
            severity=Severity.ERROR,
            position=0,
            length=5,
            message="Test message",
            explanation="Test explanation",
            learning_tip="Test tip",
            context="Test context"
        )
        
        assert issue.issue_type == IssueType.GRAMMAR
        assert issue.severity == Severity.ERROR
        assert issue.message == "Test message"
    
    def test_issue_to_dict(self):
        """Test converting issue to dictionary."""
        issue = Issue(
            issue_type=IssueType.SPELLING,
            severity=Severity.WARNING,
            position=10,
            length=4,
            message="Spelling error",
            explanation="Word misspelled",
            learning_tip="Check spelling",
            context="test context",
            suggested_fix="correct"
        )
        
        issue_dict = issue.to_dict()
        
        assert issue_dict['type'] == 'Spelling'
        assert issue_dict['severity'] == 'Warning'
        assert issue_dict['position'] == 10
        assert issue_dict['suggested_fix'] == 'correct'
    
    def test_issue_string_representation(self):
        """Test string representation of issue."""
        issue = Issue(
            issue_type=IssueType.STYLE,
            severity=Severity.SUGGESTION,
            position=0,
            length=5,
            message="Style issue",
            explanation="Explanation",
            learning_tip="Tip",
            context="Context"
        )
        
        issue_str = str(issue)
        assert 'Suggestion' in issue_str
        assert 'Style' in issue_str

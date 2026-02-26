# WARNING: template code, may need edits
"""Data models for representing issues found in text."""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class IssueType(Enum):
    """Types of issues that can be detected."""
    GRAMMAR = "Grammar"
    SPELLING = "Spelling"
    PUNCTUATION = "Punctuation"
    STYLE = "Style"
    CLARITY = "Clarity"
    WORD_CHOICE = "Word Choice"


class Severity(Enum):
    """Severity levels for issues."""
    ERROR = "Error"
    WARNING = "Warning"
    SUGGESTION = "Suggestion"


@dataclass
class Issue:
    """Represents a single issue found in the text."""
    
    issue_type: IssueType
    severity: Severity
    position: int
    length: int
    message: str
    explanation: str
    learning_tip: str
    context: str
    suggested_fix: Optional[str] = None
    
    def __str__(self) -> str:
        """String representation of the issue."""
        return f"[{self.severity.value}] {self.issue_type.value}: {self.message}"
    
    def to_dict(self) -> dict:
        """Convert issue to dictionary."""
        return {
            "type": self.issue_type.value,
            "severity": self.severity.value,
            "position": self.position,
            "length": self.length,
            "message": self.message,
            "explanation": self.explanation,
            "learning_tip": self.learning_tip,
            "context": self.context,
            "suggested_fix": self.suggested_fix
        }

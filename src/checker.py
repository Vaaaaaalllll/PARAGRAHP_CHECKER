# WARNING: template code, may need edits
"""Core paragraph checking and analysis functionality."""

import spacy
from typing import List, Dict, Any
from src.analyzers.grammar_analyzer import GrammarAnalyzer
from src.analyzers.spelling_analyzer import SpellingAnalyzer
from src.analyzers.style_analyzer import StyleAnalyzer
from src.analyzers.readability_analyzer import ReadabilityAnalyzer
from src.models.issue import Issue


class ParagraphChecker:
    """Main class for analyzing text and detecting issues."""
    
    def __init__(self):
        """Initialize the paragraph checker with all analyzers."""
        print("Loading language models...")
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Downloading required language model...")
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")
        
        self.grammar_analyzer = GrammarAnalyzer()
        self.spelling_analyzer = SpellingAnalyzer()
        self.style_analyzer = StyleAnalyzer(self.nlp)
        self.readability_analyzer = ReadabilityAnalyzer()
    
    def analyze(self, text: str) -> Dict[str, Any]:
        """Analyze text and return all detected issues.
        
        Args:
            text: The text to analyze
            
        Returns:
            Dictionary containing all issues and statistics
        """
        if not text or not text.strip():
            return {
                "issues": [],
                "statistics": {},
                "summary": {"total_issues": 0}
            }
        
        # Process text with spaCy
        doc = self.nlp(text)
        
        # Run all analyzers
        grammar_issues = self.grammar_analyzer.analyze(text)
        spelling_issues = self.spelling_analyzer.analyze(text, doc)
        style_issues = self.style_analyzer.analyze(text, doc)
        readability_stats = self.readability_analyzer.analyze(text)
        
        # Combine all issues
        all_issues = grammar_issues + spelling_issues + style_issues
        
        # Sort issues by position
        all_issues.sort(key=lambda x: x.position)
        
        # Create summary
        summary = self._create_summary(all_issues)
        
        return {
            "issues": all_issues,
            "statistics": readability_stats,
            "summary": summary,
            "text": text
        }
    
    def _create_summary(self, issues: List[Issue]) -> Dict[str, Any]:
        """Create a summary of all issues."""
        summary = {
            "total_issues": len(issues),
            "by_type": {},
            "by_severity": {}
        }
        
        for issue in issues:
            # Count by type
            issue_type = issue.issue_type
            summary["by_type"][issue_type] = summary["by_type"].get(issue_type, 0) + 1
            
            # Count by severity
            severity = issue.severity
            summary["by_severity"][severity] = summary["by_severity"].get(severity, 0) + 1
        
        return summary

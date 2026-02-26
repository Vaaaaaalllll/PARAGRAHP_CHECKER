# WARNING: template code, may need edits
"""Grammar and punctuation analysis using LanguageTool."""

import language_tool_python
from typing import List
from src.models.issue import Issue, IssueType, Severity


class GrammarAnalyzer:
    """Analyzes text for grammar and punctuation errors."""
    
    def __init__(self):
        """Initialize the grammar analyzer with LanguageTool."""
        self.tool = language_tool_python.LanguageTool('en-US')
    
    def analyze(self, text: str) -> List[Issue]:
        """Analyze text for grammar issues.
        
        Args:
            text: The text to analyze
            
        Returns:
            List of grammar-related issues
        """
        issues = []
        
        try:
            matches = self.tool.check(text)
            
            for match in matches:
                # Determine issue type
                issue_type = self._categorize_rule(match.ruleId, match.category)
                
                # Determine severity
                severity = self._determine_severity(match)
                
                # Extract context
                context = self._get_context(text, match.offset, match.errorLength)
                
                # Create learning tip
                learning_tip = self._create_learning_tip(match)
                
                issue = Issue(
                    issue_type=issue_type,
                    severity=severity,
                    position=match.offset,
                    length=match.errorLength,
                    message=match.message,
                    explanation=self._create_explanation(match),
                    learning_tip=learning_tip,
                    context=context,
                    suggested_fix=match.replacements[0] if match.replacements else None
                )
                
                issues.append(issue)
        
        except Exception as e:
            print(f"Grammar analysis error: {e}")
        
        return issues
    
    def _categorize_rule(self, rule_id: str, category: str) -> IssueType:
        """Categorize the rule into an issue type."""
        if 'PUNCTUATION' in category or 'COMMA' in rule_id:
            return IssueType.PUNCTUATION
        return IssueType.GRAMMAR
    
    def _determine_severity(self, match) -> Severity:
        """Determine severity based on the match."""
        if match.ruleIssueType == 'misspelling':
            return Severity.ERROR
        elif match.ruleIssueType == 'grammar':
            return Severity.ERROR
        elif match.ruleIssueType == 'typographical':
            return Severity.WARNING
        else:
            return Severity.SUGGESTION
    
    def _get_context(self, text: str, offset: int, length: int, window: int = 30) -> str:
        """Extract context around the error."""
        start = max(0, offset - window)
        end = min(len(text), offset + length + window)
        
        context = text[start:end]
        error_start = offset - start
        error_end = error_start + length
        
        # Highlight the error
        highlighted = (
            context[:error_start] + 
            ">>>" + context[error_start:error_end] + "<<<" + 
            context[error_end:]
        )
        
        return highlighted.strip()
    
    def _create_explanation(self, match) -> str:
        """Create a detailed explanation of the issue."""
        explanation = match.message
        if match.rule.description:
            explanation += f" ({match.rule.description})"
        return explanation
    
    def _create_learning_tip(self, match) -> str:
        """Create an educational tip for the user."""
        tips = {
            'COMMA': "Remember: Use commas to separate clauses and items in a list. Consider the sentence structure and natural pauses.",
            'AGREEMENT': "Subject-verb agreement: Make sure your subject and verb match in number (singular/plural).",
            'TENSE': "Verb tense consistency: Keep your tenses consistent unless you're deliberately shifting time frames.",
            'ARTICLE': "Articles (a, an, the): Use 'a' before consonant sounds, 'an' before vowel sounds, 'the' for specific items.",
        }
        
        for key, tip in tips.items():
            if key in match.ruleId:
                return tip
        
        return "Review the grammar rule mentioned and practice identifying similar patterns in your writing."
    
    def __del__(self):
        """Clean up resources."""
        if hasattr(self, 'tool'):
            self.tool.close()

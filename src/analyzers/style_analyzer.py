# WARNING: template code, may need edits
"""Style and clarity analysis."""

from typing import List
import re
from src.models.issue import Issue, IssueType, Severity


class StyleAnalyzer:
    """Analyzes text for style and clarity issues."""
    
    def __init__(self, nlp):
        """Initialize the style analyzer.
        
        Args:
            nlp: spaCy language model
        """
        self.nlp = nlp
        
        # Common weak words and phrases
        self.weak_words = [
            'very', 'really', 'quite', 'rather', 'somewhat', 'just',
            'actually', 'basically', 'literally', 'simply'
        ]
        
        # Passive voice indicators
        self.passive_indicators = ['was', 'were', 'been', 'being', 'is', 'are', 'am']
        
        # Wordy phrases
        self.wordy_phrases = {
            'in order to': 'to',
            'due to the fact that': 'because',
            'at this point in time': 'now',
            'for the purpose of': 'for',
            'in the event that': 'if',
            'with regard to': 'about',
        }
    
    def analyze(self, text: str, doc) -> List[Issue]:
        """Analyze text for style issues.
        
        Args:
            text: The text to analyze
            doc: spaCy doc object
            
        Returns:
            List of style-related issues
        """
        issues = []
        
        issues.extend(self._check_weak_words(text, doc))
        issues.extend(self._check_passive_voice(text, doc))
        issues.extend(self._check_wordy_phrases(text))
        issues.extend(self._check_sentence_length(doc))
        issues.extend(self._check_repeated_words(text, doc))
        
        return issues
    
    def _check_weak_words(self, text: str, doc) -> List[Issue]:
        """Check for weak intensifiers and filler words."""
        issues = []
        
        for token in doc:
            if token.text.lower() in self.weak_words:
                issue = Issue(
                    issue_type=IssueType.WORD_CHOICE,
                    severity=Severity.SUGGESTION,
                    position=token.idx,
                    length=len(token.text),
                    message=f"Weak word: '{token.text}'",
                    explanation=f"The word '{token.text}' is a weak intensifier that often adds little meaning.",
                    learning_tip="Try removing this word or replacing it with a more specific, stronger word. Ask yourself: Does this word add meaningful information?",
                    context=self._get_context(text, token.idx, len(token.text)),
                    suggested_fix="Consider removing or replacing"
                )
                issues.append(issue)
        
        return issues
    
    def _check_passive_voice(self, text: str, doc) -> List[Issue]:
        """Check for passive voice constructions."""
        issues = []
        
        for sent in doc.sents:
            # Look for passive voice pattern: auxiliary verb + past participle
            for i, token in enumerate(sent):
                if token.lemma_ in self.passive_indicators and i + 1 < len(sent):
                    next_token = sent[i + 1]
                    if next_token.tag_ == 'VBN':  # Past participle
                        issue = Issue(
                            issue_type=IssueType.STYLE,
                            severity=Severity.SUGGESTION,
                            position=token.idx,
                            length=next_token.idx + len(next_token.text) - token.idx,
                            message="Possible passive voice",
                            explanation="This sentence may be in passive voice, which can make writing less direct and engaging.",
                            learning_tip="Active voice tip: Identify who/what is performing the action and make them the subject. Example: 'The ball was thrown by John' 17 'John threw the ball'",
                            context=sent.text,
                            suggested_fix="Consider rewriting in active voice"
                        )
                        issues.append(issue)
                        break
        
        return issues
    
    def _check_wordy_phrases(self, text: str) -> List[Issue]:
        """Check for wordy phrases that can be simplified."""
        issues = []
        
        for phrase, replacement in self.wordy_phrases.items():
            pattern = re.compile(r'\b' + re.escape(phrase) + r'\b', re.IGNORECASE)
            
            for match in pattern.finditer(text):
                issue = Issue(
                    issue_type=IssueType.CLARITY,
                    severity=Severity.SUGGESTION,
                    position=match.start(),
                    length=len(match.group()),
                    message=f"Wordy phrase: '{match.group()}'",
                    explanation=f"The phrase '{match.group()}' can be simplified to make your writing more concise.",
                    learning_tip=f"Conciseness tip: Replace '{phrase}' with '{replacement}'. Simpler phrases make your writing clearer and more direct.",
                    context=self._get_context(text, match.start(), len(match.group())),
                    suggested_fix=replacement
                )
                issues.append(issue)
        
        return issues
    
    def _check_sentence_length(self, doc) -> List[Issue]:
        """Check for overly long sentences."""
        issues = []
        
        for sent in doc.sents:
            word_count = len([token for token in sent if not token.is_punct])
            
            if word_count > 30:
                issue = Issue(
                    issue_type=IssueType.CLARITY,
                    severity=Severity.WARNING,
                    position=sent.start_char,
                    length=len(sent.text),
                    message=f"Long sentence ({word_count} words)",
                    explanation="This sentence is quite long and may be hard to follow.",
                    learning_tip="Long sentence tip: Try breaking this into 2-3 shorter sentences. Look for natural break points like 'and', 'but', or semicolons. Each sentence should express one main idea.",
                    context=sent.text[:100] + "..." if len(sent.text) > 100 else sent.text,
                    suggested_fix="Consider breaking into shorter sentences"
                )
                issues.append(issue)
        
        return issues
    
    def _check_repeated_words(self, text: str, doc) -> List[Issue]:
        """Check for repeated words in close proximity."""
        issues = []
        window_size = 10
        
        tokens = [token for token in doc if token.is_alpha and not token.is_stop]
        
        for i, token in enumerate(tokens):
            word_lower = token.text.lower()
            
            # Check next few tokens
            for j in range(i + 1, min(i + window_size, len(tokens))):
                if tokens[j].text.lower() == word_lower:
                    issue = Issue(
                        issue_type=IssueType.STYLE,
                        severity=Severity.SUGGESTION,
                        position=tokens[j].idx,
                        length=len(tokens[j].text),
                        message=f"Repeated word: '{token.text}'",
                        explanation=f"The word '{token.text}' appears multiple times in close proximity.",
                        learning_tip="Repetition tip: Use synonyms or rephrase to avoid repetition. This makes your writing more engaging and professional.",
                        context=self._get_context(text, tokens[j].idx, len(tokens[j].text)),
                        suggested_fix="Consider using a synonym"
                    )
                    issues.append(issue)
                    break
        
        return issues
    
    def _get_context(self, text: str, offset: int, length: int, window: int = 40) -> str:
        """Extract context around the issue."""
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

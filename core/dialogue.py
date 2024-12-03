"""Dialogue management for Socratic reasoning."""

import logging
from typing import List, Dict, Any
from .agent import SocraticPredictor

logger = logging.getLogger(__name__)

class QuestionGenerator(SocraticPredictor):
    """Generate Socratic questions for a given context."""
    
    def __init__(self):
        instructions = """Generate insightful Socratic questions that:
        1. Probe deeper understanding
        2. Challenge assumptions
        3. Explore implications
        4. Examine evidence
        5. Consider alternative viewpoints
        Only generate questions, no other text."""
        
        super().__init__(
            signature="context -> questions: list[str]",
            instructions=instructions
        )
        
    def forward(self, context: str) -> List[str]:
        """Generate Socratic questions based on the given context.
        
        Args:
            context: The context to generate questions from
            
        Returns:
            List of generated questions
        """
        try:
            result = super().forward(context=context)
            return result.questions if hasattr(result, 'questions') else []
        except Exception as e:
            logger.error(f"Question generation failed: {str(e)}")
            return []

class SocraticDialogue:
    """Manages Socratic dialogue flow."""
    
    def __init__(self):
        """Initialize dialogue manager."""
        self.generate = QuestionGenerator()
        self.conversation_history: List[Dict[str, Any]] = []
        
    def generate_questions(self, context: str) -> List[str]:
        """Generate relevant Socratic questions based on context.
        
        Args:
            context: Current conversation context
            
        Returns:
            List of generated questions
        """
        questions = self.generate.forward(context)
        if questions:
            self.conversation_history.append({
                'type': 'questions',
                'content': questions,
                'context': context
            })
        return questions
        
    def get_history(self) -> List[Dict[str, Any]]:
        """Get conversation history.
        
        Returns:
            List of conversation turns
        """
        return self.conversation_history
        
    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []

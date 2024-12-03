"""Reasoning evaluation and judgment module."""

import logging
from typing import Optional, Union, Any
from .agent import SocraticLM
import dspy

logger = logging.getLogger(__name__)

class ReasoningJudge:
    """Judge module for evaluating reasoning outputs with preference learning."""
    
    def __init__(self):
        """Initialize the reasoning judge."""
        self.lm = SocraticLM()
        
        # Rating predictor for single outputs
        rating_instructions = """Rate this solution from 0 to 1, where 1 is perfect.
        Consider:
        1. Accuracy of information
        2. Clarity of explanation
        3. Logical coherence
        4. Completeness
        Only respond with a number."""
        
        self.rating_judge = dspy.Predict("output -> rating: float")
        self.rating_judge.signature = self.rating_judge.signature.with_instructions(rating_instructions)
        self.rating_judge.lm = self.lm
        
        # Preference predictor for comparing outputs
        preference_instructions = """Compare these two solutions and respond with only 'true' or 'false'.
        Consider:
        1. Accuracy
        2. Clarity
        3. Efficiency
        4. Completeness
        Is Solution 1 better than Solution 2?"""
        
        self.preference_judge = dspy.Predict("output1: str, output2: str -> output_1_better: bool")
        self.preference_judge.signature = self.preference_judge.signature.with_instructions(preference_instructions)
        self.preference_judge.lm = self.lm
        
    def forward(self, output1: str, output2: Optional[str] = None) -> Any:
        """Judge outputs either by rating a single output or comparing two outputs.
        
        Args:
            output1: First output to evaluate
            output2: Optional second output for comparison
            
        Returns:
            For single output: Rating prediction (0-1)
            For comparison: Boolean prediction (is output1 better?)
        """
        try:
            if output2 is None:
                # Single output rating
                if not output1:
                    return dspy.Prediction(score=0.0)
                rating = self.rating_judge(output=output1)
                return dspy.Prediction(score=float(rating.rating))
            else:
                # Comparison between two outputs
                if not output1 or not output2:
                    raise ValueError("Both outputs must be provided for comparison")
                return self.preference_judge(output1=output1, output2=output2)
        except Exception as e:
            logger.error(f"Judgment failed: {str(e)}")
            if output2 is None:
                return dspy.Prediction(score=0.0)
            raise

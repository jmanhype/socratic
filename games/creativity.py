"""Creativity game implementation."""

import logging
from typing import Any, Optional
from ..core.agent import SocraticPredictor

logger = logging.getLogger(__name__)

class CreativityGame:
    """Game focused on creative reasoning and generation."""
    
    def __init__(self):
        """Initialize creativity game."""
        self.create = SocraticPredictor(
            signature="prompt: str -> creative_output: str",
            instructions="""Generate creative and insightful outputs that:
            1. Show originality
            2. Maintain coherence
            3. Demonstrate adaptability
            4. Consider multiple perspectives
            5. Balance novelty with usefulness"""
        )
        
    def forward(self, prompt: str) -> Any:
        """Generate creative output for a prompt.
        
        Args:
            prompt: Input prompt for creative generation
            
        Returns:
            Generated creative output
        """
        try:
            result = self.create.forward(prompt=prompt)
            return result.creative_output if hasattr(result, 'creative_output') else str(result)
        except Exception as e:
            logger.error(f"Creative generation failed: {str(e)}")
            return str(e)

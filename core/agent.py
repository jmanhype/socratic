"""Base agent components for the Socratic framework."""

import os
import dspy
from typing import Optional
from ..utils.config import load_config

class SocraticLM(dspy.LM):
    """Language model wrapper for Socratic reasoning."""
    
    def __init__(self, model: str = "gpt-4", temperature: float = 0.0,
                 max_tokens: int = 1000, api_key: Optional[str] = None):
        """Initialize the language model.
        
        Args:
            model: The OpenAI model to use
            temperature: Temperature for generation (0.0 for deterministic)
            max_tokens: Maximum tokens to generate
            api_key: OpenAI API key (defaults to environment variable)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found")
            
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.model = model
            
        super().__init__(
            model=model,
            model_type="chat",
            temperature=temperature,
            max_tokens=max_tokens,
            api_key=self.api_key
        )

class SocraticPredictor(dspy.Predict):
    """Base predictor for Socratic reasoning tasks."""
    
    def __init__(self, signature: Optional[str] = None, 
                 instructions: Optional[str] = None):
        """Initialize the predictor.
        
        Args:
            signature: The signature for the predictor
            instructions: Instructions for the predictor
        """
        if signature is None:
            signature = "input -> output"
        super().__init__(signature)
        if instructions and hasattr(self.signature, 'with_instructions'):
            self.signature = self.signature.with_instructions(instructions)
        self.lm = dspy.settings.lm
        
    def forward(self, **kwargs):
        """Forward pass for prediction."""
        try:
            return super().forward(**kwargs)
        except Exception as e:
            raise RuntimeError(f"Prediction failed: {str(e)}")

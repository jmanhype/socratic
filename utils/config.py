"""Configuration settings for the Socratic framework."""

import os
import uuid
from typing import Dict, Any
from dotenv import load_dotenv

def load_config() -> None:
    """Load environment variables from .env file."""
    load_dotenv()

# OpenAI configuration
OPENAI_CONFIG: Dict[str, Any] = {
    "api_key": os.getenv("OPENAI_API_KEY"),
    "model": "gpt-4-turbo-preview"
}

# Mem0 configuration
MEM0_CONFIG: Dict[str, Any] = {
    "api_key": os.getenv("MEM0_API_KEY"),
    "user_id": "test_user_id",  # Fixed ID for testing
    "agent_id": "test_agent_id",  # Fixed ID for testing
    "api_version": "v1.1",
    "rate_limit": {
        "max_retries": 3,
        "retry_delay": 60,  # Delay in seconds between retries
        "rate_limit_delay": 3600  # 1 hour delay when rate limit is hit
    },
    "index_delay": 5  # Wait 5 seconds for indexing after add operations
}

# Memory client configuration
MEMORY_CONFIG: Dict[str, Any] = {
    "api_key": os.getenv("OPENAI_API_KEY")  # Use OpenAI API key for memory operations
}

# DSPy configuration
DSPY_CONFIG: Dict[str, Any] = {
    "lm": OPENAI_CONFIG["model"],
    "temperature": 0.7
}

# Default configuration
DEFAULTS: Dict[str, Any] = {
    "max_workers": 4,
    "timeout": 30,
    "retry_attempts": 3
}

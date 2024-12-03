"""Shared test fixtures."""

import os
import pytest
from unittest.mock import Mock, patch

@pytest.fixture(autouse=True)
def mock_openai():
    """Mock OpenAI API for testing."""
    os.environ["OPENAI_API_KEY"] = "test_key"
    with patch("openai.OpenAI") as mock:
        mock.return_value = Mock()
        yield mock

@pytest.fixture
def mock_memory_client():
    """Mock Mem0 client for testing."""
    with patch("mem0.Memory") as mock:
        mock_instance = Mock()
        mock.return_value = mock_instance
        
        # Mock search responses
        def search_side_effect(*args, **kwargs):
            return [
                {
                    "id": "test_id",
                    "memory": "Test memory content",
                    "metadata": {"type": "test"},
                    "score": 0.95
                }
            ]
        mock_instance.search.side_effect = search_side_effect
        
        # Mock add response
        def add_side_effect(*args, **kwargs):
            return {"status": "success"}
        mock_instance.add.side_effect = add_side_effect
        
        yield mock_instance

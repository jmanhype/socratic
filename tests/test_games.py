"""Test suite for Socratic Games."""

import os
import sys
from dotenv import load_dotenv
from mem0 import Memory

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from socratic.games.reasoning import ReasoningGame
from socratic.utils.config import MEM0_CONFIG

# Load environment variables
load_dotenv()

print("\nRunning Socratic Games Tests")
print("============================\n")

def test_initialization():
    """Test basic initialization of ReasoningGame."""
    print("=== Testing ReasoningGame Initialization ===\n")
    
    try:
        memory = Memory()
        game = ReasoningGame(memory_client=memory)
        assert game is not None
        assert game.conversation_history == []
        assert game.memory_context == ""
        assert game.agent_id == MEM0_CONFIG["agent_id"]
        assert game.user_id == MEM0_CONFIG["user_id"]
        print("Basic initialization tests passed\n")
    except Exception as e:
        print(f"Error in initialization tests: {str(e)}\n")
        raise

def test_context_preservation():
    """Test context preservation in conversations."""
    print("=== Testing Context Preservation ===\n")
    
    memory = Memory()
    game = ReasoningGame(memory_client=memory)
    
    # Test basic conversation flow
    print("\n1. Testing basic conversation flow...")
    response = game.forward("How old is Barack Obama?")
    assert response is not None
    print("Basic conversation test passed\n")
    
    # Test memory context
    print("2. Testing memory context...")
    game.update_memory_context()
    context = game.memory_context
    assert isinstance(context, str)
    print("Memory context test passed\n")
    
    # Test follow-up questions
    print("3. Testing follow-up with context...")
    response = game.forward("And how old is Michelle Obama?")
    assert response is not None
    assert len(game.conversation_history) == 2
    print("Follow-up question test passed\n")
    
    # Test memory retrieval
    print("4. Testing memory retrieval...")
    history = game.get_relevant_memories("Obama")
    assert isinstance(history, list)
    print("Memory retrieval test passed\n")

def test_memory_operations():
    """Test memory-related operations."""
    print("=== Testing Memory Operations ===\n")
    
    memory = Memory()
    game = ReasoningGame(memory_client=memory)
    
    # Test insight storage
    print("\n1. Testing insight storage...")
    insight = "Barack Obama was born on August 4, 1961"
    result = game.store_insight(insight, metadata={"source": "test"})
    assert result is not None
    print("Insight storage test passed\n")
    
    # Test reasoning output storage
    print("2. Testing reasoning output storage...")
    output = "Barack Obama is 62 years old in 2024"
    result = game.store_reasoning_output(output, metadata={"source": "test"})
    assert result is not None
    print("Reasoning output storage test passed\n")
    
    # Test memory search
    print("3. Testing memory search...")
    results = game.search_memories("Obama")
    assert isinstance(results, list)
    assert len(results) > 0
    print("Memory search test passed\n")
    
    # Test memory type filtering
    print("4. Testing memory type filtering...")
    insights = game.get_memory_by_type("insight")
    assert isinstance(insights, list)
    assert len(insights) > 0
    print("Memory type filtering test passed\n")

if __name__ == "__main__":
    try:
        # Run tests
        test_initialization()
        test_context_preservation()
        test_memory_operations()
        print("\nAll tests completed successfully! \n")
    except Exception as e:
        print(f"\nTest suite failed: {str(e)}\n")
        sys.exit(1)

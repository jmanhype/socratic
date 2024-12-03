"""Test the core components of the Socratic framework."""

import logging
import sys
import os
from dotenv import load_dotenv
import dspy

# Add the package directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Load environment variables
load_dotenv()

from socratic.core.agent import SocraticLM
from socratic.core.judge import ReasoningJudge

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def test_socratic_lm():
    """Test the SocraticLM functionality."""
    print("\n=== Testing SocraticLM ===\n")
    
    # Initialize LM
    lm = SocraticLM()
    assert isinstance(lm, dspy.LM), "SocraticLM should be a DSPy LM instance"
    
    # Test basic configuration
    assert lm.model == "gpt-4", "Default model should be gpt-4"
    assert lm.temperature == 0.0, "Default temperature should be 0.0"
    assert lm.max_tokens == 1000, "Default max_tokens should be 1000"
    print("Basic LM configuration tests passed")

def test_reasoning_judge():
    """Test the ReasoningJudge functionality."""
    print("\n=== Testing Enhanced Reasoning Judge ===\n")
    
    # Initialize the judge
    judge = ReasoningJudge()
    assert hasattr(judge, 'rating_judge'), "Judge should have rating_judge"
    assert hasattr(judge, 'preference_judge'), "Judge should have preference_judge"
    
    # Test outputs to evaluate
    output1 = """
    The age calculation for Barack Obama:
    1. Barack Obama was born on August 4, 1961
    2. As of April 2024, we calculate:
       - From 1961 to 2024 is 63 years
       - From August to April is -4 months
    Therefore, Barack Obama will be 62 years old in April 2024.
    """
    
    output2 = """
    Barack Obama's age in April 2024:
    Born: August 4, 1961
    Age in April 2024 = 62 years and 8 months
    """
    
    # Test single output rating
    print("\n1. Testing single output rating:")
    print("\nEvaluating Output 1:")
    print(output1)
    rating1 = judge.forward(output1)
    print(f"Rating: {rating1.score if hasattr(rating1, 'score') else 0.0}")
    assert hasattr(rating1, 'score'), "Rating should have a score attribute"
    assert 0 <= rating1.score <= 1, "Rating should be between 0 and 1"
    
    print("\nEvaluating Output 2:")
    print(output2)
    rating2 = judge.forward(output2)
    print(f"Rating: {rating2.score if hasattr(rating2, 'score') else 0.0}")
    assert hasattr(rating2, 'score'), "Rating should have a score attribute"
    assert 0 <= rating2.score <= 1, "Rating should be between 0 and 1"
    
    # Test preference comparison
    print("\n2. Testing preference comparison:")
    print("\nComparing:")
    print("Output 1:")
    print(output1)
    print("\nOutput 2:")
    print(output2)
    preference = judge.forward(output1, output2)
    result = preference.output_1_better if hasattr(preference, 'output_1_better') else False
    print(f"\nIs Output 1 better than Output 2? {result}")
    assert hasattr(preference, 'output_1_better'), "Preference should have output_1_better attribute"
    assert isinstance(result, bool), "Preference result should be boolean"
    
    # Test error handling
    print("\n3. Testing error handling:")
    print("Testing with None input...")
    rating_none = judge.forward(None)
    print(f"Rating with None input: {rating_none.score if hasattr(rating_none, 'score') else 0.0}")
    assert hasattr(rating_none, 'score'), "None input should still return a rating"
    assert rating_none.score == 0.0, "None input should get a zero rating"
    
    try:
        # This should raise an error
        judge.forward(None, None).output_1_better
        assert False, "Should have raised an error"
    except Exception as e:
        print(f"Expected error occurred: {str(e)}")
        assert True, "Error was properly handled"

if __name__ == "__main__":
    # Run all tests
    print("\nRunning Socratic Framework Tests")
    print("================================")
    
    test_socratic_lm()
    test_reasoning_judge()

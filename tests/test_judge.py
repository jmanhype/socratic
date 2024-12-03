import logging
import sys
import os

# Add the package directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from socratic_agent2 import ReasoningJudge

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def main():
    try:
        # Initialize the judge
        print("\n=== Testing Enhanced Reasoning Judge ===\n")
        judge = ReasoningJudge()
        
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
        
        print("\nEvaluating Output 2:")
        print(output2)
        rating2 = judge.forward(output2)
        print(f"Rating: {rating2.score if hasattr(rating2, 'score') else 0.0}")
        
        # Test preference comparison
        print("\n2. Testing preference comparison:")
        print("\nComparing:")
        print("Output 1:")
        print(output1)
        print("\nOutput 2:")
        print(output2)
        preference = judge.forward(output1, output2)
        print(f"\nIs Output 1 better than Output 2? {preference.output_1_better if hasattr(preference, 'output_1_better') else False}")
        
        # Test error handling
        print("\n3. Testing error handling:")
        print("Testing with None input...")
        rating_none = judge.forward(None)
        print(f"Rating with None input: {rating_none.score if hasattr(rating_none, 'score') else 0.0}")
        
        try:
            # This should raise an error
            judge.forward(None, None).output_1_better
            print("Error: Expected exception not raised")
        except AttributeError as e:
            print(f"Expected error occurred: {str(e)}")
            
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()

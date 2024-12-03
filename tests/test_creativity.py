"""Test the creativity components of the Socratic framework."""

import logging
import sys
import os
from dotenv import load_dotenv

# Add the package directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Load environment variables
load_dotenv()

from socratic.games.creativity import CreativityGame
from socratic.core.improver import Improver

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def test_creativity_game():
    """Test the CreativityGame functionality."""
    print("\n=== Testing CreativityGame ===\n")
    
    # Initialize game
    game = CreativityGame()
    
    # Test creative generation
    print("\n1. Testing creative generation...")
    prompt = "Generate a creative story about a time-traveling scientist"
    response = game.forward(prompt)
    
    assert response is not None, "Should get a creative response"
    assert isinstance(response, str), "Response should be a string"
    assert len(response) > 0, "Response should not be empty"
    print("Creative generation test passed")
    
    # Test with different creative tasks
    print("\n2. Testing different creative tasks...")
    tasks = [
        "Write a haiku about artificial intelligence",
        "Create a metaphor for quantum computing",
        "Design a fictional invention that solves climate change"
    ]
    
    for task in tasks:
        response = game.forward(task)
        assert response is not None, f"Should get response for task: {task}"
        assert len(response) > 0, f"Response should not be empty for task: {task}"
    
    print("Multiple creative tasks test passed")

def test_improver():
    """Test the Improver functionality."""
    print("\n=== Testing Improver ===\n")
    
    # Initialize improver
    improver = Improver()
    
    # Test basic improvement
    print("\n1. Testing basic improvement...")
    initial_solution = """
    def calculate_age(birth_year, current_year):
        return current_year - birth_year
    """
    
    historical_context = """
    Previous improvements:
    1. Added error handling
    2. Considered month and day
    3. Added validation
    """
    
    improved = improver.forward(initial_solution, historical_context)
    assert improved is not None, "Should get improved solution"
    assert isinstance(improved, str), "Improved solution should be a string"
    assert len(improved) > len(initial_solution), "Improved solution should be more detailed"
    print("Basic improvement test passed")
    
    # Test improvement without context
    print("\n2. Testing improvement without context...")
    improved_no_context = improver.forward(initial_solution)
    assert improved_no_context is not None, "Should get improved solution without context"
    print("Improvement without context test passed")
    
    # Test iterative improvement
    print("\n3. Testing iterative improvement...")
    iterations = 3
    current_solution = initial_solution
    
    for i in range(iterations):
        new_solution = improver.forward(current_solution, f"Iteration {i+1}")
        assert new_solution is not None, f"Should get improvement in iteration {i+1}"
        current_solution = new_solution
    
    print("Iterative improvement test passed")

if __name__ == "__main__":
    print("\nRunning Socratic Creativity Tests")
    print("================================")
    
    test_creativity_game()
    test_improver()

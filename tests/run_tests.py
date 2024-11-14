import unittest
import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent.parent / 'src'
sys.path.append(str(src_path))

def run_tests():
    """Run all tests in the test suite."""
    # Add project root to Python path
    project_root = Path(__file__).parent.parent
    sys.path.append(str(project_root))

    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = Path(__file__).parent
    suite = loader.discover(start_dir)
    
    # Run tests with verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return 0 if tests passed, 1 if any failed
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_tests()) 
import unittest
import sys
from pathlib import Path
from tests.create_sample_files import create_sample_files
import pytest
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_tests():
    """Run all tests in the test suite."""
    try:
        # Add project root to Python path
        project_root = Path(__file__).parent.parent
        sys.path.insert(0, str(project_root))
        
        # Create sample files
        create_sample_files()
        
        # Run pytest for Streamlit UI tests
        logger.info("Running Streamlit UI tests...")
        pytest_result = pytest.main(['-v', '--tb=short', str(project_root / 'tests')])
        
        if pytest_result != 0:
            logger.warning("Some Streamlit UI tests failed or had errors")
        
        # Run unittest for remaining tests
        logger.info("Running unit tests...")
        loader = unittest.TestLoader()
        start_dir = Path(__file__).parent
        suite = loader.discover(start_dir, pattern='test_*.py')
        
        # Filter out the obsolete test files and Streamlit tests
        filtered_tests = unittest.TestSuite()
        excluded_patterns = ['test_main_window', 'test_streamlit_ui']
        for test in suite._tests:
            if not any(x in str(test) for x in excluded_patterns):
                filtered_tests.addTest(test)
        
        # Run tests with verbosity
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(filtered_tests)
        
        # Return overall success status
        return 0 if result.wasSuccessful() and pytest_result == 0 else 1
        
    except Exception as e:
        logger.error(f"Error running tests: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(run_tests()) 
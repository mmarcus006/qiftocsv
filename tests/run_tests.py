import unittest
import sys
from pathlib import Path
from tests.create_sample_files import create_sample_files
import pytest

def run_tests():
    """Run all tests in the test suite."""
    # Add project root to Python path
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))
    
    # Create sample files
    create_sample_files()
    
    # Run pytest for Streamlit UI tests
    pytest.main(['-v', str(project_root / 'tests')])
    
    # Run unittest for remaining tests
    loader = unittest.TestLoader()
    start_dir = Path(__file__).parent
    # Exclude the old main_window test and streamlit UI test from unittest discovery
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Filter out the obsolete test files
    filtered_tests = unittest.TestSuite()
    for test in suite._tests:
        if not any(x in str(test) for x in ['test_main_window', 'test_streamlit_ui']):
            filtered_tests.addTest(test)
    
    # Run tests with verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(filtered_tests)
    
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_tests()) 
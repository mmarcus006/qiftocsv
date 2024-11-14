import unittest
from pathlib import Path
import tempfile
import shutil

class BaseTestCase(unittest.TestCase):
    """Base test case with common utilities for QIF to CSV converter tests."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test resources."""
        cls.test_dir = Path(tempfile.mkdtemp())
        cls.sample_data_dir = cls.test_dir / 'sample_data'
        cls.sample_data_dir.mkdir(exist_ok=True)
        
    @classmethod
    def tearDownClass(cls):
        """Clean up test resources."""
        shutil.rmtree(cls.test_dir)
        
    def create_test_file(self, content: str, filename: str) -> Path:
        """Create a test file with given content."""
        filepath = self.test_dir / filename
        filepath.write_text(content, encoding='utf-8')
        return filepath
        
    def create_sample_qif(self, transactions: list[str] = None) -> Path:
        """Create a sample QIF file for testing."""
        content = [
            "!Type:Bank",
            "D01/15/2024",
            "T-1000.00",
            "PPayee Name",
            "MTransaction Memo",
            "LCategory",
            "CX",
            "N1001",
            "^"
        ]
        
        if transactions:
            content.extend(transactions)
            
        return self.create_test_file('\n'.join(content), 'test.qif') 
from pathlib import Path
from datetime import datetime
from src.core.qif_parser import QIFParser
from tests.test_base import BaseTestCase

class TestQIFParser(BaseTestCase):
    """Test cases for QIFParser class."""
    
    def setUp(self):
        """Set up test case."""
        self.parser = QIFParser()
        
    def test_valid_file_reading(self):
        """Test reading a valid QIF file."""
        qif_file = self.create_sample_qif()
        result = self.parser.parse_file(qif_file)
        
        self.assertTrue(result)
        self.assertEqual(len(self.parser.transactions), 1)
        self.assertEqual(self.parser.get_account_type(), "Bank")
        
    def test_nonexistent_file(self):
        """Test handling of non-existent files."""
        with self.assertRaises(FileNotFoundError):
            self.parser.parse_file("nonexistent.qif")
            
    def test_empty_file(self):
        """Test handling of empty files."""
        empty_file = self.create_test_file("", "empty.qif")
        with self.assertRaises(ValueError):
            self.parser.parse_file(empty_file)
            
    def test_invalid_format(self):
        """Test handling of invalid file formats."""
        invalid_file = self.create_test_file("Invalid content", "invalid.qif")
        with self.assertRaises(ValueError):
            self.parser.parse_file(invalid_file)
            
    def test_different_date_formats(self):
        """Test handling of different date formats."""
        date_formats = [
            ("D01/15/2024", "%m/%d/%Y"),
            ("D01/15/24", "%m/%d/%y"),
            ("D2024-01-15", "%Y-%m-%d")
        ]
        
        for date_str, fmt in date_formats:
            content = [
                "!Type:Bank",
                date_str,
                "T-1000.00",
                "^"
            ]
            
            qif_file = self.create_test_file('\n'.join(content), f"date_test_{fmt}.qif")
            self.parser.parse_file(qif_file)
            
            transaction = self.parser.transactions[0]
            expected_date = datetime.strptime(date_str[1:], fmt)
            self.assertEqual(transaction['date'], expected_date)
            
    def test_special_characters(self):
        """Test handling of special characters in text fields."""
        content = [
            "!Type:Bank",
            "D01/15/2024",
            "T-1000.00",
            "PSpecial & Chars © ®",
            "MMemo with émojis 🎉",
            "^"
        ]
        
        qif_file = self.create_test_file('\n'.join(content), "special_chars.qif")
        self.parser.parse_file(qif_file)
        
        transaction = self.parser.transactions[0]
        self.assertEqual(transaction['payee'], "Special & Chars © ®")
        self.assertEqual(transaction['memo'], "Memo with émojis 🎉") 
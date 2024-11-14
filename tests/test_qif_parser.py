import unittest
from datetime import datetime
from pathlib import Path
from src.core.qif_parser import QIFParser, QIFParserError

class TestQIFParser(unittest.TestCase):
    def setUp(self):
        self.parser = QIFParser()
        self.samples_dir = Path(__file__).parent.parent / 'samples'
        
    def test_parse_investment_account_5383(self):
        """Test parsing of investment account 5383 transactions"""
        filepath = self.samples_dir / '5383_Investment_AllExports.txt'
        success = self.parser.parse_file(filepath)
        
        # Verify parsing was successful
        self.assertTrue(success)
        
        # Verify account type
        self.assertEqual(self.parser.get_account_type(), 'Invst')
        
        # Get all transactions
        transactions = self.parser.get_transactions()
        
        # Verify we have transactions
        self.assertTrue(len(transactions) > 0)
        
        # Verify first transaction
        first_trans = transactions[0]
        self.assertEqual(first_trans['date'], datetime(2024, 1, 15))
        self.assertEqual(first_trans['amount'], -1500.00)
        
    def test_parse_investment_account_8007(self):
        """Test parsing of investment account 8007 transactions"""
        # Consider adding a valid test file if needed
        pass

    def test_error_handling(self):
        """Test error handling for invalid files"""
        # Test non-existent file
        with self.assertRaises(FileNotFoundError):
            self.parser.parse_file('nonexistent.qif')
            
        # Test empty file
        empty_file = self.samples_dir / 'empty.qif'
        empty_file.write_text('')
        with self.assertRaises(ValueError):
            self.parser.parse_file(empty_file)
        empty_file.unlink()  # Clean up
        
    def test_amount_parsing(self):
        """Test parsing of different amount formats"""
        # Test valid amounts
        self.assertEqual(self.parser._parse_amount('1234.56'), 1234.56)
        self.assertEqual(self.parser._parse_amount('-1234.56'), -1234.56)
        self.assertEqual(self.parser._parse_amount('1,234.56'), 1234.56)
        self.assertEqual(self.parser._parse_amount('-1,234.56'), -1234.56)
        
        # Test invalid amount
        with self.assertRaises(ValueError):
            self.parser._parse_amount('invalid')

if __name__ == '__main__':
    unittest.main() 
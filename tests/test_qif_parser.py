import unittest
from datetime import datetime
from pathlib import Path
from src.core.qif_parser import QIFParser

class TestQIFParser(unittest.TestCase):
    def setUp(self):
        self.parser = QIFParser()
        self.samples_dir = Path(__file__).parent.parent / 'samples'
        
    def test_parse_investment_account_5383(self):
        """Test parsing of investment account 5383 transactions"""
        filepath = self.samples_dir / '5383_Investment_TransactionsOnly.txt'
        success = self.parser.parse_file(filepath)
        
        # Verify parsing was successful
        self.assertTrue(success)
        
        # Verify account type
        self.assertEqual(self.parser.get_account_type(), 'Bank')
        
        # Get all transactions
        transactions = self.parser.get_transactions()
        
        # Verify we have transactions
        self.assertTrue(len(transactions) > 0)
        
        # Verify first transaction
        first_trans = transactions[0]
        self.assertEqual(first_trans['date'], datetime(2024, 7, 7))
        self.assertEqual(first_trans['amount'], 19049.26)
        self.assertEqual(first_trans['payee'], 'Opening Balance')
        self.assertEqual(first_trans['category'], '[JPM - MRJ & DPJ - 5383]')
        
        # Verify a random transaction in the middle
        # Let's check the Fed Est Tax Payment transaction
        tax_payment = None
        for trans in transactions:
            if trans.get('memo') == 'Fed Est Tax Payment Q2 2024':
                tax_payment = trans
                break
                
        self.assertIsNotNone(tax_payment)
        self.assertEqual(tax_payment['amount'], -360000.00)
        self.assertEqual(tax_payment['category'], 'Tax:Fed')

    def test_parse_investment_account_8007(self):
        """Test parsing of investment account 8007 transactions"""
        filepath = self.samples_dir / '8007_Investment_TransactionsOnly.txt'
        success = self.parser.parse_file(filepath)
        
        # Verify parsing was successful
        self.assertTrue(success)
        
        # Verify account type
        self.assertEqual(self.parser.get_account_type(), 'Invst')
        
        # Get all transactions
        transactions = self.parser.get_transactions()
        
        # Verify we have transactions
        self.assertTrue(len(transactions) > 0)
        
        # Verify first investment transaction
        first_trans = transactions[1]  # Skip the voided cash transaction
        self.assertEqual(first_trans['date'], datetime(2023, 12, 31))
        self.assertEqual(first_trans['type'], 'ShrsIn')
        self.assertEqual(first_trans['security'], 'JPM TAX FREE RESERVE SWEEP FD FUND')
        self.assertEqual(first_trans['quantity'], 5.53)
        self.assertEqual(first_trans['price'], 1.0)
        self.assertEqual(first_trans['amount'], 5.53)
        
        # Verify a stock purchase transaction
        spy_purchase = None
        for trans in transactions:
            if trans.get('security') == 'SPDR S&P 500 ETF TRUST' and trans.get('type') == 'Buy':
                spy_purchase = trans
                break
                
        self.assertIsNotNone(spy_purchase)
        self.assertTrue(spy_purchase['amount'] > 0)
        self.assertTrue(spy_purchase['quantity'] > 0)
        self.assertTrue(spy_purchase['price'] > 0)

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
        self.assertEqual(self.parser._parse_amount('1234.56'), 1234.56)
        self.assertEqual(self.parser._parse_amount('-1234.56'), -1234.56)
        self.assertEqual(self.parser._parse_amount('1,234.56'), 1234.56)
        self.assertEqual(self.parser._parse_amount('-1,234.56'), -1234.56)
        
        with self.assertRaises(ValueError):
            self.parser._parse_amount('invalid')

if __name__ == '__main__':
    unittest.main() 
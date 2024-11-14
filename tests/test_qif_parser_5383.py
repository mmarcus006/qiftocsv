import unittest
from datetime import datetime
from pathlib import Path
from src.core.qif_parser import QIFParser

class TestQIFParser5383(unittest.TestCase):
    def setUp(self):
        self.parser = QIFParser()
        self.samples_dir = Path(__file__).parent.parent / 'samples'
        self.filepath = self.samples_dir / '5383_Investment_TransactionsOnly.QIF'
        
    def test_parse_5383_qif(self):
        """Test parsing of 5383 QIF file"""
        success = self.parser.parse_file(self.filepath)
        
        # Verify parsing was successful
        self.assertTrue(success)
        
        # Verify account type
        self.assertEqual(self.parser.get_account_type(), 'Bank')
        
        # Get all transactions
        transactions = self.parser.get_transactions()
        
        # Verify we have transactions
        self.assertGreater(len(transactions), 0)
        
        # Verify first transaction (Opening Balance)
        first_trans = transactions[0]
        self.assertEqual(first_trans['date'], datetime(2024, 7, 7))
        self.assertEqual(first_trans['amount'], 19049.26)
        self.assertEqual(first_trans['payee'], 'Opening Balance')
        self.assertEqual(first_trans['category'], '[JPM - MRJ & DPJ - 5383]')
        
        # Verify specific transactions
        self.verify_transaction_exists(transactions, {
            'date': datetime(2024, 7, 12),
            'amount': 10577.00,
            'payee': 'Vensure Hr Payroll',
            'category': 'Net Salary'
        })
        
        self.verify_transaction_exists(transactions, {
            'date': datetime(2024, 8, 5),
            'amount': -1349.00,
            'payee': 'Whitbyschool Scho Web',
            'category': 'Education:Tuition'
        })
        
        # Verify all amounts are properly parsed
        for trans in transactions:
            self.assertIsInstance(trans['amount'], float)
            self.assertIsInstance(trans['date'], datetime)
    
    def verify_transaction_exists(self, transactions, expected):
        """Helper method to verify a specific transaction exists"""
        found = False
        for trans in transactions:
            matches = all(
                trans.get(key) == value 
                for key, value in expected.items()
            )
            if matches:
                found = True
                break
        self.assertTrue(found, f"Transaction not found: {expected}")
    
    def test_transaction_integrity(self):
        """Test integrity of transaction data"""
        self.parser.parse_file(self.filepath)
        transactions = self.parser.get_transactions()
        
        for trans in transactions:
            # Verify required fields
            self.assertIn('date', trans)
            self.assertIn('amount', trans)
            
            # Verify date format
            self.assertIsInstance(trans['date'], datetime)
            
            # Verify amount is float
            self.assertIsInstance(trans['amount'], float)
            
            # Verify optional fields are strings when present
            if 'payee' in trans:
                self.assertIsInstance(trans['payee'], str)
            if 'category' in trans:
                self.assertIsInstance(trans['category'], str)
            if 'memo' in trans:
                self.assertIsInstance(trans['memo'], str)

if __name__ == '__main__':
    unittest.main() 
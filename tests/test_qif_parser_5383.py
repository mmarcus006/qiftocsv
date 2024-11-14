import unittest
from datetime import datetime
from pathlib import Path
from src.core.qif_parser import QIFParser, QIFParserError

class TestQIFParser5383(unittest.TestCase):
    def setUp(self):
        self.parser = QIFParser()
        self.sample_file = Path(__file__).parent / 'samples' / '5383_Investment.QIF'
        
        if not self.sample_file.exists():
            self.sample_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.sample_file, 'w') as f:
                f.write('!Type:Invst\n')
                f.write('D01/01/2020\n')
                f.write('N1000.00\n')
                f.write('YBUY\n')
                f.write('^\n')
        
        self.parser.parse_file(self.sample_file)
    
    def test_parse_5383_qif(self):
        """Test parsing of 5383 QIF file"""
        self.assertEqual(self.parser.get_account_type(), 'Invst')
        
        # Get all transactions
        transactions = self.parser.get_transactions()
        
        # Verify we have transactions
        self.assertGreater(len(transactions), 0)
        
        # Verify first transaction
        first_trans = transactions[0]
        self.assertEqual(first_trans['date'], datetime(2024, 7, 7))
        self.assertEqual(first_trans['amount'], 19049.26)
        
        # Verify investment-specific fields when present
        for trans in transactions:
            if 'type' in trans and trans['type'] in self.parser.INVESTMENT_TYPES:
                self.assertIn('security', trans)
                if trans['type'] in {'Buy', 'Sell', 'ShrsIn', 'ShrsOut'}:
                    self.assertIn('quantity', trans)
                    self.assertIn('price', trans)
        
    def test_transaction_integrity(self):
        """Test integrity of transaction data"""
        transactions = self.parser.get_transactions()
        
        for trans in transactions:
            # Verify required fields
            self.assertIn('date', trans)
            self.assertIn('amount', trans)
            
            # Verify field types
            self.assertIsInstance(trans['date'], datetime)
            self.assertIsInstance(trans['amount'], float)
            
            # Verify optional fields are strings when present
            for field in ['payee', 'category', 'memo', 'security', 'type']:
                if field in trans:
                    self.assertIsInstance(trans[field], str)
                    
            # Verify numeric fields are float when present
            for field in ['quantity', 'price']:
                if field in trans:
                    self.assertIsInstance(trans[field], float)

if __name__ == '__main__':
    unittest.main() 
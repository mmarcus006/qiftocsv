import unittest
from datetime import datetime
from pathlib import Path
from src.core.qif_parser import QIFParser, QIFParserError

class TestQIFParser5383(unittest.TestCase):
    def setUp(self):
        self.parser = QIFParser()
        self.sample_file = Path(__file__).parent / 'samples' / '5383_Investment.QIF'
        
        # Create sample file with valid investment transaction data
        if not self.sample_file.exists():
            self.sample_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.sample_file, 'w') as f:
                f.write('!Type:Invst\n')
                f.write('D07/07/2024\n')  # Date
                f.write('N19049.26\n')    # Amount
                f.write('YBUY\n')         # Transaction type
                f.write('IAAPL\n')        # Security
                f.write('Q100\n')         # Quantity
                f.write('P190.4926\n')    # Price
                f.write('^\n')            # End of transaction
        
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
        self.assertEqual(first_trans['type'], 'Buy')
        self.assertEqual(first_trans['security'], 'AAPL')
        self.assertEqual(first_trans['quantity'], 100.0)
        self.assertEqual(first_trans['price'], 190.4926)
        
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
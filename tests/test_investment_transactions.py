from pathlib import Path
from datetime import datetime
from src.core.qif_parser import QIFParser
from src.core.csv_generator import CSVGenerator
from tests.test_base import BaseTestCase

class TestInvestmentTransactions(BaseTestCase):
    """Test cases for investment transaction handling."""
    
    def setUp(self):
        """Set up test case."""
        self.parser = QIFParser()
        self.generator = CSVGenerator()
        self.samples_dir = Path(__file__).parent.parent / 'samples'
        
    def test_5383_investment_transactions(self):
        """Test parsing 5383 investment transactions file."""
        qif_file = self.samples_dir / '5383_Investment_TransactionsOnly.txt'
        self.parser.parse_file(qif_file)
        transactions = self.parser.get_transactions()
        
        # Verify basic transaction structure
        self.assertGreater(len(transactions), 0)
        
        # Test specific transaction fields
        for transaction in transactions:
            if 'amount' in transaction:
                self.assertIsInstance(transaction['amount'], float)
            if 'date' in transaction:
                self.assertIsInstance(transaction['date'], datetime)
                
    def test_5383_all_exports(self):
        """Test parsing complete 5383 investment export file."""
        qif_file = self.samples_dir / '5383_Investment_AllExports.txt'
        self.parser.parse_file(qif_file)
        transactions = self.parser.get_transactions()
        
        # Verify investment-specific fields
        investment_fields = ['security', 'quantity', 'price']
        for transaction in transactions:
            if transaction.get('type') == 'Buy':
                for field in investment_fields:
                    self.assertIn(field, transaction)
                    
    def test_investment_calculations(self):
        """Test investment transaction calculations."""
        qif_file = self.samples_dir / '5383_Investment_AllExports.txt'
        self.parser.parse_file(qif_file)
        transactions = self.parser.get_transactions()
        
        for transaction in transactions:
            if all(field in transaction for field in ['quantity', 'price', 'amount']):
                # Verify amount equals quantity times price
                calculated_amount = float(transaction['quantity']) * float(transaction['price'])
                self.assertAlmostEqual(
                    float(transaction['amount']),
                    calculated_amount,
                    places=2
                ) 
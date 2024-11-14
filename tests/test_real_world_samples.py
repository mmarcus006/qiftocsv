from pathlib import Path
from datetime import datetime
from qiftocsv.src.core.qif_parser import QIFParser
from qiftocsv.src.core.csv_generator import CSVGenerator
from qiftocsv.tests.test_base import BaseTestCase

class TestRealWorldSamples(BaseTestCase):
    """Test cases using real-world QIF sample files."""
    
    def setUp(self):
        """Set up test case."""
        self.parser = QIFParser()
        self.generator = CSVGenerator()
        self.samples_dir = Path(__file__).parent.parent / 'samples'
        
    def test_quicken_2020_format(self):
        """Test parsing Quicken 2020 format QIF file."""
        qif_file = self.samples_dir / 'quicken_2020.qif'
        self.parser.parse_file(qif_file)
        transactions = self.parser.get_transactions()
        
        # Verify specific Quicken 2020 format features
        self.assertEqual(self.parser.get_account_type(), "Bank")
        self.assertGreater(len(transactions), 0)
        
        # Test specific transaction format
        first_transaction = transactions[0]
        self.assertIn('date', first_transaction)
        self.assertIn('amount', first_transaction)
        self.assertIsInstance(first_transaction['amount'], float)
        
    def test_multi_account_file(self):
        """Test parsing QIF file with multiple accounts."""
        qif_file = self.samples_dir / 'multi_account.qif'
        self.parser.parse_file(qif_file)
        transactions = self.parser.get_transactions()
        
        # Verify account types and transactions
        unique_categories = set(
            t['category'] for t in transactions 
            if 'category' in t
        )
        self.assertGreater(len(unique_categories), 1)
        
    def test_investment_transactions(self):
        """Test parsing investment transactions."""
        qif_file = self.samples_dir / 'investments.qif'
        self.parser.parse_file(qif_file)
        transactions = self.parser.get_transactions()
        
        # Verify investment-specific fields
        investment_fields = ['security', 'price', 'quantity']
        for transaction in transactions:
            for field in investment_fields:
                if field in transaction:
                    self.assertIsNotNone(transaction[field])
                    
    def test_international_transactions(self):
        """Test parsing transactions with international characters."""
        qif_file = self.samples_dir / 'international.qif'
        self.parser.parse_file(qif_file)
        transactions = self.parser.get_transactions()
        
        # Test international character handling
        for transaction in transactions:
            if 'payee' in transaction:
                # Verify no encoding issues
                self.assertIsInstance(transaction['payee'], str)
                # Verify international characters preserved
                if any(ord(c) > 127 for c in transaction['payee']):
                    original_payee = transaction['payee']
                    csv_content = self.generator.generate_csv([transaction])
                    self.assertIn(original_payee, csv_content)
                    
    def test_split_transactions(self):
        """Test parsing split transactions."""
        qif_file = self.samples_dir / 'split_transactions.qif'
        self.parser.parse_file(qif_file)
        transactions = self.parser.get_transactions()
        
        # Find split transactions
        split_transactions = [
            t for t in transactions 
            if 'splits' in t
        ]
        
        for transaction in split_transactions:
            # Verify split amounts sum to total
            total_amount = float(transaction['amount'])
            split_sum = sum(
                float(split['amount']) 
                for split in transaction['splits']
            )
            self.assertAlmostEqual(total_amount, split_sum, places=2)
            
    def test_historical_data(self):
        """Test parsing historical transaction data."""
        qif_file = self.samples_dir / 'historical.qif'
        self.parser.parse_file(qif_file)
        transactions = self.parser.get_transactions()
        
        # Verify date handling across years
        dates = [t['date'] for t in transactions if 'date' in t]
        years = set(d.year for d in dates if isinstance(d, datetime))
        self.assertGreater(len(years), 1)  # Multiple years
        
        # Verify historical amount formats
        for transaction in transactions:
            if 'amount' in transaction:
                self.assertIsInstance(transaction['amount'], float) 
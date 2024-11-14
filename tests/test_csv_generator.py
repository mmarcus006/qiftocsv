import csv
from io import StringIO
from datetime import datetime
from src.core.csv_generator import CSVGenerator
from tests.test_base import BaseTestCase

class TestCSVGenerator(BaseTestCase):
    """Test cases for CSVGenerator class."""
    
    def setUp(self):
        """Set up test case."""
        self.generator = CSVGenerator()
        self.sample_transaction = {
            'date': datetime(2024, 1, 15),
            'amount': -1000.00,
            'payee': 'Test Payee',
            'memo': 'Test Memo',
            'category': 'Test Category',
            'cleared': 'X',
            'reference': '1001'
        }
        
    def test_valid_generation(self):
        """Test CSV generation with valid transaction data."""
        transactions = [self.sample_transaction]
        csv_content = self.generator.generate_csv(transactions)
        
        # Parse generated CSV
        reader = csv.DictReader(StringIO(csv_content))
        rows = list(reader)
        
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['date'], '2024-01-15')
        self.assertEqual(rows[0]['amount'], '-1000.00')
        self.assertEqual(rows[0]['payee'], 'Test Payee')
        
    def test_empty_transactions(self):
        """Test handling of empty transaction lists."""
        with self.assertRaises(ValueError):
            self.generator.generate_csv([])
            
    def test_missing_fields(self):
        """Test handling of missing fields."""
        transaction = {'date': datetime(2024, 1, 15)}
        csv_content = self.generator.generate_csv([transaction])
        
        reader = csv.DictReader(StringIO(csv_content))
        row = next(reader)
        
        for field in self.generator.fieldnames:
            self.assertIn(field, row)
            if field != 'date':
                self.assertEqual(row[field], '')
                
    def test_special_characters(self):
        """Test handling of special characters."""
        transaction = {
            'date': datetime(2024, 1, 15),
            'payee': 'Special & Chars © ®',
            'memo': 'Memo with émojis 🎉'
        }
        
        csv_content = self.generator.generate_csv([transaction])
        reader = csv.DictReader(StringIO(csv_content))
        row = next(reader)
        
        self.assertEqual(row['payee'], 'Special & Chars © ®')
        self.assertEqual(row['memo'], 'Memo with émojis 🎉') 
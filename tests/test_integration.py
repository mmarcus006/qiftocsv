from src.core.qif_parser import QIFParser
from src.core.csv_generator import CSVGenerator
from tests.test_base import BaseTestCase

class TestIntegration(BaseTestCase):
    """Integration tests for QIF to CSV conversion."""
    
    def setUp(self):
        """Set up test case."""
        self.parser = QIFParser()
        self.generator = CSVGenerator()
        
    def test_end_to_end_conversion(self):
        """Test complete conversion process from QIF to CSV."""
        # Create sample QIF file
        qif_content = "\n".join([
            "!Type:Bank",
            "D01/15/2024",
            "T-1000.00",
            "PTest Payee",
            "MTest Memo",
            "LTest Category",
            "CX",
            "N1001",
            "^"
        ])
        qif_file = self.create_test_file(qif_content, "test.qif")
        
        # Parse QIF file
        self.parser.parse_file(qif_file)
        transactions = self.parser.get_transactions()
        
        # Generate CSV
        csv_content = self.generator.generate_csv(transactions)
        csv_file = self.test_dir / "output.csv"
        
        # Save and verify CSV
        with open(csv_file, 'w', encoding='utf-8') as f:
            f.write(csv_content)
            
        self.assertTrue(csv_file.exists())
        self.assertTrue(csv_file.stat().st_size > 0)
        
        # Verify CSV content
        with open(csv_file, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("Test Payee", content)
            self.assertIn("Test Memo", content)
            self.assertIn("-1000.00", content)
            
    def test_large_file_handling(self):
        """Test handling of large QIF files."""
        # Create a large QIF file (multiple transactions)
        transactions = []
        transactions.append("!Type:Bank")  # Add header first
        
        for i in range(1000):  # 1000 transactions
            transactions.extend([
                f"D01/{i%28+1}/2024",
                f"T-{i+1}.00",
                f"PPayee {i}",
                f"MMemo {i}",
                "^"
            ])
            
        qif_content = "\n".join(transactions)
        qif_file = self.create_test_file(qif_content, "large.qif")
        
        # Process file
        self.parser.parse_file(qif_file)
        transactions = self.parser.get_transactions()
        
        # Verify transaction count
        self.assertEqual(len(transactions), 1000)
        
        # Generate and verify CSV
        csv_content = self.generator.generate_csv(transactions)
        self.assertGreater(len(csv_content), 1000)  # Reasonable size check 
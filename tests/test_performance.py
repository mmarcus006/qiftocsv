import time
from pathlib import Path
from src.core.qif_parser import QIFParser
from src.core.csv_generator import CSVGenerator
from .test_base import BaseTestCase

class TestPerformance(BaseTestCase):
    """Performance tests for QIF to CSV conversion."""
    
    def setUp(self):
        """Set up test case."""
        self.parser = QIFParser()
        self.generator = CSVGenerator()
        
    def test_parsing_performance(self):
        """Test QIF parsing performance with different file sizes."""
        file_sizes = [100, 1000, 5000]  # Number of transactions
        
        for size in file_sizes:
            # Create test file
            transactions = []
            for i in range(size):
                transactions.extend([
                    f"D01/{i%28+1}/2024",
                    f"T-{i+1}.00",
                    f"PPayee {i}",
                    f"MMemo {i}",
                    "^"
                ])
                
            qif_content = "!Type:Bank\n" + "\n".join(transactions)
            qif_file = self.create_test_file(qif_content, f"perf_{size}.qif")
            
            # Measure parsing time
            start_time = time.time()
            self.parser.parse_file(qif_file)
            parse_time = time.time() - start_time
            
            # Assert reasonable performance (adjust thresholds as needed)
            self.assertLess(parse_time, size * 0.001)  # 1ms per transaction
            
    def test_csv_generation_performance(self):
        """Test CSV generation performance with different dataset sizes."""
        dataset_sizes = [100, 1000, 5000]
        
        for size in dataset_sizes:
            # Create test transactions
            transactions = [
                {
                    'date': f"2024-01-{i%28+1}",
                    'amount': f"-{i+1}.00",
                    'payee': f"Payee {i}",
                    'memo': f"Memo {i}"
                }
                for i in range(size)
            ]
            
            # Measure generation time
            start_time = time.time()
            self.generator.generate_csv(transactions)
            generate_time = time.time() - start_time
            
            # Assert reasonable performance
            self.assertLess(generate_time, size * 0.001)  # 1ms per transaction 
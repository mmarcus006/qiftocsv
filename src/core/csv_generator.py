import csv
from typing import List, Dict
import io

class CSVGenerator:
    def __init__(self):
        self.fieldnames = [
            'date', 'amount', 'payee', 'memo', 
            'category', 'cleared', 'reference'
        ]
    
    def generate_csv(self, transactions: List[Dict]) -> str:
        """Generate CSV content from transactions."""
        output = io.StringIO()
        
        writer = csv.DictWriter(
            output,
            fieldnames=self.fieldnames,
            extrasaction='ignore'
        )
        
        writer.writeheader()
        
        for transaction in transactions:
            # Format date if it's a datetime object
            if 'date' in transaction and hasattr(transaction['date'], 'strftime'):
                transaction['date'] = transaction['date'].strftime('%Y-%m-%d')
            
            # Ensure all fields exist
            row = {field: transaction.get(field, '') for field in self.fieldnames}
            writer.writerow(row)
        
        return output.getvalue()
    
    def save_csv(self, transactions: List[Dict], filepath: str) -> bool:
        """Save transactions to a CSV file."""
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=self.fieldnames,
                    extrasaction='ignore'
                )
                
                writer.writeheader()
                
                for transaction in transactions:
                    # Format date if it's a datetime object
                    if 'date' in transaction and hasattr(transaction['date'], 'strftime'):
                        transaction['date'] = transaction['date'].strftime('%Y-%m-%d')
                    
                    # Ensure all fields exist
                    row = {field: transaction.get(field, '') for field in self.fieldnames}
                    writer.writerow(row)
                    
            return True
            
        except Exception as e:
            raise Exception(f"Error saving CSV file: {str(e)}") 
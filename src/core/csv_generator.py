import csv
from typing import List, Dict, Optional
from pathlib import Path
import io
from datetime import datetime

class CSVGenerator:
    """Generator for CSV files from transaction data."""
    
    FIELDNAMES = [
        'date', 'amount', 'payee', 'memo', 
        'category', 'cleared', 'reference'
    ]
    
    def __init__(self):
        self.fieldnames = self.FIELDNAMES
    
    def generate_csv(self, transactions: List[Dict], delimiter: str = ',') -> str:
        """
        Generate CSV content from transactions.
        
        Args:
            transactions: List of transaction dictionaries
            delimiter: CSV delimiter character
            
        Returns:
            str: Generated CSV content
            
        Raises:
            ValueError: If transactions data is invalid
        """
        if not transactions:
            raise ValueError("No transactions to convert")
            
        output = io.StringIO()
        
        writer = csv.DictWriter(
            output,
            fieldnames=self.fieldnames,
            delimiter=delimiter,
            extrasaction='ignore',
            quoting=csv.QUOTE_MINIMAL
        )
        
        writer.writeheader()
        
        for transaction in transactions:
            row = self._format_transaction(transaction)
            writer.writerow(row)
        
        return output.getvalue()
    
    def _format_transaction(self, transaction: Dict) -> Dict:
        """Format transaction data for CSV output."""
        formatted = {}
        
        for field in self.fieldnames:
            value = transaction.get(field, '')
            
            if field == 'date' and isinstance(value, datetime):
                formatted[field] = value.strftime('%Y-%m-%d')
            elif field == 'amount' and value:
                formatted[field] = f"{float(value):.2f}"
            else:
                formatted[field] = str(value) if value is not None else ''
                
        return formatted
    
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
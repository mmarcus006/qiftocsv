from datetime import datetime
from typing import Dict, List, Optional
import re
from pathlib import Path

class QIFParser:
    """Parser for QIF (Quicken Interchange Format) files."""
    
    DATE_FORMATS = ['%m/%d/%Y', '%m/%d/%y', '%Y-%m-%d']
    
    def __init__(self):
        self.transactions: List[Dict] = []
        self.account_type: Optional[str] = None
        
    def _parse_amount(self, value: str) -> float:
        """Parse amount string to float, handling commas."""
        try:
            # Handle empty or whitespace-only values
            if not value or value.isspace():
                return 0.0
            return float(value.replace(',', ''))
        except ValueError as e:
            raise ValueError(f"Invalid amount format: {value}") from e
    
    def parse_file(self, filepath: str | Path) -> bool:
        """Parse a QIF file and store the transactions."""
        try:
            filepath = Path(filepath)
            if not filepath.exists():
                raise FileNotFoundError(f"File not found: {filepath}")
                
            with filepath.open('r', encoding='utf-8') as file:
                content = file.read().strip()
                
            if not content:
                raise ValueError("Empty QIF file")
                
            # Split into sections by account type
            sections = content.split('!Type:')
            if len(sections) < 2:
                raise ValueError("Invalid QIF file format")
                
            # Clear previous transactions
            self.transactions.clear()
            
            # Process each section
            for section in sections[1:]:  # Skip empty first split
                if not section.strip():
                    continue
                    
                lines = section.strip().split('\n')
                if not lines:
                    continue
                    
                # Set account type from section header
                self.account_type = lines[0].strip()
                current_transaction = {}
                
                # Process remaining lines
                for line in lines[1:]:
                    if not line.strip():
                        continue
                        
                    if line.startswith('^'):
                        if current_transaction:
                            self.transactions.append(current_transaction)
                            current_transaction = {}
                        continue
                        
                    code = line[0]
                    value = line[1:].strip()
                    
                    if code == 'D':  # Date
                        for fmt in self.DATE_FORMATS:
                            try:
                                current_transaction['date'] = datetime.strptime(value, fmt)
                                break
                            except ValueError:
                                continue
                    elif code == 'T':  # Amount
                        current_transaction['amount'] = self._parse_amount(value)
                    elif code == 'P':  # Payee
                        current_transaction['payee'] = value
                    elif code == 'M':  # Memo
                        current_transaction['memo'] = value
                    elif code == 'L':  # Category
                        current_transaction['category'] = value
                    elif code == 'C':  # Cleared status
                        current_transaction['cleared'] = value
                    elif code == 'N':  # Number/Reference
                        current_transaction['reference'] = value
                        
                if current_transaction:
                    self.transactions.append(current_transaction)
                    
            return True
            
        except Exception as e:
            if isinstance(e, FileNotFoundError):
                raise
            raise ValueError(f"Error reading QIF file: {str(e)}")
    
    def get_transactions(self) -> List[Dict]:
        """Return the parsed transactions."""
        return self.transactions
    
    def get_account_type(self) -> str:
        """Return the account type."""
        return self.account_type
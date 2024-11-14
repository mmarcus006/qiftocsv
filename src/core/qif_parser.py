from datetime import datetime
from typing import Dict, List, Optional
import re

class QIFParser:
    def __init__(self):
        self.transactions: List[Dict] = []
        self.account_type: Optional[str] = None
        
    def parse_file(self, filepath: str) -> bool:
        """Parse a QIF file and store the transactions."""
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read().strip()
                
            # Split into header and transactions
            header, *transactions = content.split('\n^\n')
            
            # Parse header for account type
            self.account_type = self._parse_header(header)
            
            # Parse each transaction
            for transaction in transactions:
                if transaction.strip():
                    parsed_transaction = self._parse_transaction(transaction)
                    if parsed_transaction:
                        self.transactions.append(parsed_transaction)
                        
            return True
            
        except Exception as e:
            raise Exception(f"Error parsing QIF file: {str(e)}")
    
    def _parse_header(self, header: str) -> str:
        """Parse the QIF header to determine account type."""
        header_line = header.split('\n')[0]
        if header_line.startswith('!Type:'):
            return header_line[6:].strip()
        return 'Unknown'
    
    def _parse_transaction(self, transaction: str) -> Dict:
        """Parse a single transaction block into a dictionary."""
        lines = transaction.strip().split('\n')
        transaction_data = {}
        
        for line in lines:
            if not line:
                continue
                
            identifier = line[0]
            value = line[1:].strip()
            
            if identifier == 'D':  # Date
                try:
                    # Handle different date formats
                    date_formats = ['%m/%d/%Y', '%m/%d/%y', '%Y-%m-%d']
                    for fmt in date_formats:
                        try:
                            transaction_data['date'] = datetime.strptime(value, fmt)
                            break
                        except ValueError:
                            continue
                except ValueError:
                    transaction_data['date'] = value
            elif identifier == 'T':  # Amount
                try:
                    transaction_data['amount'] = float(value.replace(',', ''))
                except ValueError:
                    transaction_data['amount'] = value
            elif identifier == 'P':  # Payee
                transaction_data['payee'] = value
            elif identifier == 'M':  # Memo
                transaction_data['memo'] = value
            elif identifier == 'L':  # Category
                transaction_data['category'] = value
            elif identifier == 'C':  # Cleared status
                transaction_data['cleared'] = value
            elif identifier == 'N':  # Number (check/reference)
                transaction_data['reference'] = value
                
        return transaction_data
    
    def get_transactions(self) -> List[Dict]:
        """Return the parsed transactions."""
        return self.transactions
    
    def get_account_type(self) -> str:
        """Return the account type."""
        return self.account_type
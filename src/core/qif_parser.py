from datetime import datetime
from typing import Dict, List, Optional, Union
import re
from pathlib import Path

class QIFParserError(Exception):
    """Base exception class for QIF parser errors"""
    pass

class QIFParser:
    """Parser for QIF (Quicken Interchange Format) files."""
    
    INVESTMENT_TYPES = {'Buy', 'Sell', 'ShrsIn', 'ShrsOut', 'Div', 'IntInc'}
    
    def __init__(self):
        self.reset()
        
    def reset(self):
        """Reset parser state"""
        self.transactions: List[Dict] = []
        self.account_type: Optional[str] = None
        self.is_investment_account: bool = False
        
    def _parse_date(self, value: str) -> datetime:
        """Parse QIF date format to datetime object."""
        try:
            # Handle the specific format from the sample: "M/ D'YY"
            value = value.replace("'", "/20")  # Convert '24 to /2024
            value = value.replace(" ", "")     # Remove any spaces
            
            month, day, year = value.split("/")
            return datetime(int(year), int(month), int(day))
            
        except (ValueError, IndexError) as e:
            raise ValueError(f"Invalid date format: {value}. Expected format: M/D'YY") from e
            
    def _parse_amount(self, value: str) -> float:
        """Parse amount string to float, handling commas."""
        try:
            return float(value.replace(',', ''))
        except ValueError as e:
            raise ValueError(f"Invalid amount format: {value}. Expected numeric value.") from e
            
    def _parse_investment_line(self, code: str, value: str, current_transaction: Dict):
        """Parse investment-specific QIF fields."""
        if code == 'N':  # Transaction type
            current_transaction['type'] = value
        elif code == 'Y':  # Security name
            current_transaction['security'] = value
        elif code == 'I':  # Price
            current_transaction['price'] = self._parse_amount(value)
        elif code == 'Q':  # Quantity
            current_transaction['quantity'] = self._parse_amount(value)
        elif code == '$':  # Amount (investment)
            current_transaction['amount'] = self._parse_amount(value)
            
    def _parse_line(self, code: str, value: str, current_transaction: Dict):
        """Parse a single line of QIF data."""
        try:
            if code == 'D':  # Date
                current_transaction['date'] = self._parse_date(value)
            elif code == 'T':  # Amount
                current_transaction['amount'] = self._parse_amount(value)
            elif code == 'U':  # Amount (alternate)
                current_transaction['amount'] = self._parse_amount(value)
            elif code == 'P':  # Payee
                current_transaction['payee'] = value
            elif code == 'L':  # Category
                current_transaction['category'] = value
            elif code == 'M':  # Memo
                current_transaction['memo'] = value
            elif code == 'C':  # Cleared status
                current_transaction['cleared'] = value
                
            # Handle investment-specific fields if this is an investment account
            if self.is_investment_account:
                self._parse_investment_line(code, value, current_transaction)
                
        except ValueError as e:
            raise QIFParserError(f"Error parsing line with code '{code}': {str(e)}")
            
    def parse_file(self, filepath: Union[str, Path]) -> bool:
        """Parse QIF file and store transactions."""
        self.reset()  # Reset parser state
        
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                current_transaction = {}
                
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                        
                    if line.startswith('!Type:'):
                        self.account_type = line[6:]
                        self.is_investment_account = self.account_type == 'Invst'
                        continue
                        
                    if line == '^':
                        if current_transaction:
                            # For investment accounts, amount can be calculated from quantity * price
                            if self.is_investment_account and 'amount' not in current_transaction:
                                if 'quantity' in current_transaction and 'price' in current_transaction:
                                    current_transaction['amount'] = (
                                        current_transaction['quantity'] * current_transaction['price']
                                    )
                                    
                            # Validate required fields
                            if 'date' not in current_transaction:
                                raise QIFParserError("Transaction missing required date field")
                            if 'amount' not in current_transaction:
                                raise QIFParserError("Transaction missing required amount field")
                                
                            self.transactions.append(current_transaction)
                            current_transaction = {}
                        continue
                        
                    if len(line) >= 2:
                        code = line[0]
                        value = line[1:].strip()
                        self._parse_line(code, value, current_transaction)
                
                # Add last transaction if exists
                if current_transaction:
                    self.transactions.append(current_transaction)
                    
                if not self.transactions:
                    raise ValueError("No valid transactions found in file")
                    
                return True
                
        except FileNotFoundError as e:
            raise FileNotFoundError(
                f"QIF file not found: {filepath}. Please verify the file path."
            ) from e
        except PermissionError as e:
            raise PermissionError(
                f"Permission denied accessing file: {filepath}. "
                "Please check file permissions."
            ) from e
        except ValueError as e:
            raise ValueError(str(e)) from e
        except Exception as e:
            raise QIFParserError(f"Error parsing QIF file: {str(e)}") from e
            
    def get_transactions(self) -> List[Dict]:
        """Return list of parsed transactions."""
        return self.transactions
        
    def get_account_type(self) -> Optional[str]:
        """Return account type from QIF file."""
        return self.account_type
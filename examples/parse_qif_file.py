from pathlib import Path
from src.core.qif_parser import QIFParser
from pprint import pprint
from datetime import datetime

def format_amount(amount):
    """Format amount with commas for thousands"""
    return f"${amount:,.2f}"

def main():
    # Initialize parser
    parser = QIFParser()
    
    # Get sample file
    samples_dir = Path(__file__).parent.parent / 'samples'
    filepath = samples_dir / '5383_Investment_TransactionsOnly.QIF'
    
    print(f"\nParsing {filepath.name}...")
    
    try:
        parser.parse_file(filepath)
        
        print(f"\nAccount Type: {parser.get_account_type()}")
        transactions = parser.get_transactions()
        print(f"Number of transactions: {len(transactions)}")
        
        # Calculate some statistics
        total_debits = sum(t['amount'] for t in transactions if t['amount'] < 0)
        total_credits = sum(t['amount'] for t in transactions if t['amount'] > 0)
        
        print(f"\nSummary:")
        print(f"Total Credits: {format_amount(total_credits)}")
        print(f"Total Debits: {format_amount(total_debits)}")
        print(f"Net Amount: {format_amount(total_credits + total_debits)}")
        
        # Print first 3 transactions as example
        print("\nFirst 3 transactions:")
        for trans in transactions[:3]:
            print("\nTransaction:")
            print(f"Date: {trans['date'].strftime('%m/%d/%Y')}")
            print(f"Amount: {format_amount(trans['amount'])}")
            print(f"Payee: {trans.get('payee', 'N/A')}")
            if 'category' in trans:
                print(f"Category: {trans['category']}")
            if 'memo' in trans:
                print(f"Memo: {trans['memo']}")
                
        # Print some category statistics
        categories = {}
        for trans in transactions:
            if 'category' in trans:
                cat = trans['category']
                if cat not in categories:
                    categories[cat] = {'count': 0, 'total': 0}
                categories[cat]['count'] += 1
                categories[cat]['total'] += trans['amount']
        
        print("\nTop Categories by Transaction Count:")
        sorted_cats = sorted(categories.items(), 
                           key=lambda x: x[1]['count'], 
                           reverse=True)[:5]
        for cat, stats in sorted_cats:
            print(f"{cat}: {stats['count']} transactions, "
                  f"Total: {format_amount(stats['total'])}")
                
    except Exception as e:
        print(f"Error parsing file: {str(e)}")

if __name__ == '__main__':
    main() 
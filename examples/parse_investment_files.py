from pathlib import Path
from src.core.qif_parser import QIFParser
from pprint import pprint

def main():
    # Initialize parser
    parser = QIFParser()
    
    # Get sample files
    samples_dir = Path(__file__).parent.parent / 'samples'
    files = [
        '5383_Investment_TransactionsOnly.txt',
        '8007_Investment_TransactionsOnly.txt'
    ]
    
    # Parse each file
    for filename in files:
        filepath = samples_dir / filename
        print(f"\nParsing {filename}...")
        
        try:
            parser.parse_file(filepath)
            
            print(f"Account Type: {parser.get_account_type()}")
            print(f"Number of transactions: {len(parser.get_transactions())}")
            
            # Print first 3 transactions as example
            print("\nFirst 3 transactions:")
            for trans in parser.get_transactions()[:3]:
                pprint(trans)
                
        except Exception as e:
            print(f"Error parsing {filename}: {str(e)}")

if __name__ == '__main__':
    main() 
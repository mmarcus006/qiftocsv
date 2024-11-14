from pathlib import Path
import shutil

def create_sample_files():
    """Create sample QIF files for testing."""
    samples_dir = Path(__file__).parent.parent / 'samples'
    samples_dir.mkdir(exist_ok=True)
    
    # Create Quicken 2020 sample
    quicken_2020 = samples_dir / 'quicken_2020.qif'
    quicken_2020.write_text("""!Type:Bank
D01/15/2024
T-1000.00
PTest Payee
MTest Memo
^""", encoding='utf-8')
    
    # Create investment sample
    investments = samples_dir / 'investments.qif'
    investments.write_text("""!Type:Invst
D01/15/2024
NBuy
YAAPL
I15.00
Q10
T150.00
^""", encoding='utf-8')
    
    # Create international sample
    international = samples_dir / 'international.qif'
    international.write_text("""!Type:Bank
D01/15/2024
T-1000.00
PTest Café
MTest Mémo
^""", encoding='utf-8')

if __name__ == '__main__':
    create_sample_files() 
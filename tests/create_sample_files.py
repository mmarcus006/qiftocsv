from pathlib import Path
import shutil

def create_sample_files():
    """Create sample QIF files for testing."""
    samples_dir = Path(__file__).parent.parent / 'samples'
    samples_dir.mkdir(exist_ok=True)
    
    # Create sample files
    files = {
        'quicken_2020.qif': """!Type:Bank
D01/15/2024
T-1000.00
PTest Payee
MTest Memo
^""",
        'investments.qif': """!Type:Invst
D01/15/2024
NBuy
YAAPL
I15.00
Q10
T150.00
^""",
        'international.qif': """!Type:Bank
D01/15/2024
T-1000.00
PTest Café
MTest Mémo
^""",
        'historical.qif': """!Type:Bank
D01/15/2023
T-1000.00
PHistorical Test
^
D12/15/2022
T-2000.00
PCurrent Test
^""",
        'split_transactions.qif': """!Type:Bank
D01/15/2024
T-1500.00
PSplit Test
SCategory 1
$-1000.00
SCategory 2
$-500.00
^""",
        'multi_account.qif': """!Type:Bank
D01/15/2024
T-1000.00
PBank Transaction
LBank Category
^
!Type:CCard
D01/15/2024
T-500.00
PCredit Card Transaction
LCredit Card Category
^
!Type:Invst
D01/15/2024
T-2000.00
PInvestment Transaction
LInvestment Category
^""",
        '5383_Investment_TransactionsOnly.txt': """!Type:Invst
D01/15/2024
NBuy
YAAPL
I150.00
Q10
T-1500.00
^
D01/16/2024
NSell
YAAPL
I160.00
Q5
T800.00
^""",
        '5383_Investment_AllExports.txt': """!Type:Invst
D01/15/2024
NBuy
YAAPL
I150.00
Q10
T-1500.00
MBuy Transaction
^
D01/16/2024
NSell
YAAPL
I160.00
Q5
T800.00
MSell Transaction
^"""
    }
    
    for filename, content in files.items():
        filepath = samples_dir / filename
        filepath.write_text(content, encoding='utf-8')

if __name__ == '__main__':
    create_sample_files() 
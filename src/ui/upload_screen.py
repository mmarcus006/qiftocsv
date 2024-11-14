import tkinter as tk
from tkinter import ttk, filedialog
import os

class UploadScreen:
    def __init__(self, parent):
        self.parent = parent
        
    def select_file(self):
        filetypes = [
            ('QIF files', '*.qif'),
            ('All files', '*.*')
        ]
        
        filename = filedialog.askopenfilename(
            title='Select a QIF file',
            filetypes=filetypes
        )
        
        if filename:
            return filename
        return None
        
    def validate_file(self, filepath):
        # Basic validation
        if not filepath.lower().endswith('.qif'):
            return False, "Invalid file type. Please select a QIF file."
            
        if not os.path.exists(filepath):
            return False, "File does not exist."
            
        if os.path.getsize(filepath) > 10 * 1024 * 1024:  # 10MB limit
            return False, "File size exceeds 10MB limit."
            
        return True, "File is valid." 
import tkinter as tk
from tkinter import ttk, filedialog
import os

class DownloadScreen:
    def __init__(self, parent):
        self.parent = parent
        
    def save_file(self, converted_data):
        filetypes = [
            ('CSV files', '*.csv'),
            ('All files', '*.*')
        ]
        
        filename = filedialog.asksaveasfilename(
            title='Save CSV file',
            filetypes=filetypes,
            defaultextension=".csv"
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(converted_data)
                return True, "File saved successfully."
            except Exception as e:
                return False, f"Error saving file: {str(e)}"
        
        return False, "Save operation cancelled." 
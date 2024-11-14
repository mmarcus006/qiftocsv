import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import threading
from typing import Optional
from src.core.qif_parser import QIFParser
from src.core.csv_generator import CSVGenerator
from src.ui.upload_screen import UploadScreen
from src.ui.download_screen import DownloadScreen

class MainWindow:
    """Main window for the QIF to CSV converter application."""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.setup_window()
        self.setup_ui()
        self.initialize_components()
        
    def setup_window(self):
        """Configure the main window."""
        self.root.title("QIF to CSV Converter")
        self.root.geometry("800x600")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
    def setup_ui(self):
        """Set up the user interface components."""
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure main frame grid
        self.main_frame.grid_columnconfigure(0, weight=1)
        for i in range(5):
            self.main_frame.grid_rowconfigure(i, weight=1)
            
        self._create_widgets()
        
    def _create_widgets(self):
        """Create and configure UI widgets."""
        # Title
        self.title_label = ttk.Label(
            self.main_frame,
            text="QIF to CSV Converter",
            font=('Helvetica', 24)
        )
        self.title_label.grid(row=0, column=0, pady=20)
        
        # Buttons and progress indicators
        self._create_control_widgets()
        
    def _create_control_widgets(self):
        """Create control widgets (buttons, progress bar, etc.)."""
        # Upload button
        self.upload_btn = ttk.Button(
            self.main_frame,
            text="Upload QIF File",
            command=self._handle_upload
        )
        self.upload_btn.grid(row=1, column=0, pady=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            self.main_frame,
            orient="horizontal",
            length=300,
            mode="determinate"
        )
        self.progress.grid(row=2, column=0, pady=10)
        
        # Status label
        self.status_label = ttk.Label(
            self.main_frame,
            text="Ready to convert files",
            font=('Helvetica', 10)
        )
        self.status_label.grid(row=3, column=0, pady=10)
        
        # Download button
        self.download_btn = ttk.Button(
            self.main_frame,
            text="Download CSV",
            command=self._handle_download,
            state="disabled"
        )
        self.download_btn.grid(row=4, column=0, pady=10)
        
    def initialize_components(self):
        """Initialize components and set up event handlers."""
        self.upload_screen = UploadScreen(self)
        self.download_screen = DownloadScreen(self)
        self.qif_parser = QIFParser()
        self.csv_generator = CSVGenerator()
        self.current_transactions = None
        
    def _handle_upload(self):
        """Handle file upload and conversion."""
        filename = self.upload_screen.select_file()
        if not filename:
            return
            
        # Validate file
        is_valid, message = self.upload_screen.validate_file(filename)
        if not is_valid:
            self.status_label.config(text=message)
            return
            
        try:
            # Update UI
            self.status_label.config(text="Converting file...")
            self.progress['value'] = 0
            self.root.update()
            
            # Parse QIF file
            self.qif_parser.parse_file(filename)
            self.current_transactions = self.qif_parser.get_transactions()
            
            # Update UI
            self.progress['value'] = 100
            self.status_label.config(text="Conversion complete!")
            self.download_btn['state'] = 'normal'
            
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")
            self.progress['value'] = 0
            
    def _handle_download(self):
        """Handle CSV file download."""
        if not self.current_transactions:
            self.status_label.config(text="No data to download.")
            return
            
        try:
            # Generate CSV content
            csv_content = self.csv_generator.generate_csv(self.current_transactions)
            
            # Save file
            success, message = self.download_screen.save_file(csv_content)
            self.status_label.config(text=message)
            
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}") 
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("QIF to CSV Converter")
        self.root.geometry("800x600")
        
        # Configure grid weight
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure main frame grid weights
        self.main_frame.grid_columnconfigure(0, weight=1)
        for i in range(5):
            self.main_frame.grid_rowconfigure(i, weight=1)
            
        # Title
        title_label = ttk.Label(
            self.main_frame, 
            text="QIF to CSV Converter",
            font=('Helvetica', 24)
        )
        title_label.grid(row=0, column=0, pady=20)
        
        # Upload button
        self.upload_btn = ttk.Button(
            self.main_frame,
            text="Upload QIF File",
            command=self.upload_file
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
        
        # Download button (initially disabled)
        self.download_btn = ttk.Button(
            self.main_frame,
            text="Download CSV",
            command=self.download_file,
            state="disabled"
        )
        self.download_btn.grid(row=4, column=0, pady=10)

    def upload_file(self):
        # Placeholder for upload functionality
        self.status_label.config(text="Upload functionality coming soon...")
        
    def download_file(self):
        # Placeholder for download functionality
        self.status_label.config(text="Download functionality coming soon...") 
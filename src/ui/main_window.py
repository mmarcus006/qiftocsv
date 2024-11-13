import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.setup_ui()

    def setup_ui(self):
        # Configure main window
        self.master.geometry("600x400")
        self.master.minsize(500, 300)

        # Create main frame
        self.main_frame = ttk.Frame(self.master, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create and configure grid
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        # Add upload button
        self.upload_btn = ttk.Button(
            self.main_frame, 
            text="Upload QIF File",
            command=self.upload_file
        )
        self.upload_btn.grid(row=0, column=0, pady=20)

        # Add progress bar
        self.progress = ttk.Progressbar(
            self.main_frame,
            orient=tk.HORIZONTAL,
            length=300,
            mode='determinate'
        )
        self.progress.grid(row=1, column=0, pady=20)

        # Add status label
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(
            self.main_frame,
            textvariable=self.status_var
        )
        self.status_label.grid(row=2, column=0, pady=10)

        # Add download button (initially disabled)
        self.download_btn = ttk.Button(
            self.main_frame,
            text="Download CSV",
            command=self.download_file,
            state='disabled'
        )
        self.download_btn.grid(row=3, column=0, pady=20)

    def upload_file(self):
        filename = filedialog.askopenfilename(
            title="Select QIF File",
            filetypes=[("QIF files", "*.qif"), ("All files", "*.*")]
        )
        if filename:
            self.status_var.set(f"Selected file: {filename}")
            # TODO: Implement file processing
            self.download_btn.state(['!disabled'])

    def download_file(self):
        filename = filedialog.asksaveasfilename(
            title="Save CSV File",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.status_var.set(f"Saved to: {filename}") 
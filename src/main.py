import tkinter as tk
from ui.main_window import MainWindow

def main():
    root = tk.Tk()
    root.title("QIF to CSV Converter")
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main() 
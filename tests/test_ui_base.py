import tkinter as tk
from tests.test_base import BaseTestCase

class UITestCase(BaseTestCase):
    """Base class for UI testing."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test resources and root window."""
        super().setUpClass()
        cls.root = tk.Tk()
        cls.root.withdraw()  # Hide the root window during tests
        
    @classmethod
    def tearDownClass(cls):
        """Clean up test resources and destroy root window."""
        cls.root.destroy()
        super().tearDownClass()
        
    def wait_for(self, milliseconds: int):
        """Wait for specified milliseconds while processing events."""
        self.root.after(milliseconds)
        self.root.update() 
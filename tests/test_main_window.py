from src.ui.main_window import MainWindow
from tests.test_ui_base import UITestCase

class TestMainWindow(UITestCase):
    """Test cases for MainWindow class."""
    
    def setUp(self):
        """Set up test case."""
        self.window = MainWindow(self.root)
        
    def test_initial_state(self):
        """Test initial window state."""
        # Check window title
        self.assertEqual(self.root.title(), "QIF to CSV Converter")
        
        # Check initial button states
        self.assertEqual(
            str(self.window.download_btn['state']),
            'disabled'
        )
        self.assertEqual(
            str(self.window.upload_btn['state']),
            'normal'
        )
        
        # Check initial progress and status
        self.assertEqual(self.window.progress['value'], 0)
        self.assertEqual(
            self.window.status_label['text'],
            "Ready to convert files"
        )
        
    def test_file_upload_workflow(self):
        """Test the file upload workflow."""
        # Create valid QIF file
        qif_file = self.create_sample_qif()
        
        # Mock file selection
        self.window.upload_screen.select_file = lambda: str(qif_file)
        
        # Trigger upload
        self.window._handle_upload()
        self.wait_for(100)  # Wait for processing
        
        # Check button states
        self.assertEqual(
            str(self.window.download_btn['state']),
            'normal'
        )
        
    def test_invalid_file_upload(self):
        """Test handling of invalid file upload."""
        # Create an invalid file
        invalid_file = self.create_test_file("invalid content", "invalid.qif")
        
        # Mock file selection
        self.window.upload_screen.select_file = lambda: str(invalid_file)
        
        # Reset progress bar
        self.window.progress['value'] = 0
        
        # Trigger upload
        self.window._handle_upload()
        self.wait_for(100)  # Wait for processing
        
        # Check error handling
        self.assertEqual(self.window.progress['value'], 0)
        self.assertTrue(
            self.window.status_label['text'].startswith("Error")
        ) 
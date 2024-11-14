import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import time

def test_file_upload_and_conversion(selenium_driver, streamlit_server):
    """Test file upload and conversion functionality"""
    driver = selenium_driver
    
    # Navigate to the Streamlit app
    driver.get("http://localhost:8501")
    
    # Wait for the file uploader to be present
    wait = WebDriverWait(driver, 10)
    uploader = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))
    
    # Upload a sample QIF file
    sample_file = Path(__file__).parent / "samples" / "test_investment.qif"
    if not sample_file.exists():
        sample_file.parent.mkdir(parents=True, exist_ok=True)
        with open(sample_file, "w") as f:
            f.write("!Type:Invst\nD01/01/2020\nN1000.00\nYBUY\n^\n")
    
    uploader.send_keys(str(sample_file.absolute()))
    
    # Wait for success message
    success_msg = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//div[contains(text(), 'File converted successfully!')]")
    ))
    assert "File converted successfully!" in success_msg.text

def test_error_handling_invalid_file(selenium_driver, streamlit_server):
    """Test error handling for invalid files"""
    driver = selenium_driver
    
    # Navigate to the Streamlit app
    driver.get("http://localhost:8501")
    
    # Wait for the file uploader
    wait = WebDriverWait(driver, 10)
    uploader = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))
    
    # Create and upload invalid file
    invalid_file = Path(__file__).parent / "samples" / "invalid.qif"
    with open(invalid_file, "w") as f:
        f.write("Invalid content")
    
    uploader.send_keys(str(invalid_file.absolute()))
    
    # Wait for error message
    error_msg = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//div[contains(text(), 'An error occurred:')]")
    ))
    assert "An error occurred:" in error_msg.text
    
    # Cleanup
    invalid_file.unlink()
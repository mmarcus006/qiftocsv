import pytest
import os
import signal
import subprocess
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def pytest_configure(config):
    """Configure pytest environment."""
    # Add custom markers
    config.addinivalue_line(
        "markers", "ui: mark test as a UI test"
    )

@pytest.fixture(scope="session")
def streamlit_server():
    """Start Streamlit server for testing and clean up after"""
    # Start Streamlit server
    process = subprocess.Popen(
        ["streamlit", "run", str(Path(__file__).parent.parent / "src" / "main.py")],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )
    
    # Wait for server to start
    time.sleep(5)
    
    yield process
    
    try:
        # Cleanup: Kill the Streamlit server
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    except Exception as e:
        print(f"Error cleaning up Streamlit server: {e}")

@pytest.fixture(scope="session")
def selenium_driver():
    """Configure and provide Selenium WebDriver"""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    try:
        # Use webdriver_manager to handle driver installation
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        yield driver
    finally:
        if 'driver' in locals():
            driver.quit() 
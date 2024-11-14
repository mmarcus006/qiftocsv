import pytest
import os
import signal
import subprocess
import time
from pathlib import Path

@pytest.fixture(scope="session")
def streamlit_server():
    """Start Streamlit server for testing and clean up after"""
    # Start Streamlit server
    process = subprocess.Popen(
        ["streamlit", "run", str(Path(__file__).parent.parent / "src" / "main.py")],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid  # Allow killing the process group
    )
    
    # Wait for server to start
    time.sleep(5)
    
    yield process
    
    # Cleanup: Kill the Streamlit server
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)

@pytest.fixture(scope="session")
def selenium_driver():
    """Configure and provide Selenium WebDriver"""
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit() 
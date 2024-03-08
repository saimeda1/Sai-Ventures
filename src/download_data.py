import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up the Selenium Chrome Driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

def download_stock_data(ticker):
    # Navigate to the NASDAQ historical data page for the given ticker
    url = f"https://www.nasdaq.com/market-activity/stocks/{ticker}/historical"
    driver.get(url)

    # Wait for the page to load completely
    time.sleep(5)

    # Find the "Download Data" link or button (this might require adjusting based on the actual element)
    try:
        download_link = driver.find_element(By.LINK_TEXT, "Download Data")
        download_link.click()
        
        # You might need to wait for the download to start
        time.sleep(10)
    finally:
        driver.quit()

# Example usage
download_stock_data('aapl')

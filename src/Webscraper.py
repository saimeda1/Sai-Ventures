from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
from sqlalchemy import create_engine

# Configure webdriver
driver = webdriver.Chrome(executable_path='/path/to/chromedriver')

# URL for historical data
url = 'https://www.nasdaq.com/market-activity/quotes/historical'

# Open the webpage
driver.get(url)

# Assume you have navigated to the appropriate page and fetched the data.
# Here, a dummy data extraction process.
data = {
    'Date': ['2021-01-01', '2021-01-02'],
    'Open': [100, 102],
    'Close': [101, 103],
    'Volume': [1500, 1600]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Store data to SQL database
engine = create_engine('sqlite:///stocks.db')
df.to_sql('historical_data', con=engine, if_exists='replace', index=False)

driver.quit()

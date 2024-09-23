import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
import pyodbc
import matplotlib.pyplot as plt

# Step 1: Function to fetch data from Nasdaq
def fetch_financial_data(ticker):
    url = f'https://www.nasdaq.com/market-activity/quotes/historical/{ticker}'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract data (you may need to adapt based on the HTML structure)
        # For simplicity, let's assume we're fetching table data for now
        table = soup.find('table')  # This needs to be adapted based on HTML structure
        df = pd.read_html(str(table))[0]  # Convert HTML table to DataFrame
        
        # Some financial measures (assuming columns are correct)
        # Extract P/E or other important measures from appropriate columns
        # Placeholder for now, should be adapted based on actual data
        return df
    else:
        print(f"Failed to retrieve data for {ticker}")
        return None

# Step 2: Function to store data in SQL Server
def store_data_in_sql(df, table_name, connection_string):
    # SQLAlchemy engine connection string
    engine = create_engine(connection_string)
    
    # Store data in SQL Server table
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)
    print(f"Data stored in table: {table_name}")

# Step 3: Function to visualize data
def visualize_data(df):
    # Example: Plot P/E ratio (a

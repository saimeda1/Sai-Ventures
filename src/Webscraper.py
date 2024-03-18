import pandas as pd
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, send_file
import selenium
import io


app = Flask(__name__)

# Web scraper for Nasdaq to get desired data on user desired stock and desired time period
@app.route('/get_stock_data', methods=['GET'])
def gatherDataNasdaq():
    ticker = request.args.get('ticker')
    length = request.args.get('length')  # This needs to be defined properly on how you want to use it

    # Initializes the page based on user selected stock output
    page = f"https://www.nasdaq.com/market-activity/stocks/{ticker}/historical"

    # Here you would need to add logic to identify the URL or API that provides the CSV file.
    # For now, we are just making a GET request to the page URL.
    response = requests.get(page)

    # Check if the request was successful
    if response.status_code == 200:
        # Logic to process the page content and extract CSV data goes here
        # Since the actual data extraction method is not provided, this part is left as a placeholder
        pass
    else:
        return f"Failed to retrieve data for ticker: {ticker}"

    # After extracting the data and converting it to a CSV format, save it into a buffer
    buffer = io.StringIO()
    # Assuming 'data' is a pandas DataFrame containing the extracted data
    pd.to_csv(buffer, index=False)
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name=f"{ticker}_data.csv", mimetype='text/csv')

if __name__ == '__main__':
    app.run(debug=True)

    
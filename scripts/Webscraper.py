import yfinance as yf
import pandas as pd
import datetime


def get_historical_data(ticker: str, years: int = 5) -> pd.DataFrame:
    """
    Downloads historical price data for the given stock ticker using yfinance.
    :param ticker: Stock ticker symbol (e.g., 'AAPL')
    :param years: Number of years of historical data to fetch.
    :return: DataFrame with historical stock prices.
    """
    end_date = datetime.datetime.today()
    start_date = end_date - datetime.timedelta(days=365 * years)
    data = yf.download(ticker, start=start_date, end=end_date)
    data.reset_index(inplace=True)
    return data


def get_multiples(ticker: str) -> dict:
    """
    Retrieves current valuation multiples and financial metrics for the given ticker.
    :param ticker: Stock ticker symbol (e.g., 'AAPL')
    :return: Dictionary of financial metrics (P/E, P/B, EV/EBITDA, etc.)
    """
    stock = yf.Ticker(ticker)
    info = stock.info
    # Extract common valuation metrics
    return {
        'trailingPE': info.get('trailingPE'),
        'forwardPE': info.get('forwardPE'),
        'priceToBook': info.get('priceToBook'),
        'enterpriseToEbitda': info.get('enterpriseToEbitda'),
        'marketCap': info.get('marketCap'),
        'enterpriseValue': info.get('enterpriseValue'),
        'sector': info.get('sector'),
        'industry': info.get('industry'),
        'shortName': info.get('shortName')
    }


if __name__ == "__main__":
    # Example usage:
    ticker = "AAPL"
    hist_data = get_historical_data(ticker)
    multiples = get_multiples(ticker)

    print("Historical Data (Head):")
    print(hist_data.head())

    print("\nValuation Multiples:")
    for key, value in multiples.items():
        print(f"{key}: {value}")

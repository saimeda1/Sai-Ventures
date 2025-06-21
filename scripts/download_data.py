import os
import pandas as pd
from Webscraper import get_historical_data, get_multiples


def save_data_to_csv(ticker: str, output_dir: str = "data"):
    """
    Fetches historical stock data and valuation multiples, then saves them to CSV files.
    :param ticker: Stock ticker symbol (e.g., 'AAPL')
    :param output_dir: Directory to save CSV files in.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Historical data
    hist_df = get_historical_data(ticker)
    hist_path = os.path.join(output_dir, f"{ticker}_historical.csv")
    hist_df.to_csv(hist_path, index=False)

    # Multiples
    multiples = get_multiples(ticker)
    multiples_df = pd.DataFrame([multiples])
    mult_path = os.path.join(output_dir, f"{ticker}_multiples.csv")
    multiples_df.to_csv(mult_path, index=False)

    print(f"Saved historical data to {hist_path}")
    print(f"Saved valuation multiples to {mult_path}")


if __name__ == "__main__":
    save_data_to_csv("AAPL")
    save_data_to_csv("MSFT")

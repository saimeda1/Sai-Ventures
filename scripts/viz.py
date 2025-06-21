import pandas as pd
import matplotlib.pyplot as plt
import os


def plot_price_history(csv_path: str):
    """
    Plot historical closing price from a CSV file.
    :param csv_path: Path to the CSV file containing historical price data.
    """
    df = pd.read_csv(csv_path, parse_dates=['Date'])
    plt.figure(figsize=(10, 5))
    plt.plot(df['Date'], df['Close'], label='Close Price')
    plt.title("Stock Price Over Time")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def display_multiples(csv_path: str):
    """
    Display valuation multiples from a CSV file.
    :param csv_path: Path to the CSV file containing multiples.
    """
    df = pd.read_csv(csv_path)
    print("\nValuation Multiples:")
    print(df.T.rename(columns={0: 'Value'}))


if __name__ == "__main__":
    ticker = "AAPL"
    base_dir = "data"
    hist_file = os.path.join(base_dir, f"{ticker}_historical.csv")
    mult_file = os.path.join(base_dir, f"{ticker}_multiples.csv")

    plot_price_history(hist_file)
    display_multiples(mult_file)


Sai‑Ventures

Sai‑Ventures is a lightweight, Python-based financial analytics tool that lets you:
• Fetch historical and real-time stock data
• Compute technical indicators (SMA, EMA, RSI, MACD, Bollinger Bands)
• Backtest trading strategies
• Visualize price series with indicator overlays
• Log trades and performance metrics
• Extend with custom strategy modules via a clean plug‑in interface

Installation
------------
1. Clone the repo:
   git clone https://github.com/saimeda1/Sai-Ventures.git
2. Create a virtual environment:
   cd Sai‑Ventures
   python3 -m venv venv
   source venv/bin/activate
3. Install dependencies:
   pip install -r requirements.txt

Configuration
-------------
Copy the sample and edit parameters as desired:
   cp config/config.example.yml config/config.yml

Example config.yml contents:
data_source:
  provider: yahoo           # or alpaca, polygon
  symbols: ["AAPL", "MSFT"]
  start_date: "2023-01-01"
  end_date: "2023-06-30"

backtest:
  initial_balance: 10000

strategy:
  module: strategies.moving_average
  class: MovingAverageStrategy
  parameters:
    fast_window: 20
    slow_window: 50

Usage
-----
Backtest mode (default):
   python run.py --backtest --config config/config.yml

Live mode (if real-time API keys are provided):
   python run.py --live --config config/config.yml

Output
------
• charts/        – PNGs of price with indicators and equity curve  
• logs/          – trade-by-trade execution logs  
• reports/       – summary statistics (total return, drawdown, Sharpe ratio)

Project structure
-----------------
Sai-Ventures/
  core/
    data.py         – data fetching and preprocessing
    strategy.py     – base Strategy class
    broker.py       – trade execution simulation
    analyzer.py     – performance metrics and plot functions
  strategies/       – example strategies  
  config/           – config templates  
  charts/           – generated figures  
  logs/             – runtime logs  
  run.py            – main entrypoint  
  requirements.txt

Adding your own strategy
------------------------
Create a file in `strategies/`, e.g. `my_strategy.py`:

```python
from core.strategy import Strategy

class MyStrategy(Strategy):
    def on_bar(self, bar):
        if self.sma(10) > self.ema(20):
            self.buy()
        elif self.position > 0:
            self.sell()

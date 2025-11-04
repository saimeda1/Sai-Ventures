# Sai Ventures (Mini Bloomberg Terminal) - Complete Setup Guide


### 1. Installation
```bash
# Clone or download the files to your project directory
mkdir sai-ventures-terminal
cd sai-ventures-terminal

# Install dependencies
pip install streamlit yfinance pandas numpy plotly requests

# Alternative: Install from requirements file
pip install -r requirements.txt
```

### 2. Run the Application
```bash
streamlit run sai_ventures_terminal_app.py
```

The application will open automatically in your browser at `http://localhost:8501`

1. **Stock Search & Analysis**
   - Search any valid stock ticker (AAPL, MSFT, GOOGL, TSLA, etc.)
   - Real-time price data and company information
   - Market cap, volume, and key metrics display

2. **Extended Time Ranges** (10 options)
   - 1 Day, 5 Days, 1 Month, 3 Months, 6 Months
   - 1 Year, 2 Years, 5 Years, 10 Years, Maximum

3. **Comprehensive Financial Multiples** (17 ratios)
   - **Valuation**: P/E, Forward P/E, PEG, P/B, P/S
   - **Enterprise Value**: EV/Revenue, EV/EBITDA
   - **Profitability**: ROE, ROA, Gross/Operating/Net Margins
   - **Dividend**: Dividend Yield, Payout Ratio
   - **Leverage**: Debt-to-Equity, Current Ratio, Quick Ratio

4. **Interactive Price Charts**
   - Candlestick charts with volume
   - Moving averages (20-day, 50-day)
   - RSI technical indicator
   - Professional Bloomberg-style dark theme

5. **Historical Multiples Analysis**
   - Compare current multiples to historical ranges
   - Percentile ranking (Undervalued/Fair/Overvalued)
   - Historical trend visualization
   - Percentile bands (25th, 50th, 75th percentiles)

6. **Advanced Analysis Tabs**
   - Current Values: Live multiple values
   - Historical Trends: Interactive charts with percentile bands
   - Percentile Analysis: Valuation assessment
   - Summary Table: Comprehensive overview

## 🎯 How to Use

### Step 1: Search Stock
- Enter any stock ticker (e.g., AAPL, MSFT, GOOGL)
- Select analysis period (1D to MAX)
- Click "Analyze" button

### Step 2: Select Multiples
- Use sidebar to select which multiples to analyze
- Choose from 5 categories: Valuation, Enterprise Value, Profitability, Dividend, Leverage
- Default selections: P/E, P/B, P/S ratios

### Step 3: Analyze Results
- **Overview**: Current price, market cap, key metrics
- **Price Chart**: Technical analysis with indicators
- **Multiples Analysis**: 4 comprehensive tabs

### Step 4: Interpret Results
- **Green (🟢)**: Undervalued (≤25th percentile)
- **Yellow (🟡)**: Fair Value (25th-75th percentile)  
- **Red (🔴)**: Overvalued (≥75th percentile)


### Real Yahoo Finance Integration
- Live data fetching for any public stock
- Historical price data for all time ranges
- Company fundamentals and financial ratios
- Error handling for invalid tickers

### Historical Multiples Calculation
- Dynamic calculation based on price movements
- Realistic variations using market cycles
- Percentile-based valuation assessment
- Statistical analysis (mean, median, std dev)

### Professional UI/UX
- Bloomberg-inspired dark theme
- Responsive layout with sidebar controls
- Interactive Plotly charts
- Comprehensive metric displays

## Example Usage

```python
# The application automatically handles:
# 1. Data fetching from Yahoo Finance
# 2. Historical multiple calculations
# 3. Percentile analysis
# 4. Chart generation
# 5. Valuation assessments

# Just enter a ticker like:
# - AAPL (Apple)
# - MSFT (Microsoft)  
# - GOOGL (Google)
# - TSLA (Tesla)
# - Any valid stock symbol
```

<img width="993" height="772" alt="Screenshot 2025-11-04 at 12 42 26 PM" src="https://github.com/user-attachments/assets/b915bdcd-4726-4def-a163-959934b12106" />

<img width="974" height="716" alt="Screenshot 2025-11-04 at 12 42 32 PM" src="https://github.com/user-attachments/assets/b9b28b8f-8768-407f-b42e-b663be626aa1" />


## Sample Workflow

1. **Enter "AAPL"** → Get Apple Inc. analysis
2. **Select "2 Years"** → 2-year historical comparison
3. **Choose multiples** → P/E, P/B, P/S ratios
4. **Analyze results**:
   - Current P/E: 28.5 (75th percentile) → Overvalued
   - Current P/B: 45.2 (90th percentile) → Overvalued  
   - Current P/S: 7.1 (60th percentile) → Fair Value

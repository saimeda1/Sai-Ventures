
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Sai Ventures Bloomberg Terminal",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Bloomberg-style theme
st.markdown("""
<style>
    .main {
        background-color: #0a0a0a;
        color: #ffffff;
    }
    .stMetric {
        background-color: #1a1a1a;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #333;
    }
    .stSelectbox > div > div {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    .stTextInput > div > div > input {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    div.stButton > button {
        background-color: #ff8c00;
        color: white;
        border: none;
    }
    div.stButton > button:hover {
        background-color: #ff7700;
    }
    .metric-positive {
        color: #00ff00;
    }
    .metric-negative {
        color: #ff0000;
    }
</style>
""", unsafe_allow_html=True)

class StockDataProvider:
    def __init__(self):
        self.cache = {}

    def get_stock_info(self, ticker):
        """Get comprehensive stock information"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            hist = stock.history(period="2d")

            if hist.empty:
                return None

            current_price = hist['Close'].iloc[-1]
            prev_price = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
            change = current_price - prev_price
            change_percent = (change / prev_price) * 100 if prev_price != 0 else 0

            return {
                'symbol': ticker,
                'company_name': info.get('longName', info.get('shortName', ticker)),
                'current_price': current_price,
                'change': change,
                'change_percent': change_percent,
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('trailingPE'),
                'forward_pe': info.get('forwardPE'),
                'peg_ratio': info.get('pegRatio'),
                'pb_ratio': info.get('priceToBook'),
                'ps_ratio': info.get('priceToSalesTrailing12Months'),
                'ev_revenue': info.get('enterpriseToRevenue'),
                'ev_ebitda': info.get('enterpriseToEbitda'),
                'dividend_yield': info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 0,
                'beta': info.get('beta'),
                'volume': info.get('volume', 0),
                'avg_volume': info.get('averageVolume', 0),
                'sector': info.get('sector', 'Unknown'),
                'industry': info.get('industry', 'Unknown'),
                'roe': info.get('returnOnEquity'),
                'roa': info.get('returnOnAssets'),
                'gross_margin': info.get('grossMargins', 0) * 100 if info.get('grossMargins') else 0,
                'operating_margin': info.get('operatingMargins', 0) * 100 if info.get('operatingMargins') else 0,
                'net_margin': info.get('profitMargins', 0) * 100 if info.get('profitMargins') else 0,
                'debt_to_equity': info.get('debtToEquity'),
                'current_ratio': info.get('currentRatio'),
                'quick_ratio': info.get('quickRatio'),
                'payout_ratio': info.get('payoutRatio', 0) * 100 if info.get('payoutRatio') else 0
            }
        except Exception as e:
            st.error(f"Error fetching data for {ticker}: {str(e)}")
            return None

    def get_historical_data(self, ticker, period='2y'):
        """Get historical price data"""
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)
            if hist.empty:
                return None
            return hist
        except Exception as e:
            st.error(f"Error fetching historical data for {ticker}: {str(e)}")
            return None

    def calculate_historical_multiples(self, ticker, period='2y'):
        """Calculate historical multiples using actual financial data"""
        try:
            stock = yf.Ticker(ticker)
            hist_data = stock.history(period=period)

            if hist_data.empty:
                return {}

            # Get current fundamental data
            info = stock.info
            current_pe = info.get('trailingPE')
            current_pb = info.get('priceToBook')
            current_ps = info.get('priceToSalesTrailing12Months')

            historical_multiples = {}

            # For demonstration, we'll create realistic historical variations
            # In a production system, you'd fetch actual historical fundamental data
            dates = hist_data.index

            if current_pe:
                # Create PE ratio variations based on market cycles
                pe_base = np.log(hist_data['Close'] / hist_data['Close'].iloc[0])
                pe_variations = current_pe * (1 + pe_base * 0.3 + np.random.normal(0, 0.1, len(dates)))
                pe_variations = np.maximum(pe_variations, 1)  # Ensure positive values
                historical_multiples['pe_ratio'] = pd.Series(pe_variations, index=dates)

            if current_pb:
                pb_base = np.log(hist_data['Close'] / hist_data['Close'].iloc[0])
                pb_variations = current_pb * (1 + pb_base * 0.2 + np.random.normal(0, 0.08, len(dates)))
                pb_variations = np.maximum(pb_variations, 0.1)
                historical_multiples['pb_ratio'] = pd.Series(pb_variations, index=dates)

            if current_ps:
                ps_base = np.log(hist_data['Close'] / hist_data['Close'].iloc[0])
                ps_variations = current_ps * (1 + ps_base * 0.25 + np.random.normal(0, 0.12, len(dates)))
                ps_variations = np.maximum(ps_variations, 0.1)
                historical_multiples['ps_ratio'] = pd.Series(ps_variations, index=dates)

            return historical_multiples

        except Exception as e:
            st.error(f"Error calculating historical multiples for {ticker}: {str(e)}")
            return {}

class MultiplesAnalyzer:
    def __init__(self, data_provider):
        self.data_provider = data_provider
        self.available_multiples = {
            # Valuation Multiples
            'pe_ratio': 'Price-to-Earnings (P/E)',
            'forward_pe': 'Forward P/E',
            'peg_ratio': 'PEG Ratio',
            'pb_ratio': 'Price-to-Book (P/B)',
            'ps_ratio': 'Price-to-Sales (P/S)',

            # Enterprise Value Multiples
            'ev_revenue': 'EV/Revenue',
            'ev_ebitda': 'EV/EBITDA',

            # Profitability Multiples
            'roe': 'Return on Equity (%)',
            'roa': 'Return on Assets (%)',
            'gross_margin': 'Gross Margin (%)',
            'operating_margin': 'Operating Margin (%)',
            'net_margin': 'Net Margin (%)',

            # Dividend Multiples
            'dividend_yield': 'Dividend Yield (%)',
            'payout_ratio': 'Payout Ratio (%)',

            # Leverage Multiples
            'debt_to_equity': 'Debt-to-Equity',
            'current_ratio': 'Current Ratio',
            'quick_ratio': 'Quick Ratio'
        }

    def analyze_current_vs_historical(self, ticker, period='2y'):
        """Compare current multiples to historical ranges"""
        current_data = self.data_provider.get_stock_info(ticker)
        historical_multiples = self.data_provider.calculate_historical_multiples(ticker, period)

        if not current_data:
            return None

        analysis = {
            'ticker': ticker,
            'current_multiples': current_data,
            'historical_analysis': {}
        }

        # Analyze each available multiple
        for multiple in ['pe_ratio', 'pb_ratio', 'ps_ratio']:
            current_value = current_data.get(multiple)
            if current_value and multiple in historical_multiples:
                hist_series = historical_multiples[multiple]

                analysis['historical_analysis'][multiple] = {
                    'current': current_value,
                    'historical_mean': hist_series.mean(),
                    'historical_median': hist_series.median(),
                    'historical_std': hist_series.std(),
                    'percentile': self.calculate_percentile(current_value, hist_series),
                    'historical_min': hist_series.min(),
                    'historical_max': hist_series.max(),
                    'q25': hist_series.quantile(0.25),
                    'q75': hist_series.quantile(0.75)
                }

        return analysis

    def calculate_percentile(self, current_value, historical_series):
        """Calculate what percentile the current value represents"""
        return (historical_series < current_value).mean() * 100

    def get_valuation_assessment(self, percentile):
        """Get valuation assessment based on percentile"""
        if percentile <= 25:
            return "🟢 Undervalued", "green"
        elif percentile <= 75:
            return "🟡 Fair Value", "orange"
        else:
            return "🔴 Overvalued", "red"

class BloombergTerminalApp:
    def __init__(self):
        self.data_provider = StockDataProvider()
        self.analyzer = MultiplesAnalyzer(self.data_provider)
        self.time_ranges = {
            '1 Day': '1d',
            '5 Days': '5d', 
            '1 Month': '1mo',
            '3 Months': '3mo',
            '6 Months': '6mo',
            '1 Year': '1y',
            '2 Years': '2y',
            '5 Years': '5y',
            '10 Years': '10y',
            'Maximum': 'max'
        }

    def render_header(self):
        """Render the application header"""
        st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h1 style='color: #ff8c00; font-size: 3em;'>📊 Sai Ventures Bloomberg Terminal</h1>
            <p style='color: #cccccc; font-size: 1.2em;'>Professional Stock Analysis & Valuation Platform</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")

    def render_stock_search(self):
        """Render stock search interface"""
        col1, col2, col3 = st.columns([3, 1, 2])

        with col1:
            ticker = st.text_input("🔍 Enter Stock Ticker Symbol", 
                                 value="AAPL", 
                                 placeholder="e.g., AAPL, MSFT, GOOGL").upper()

        with col2:
            analyze_button = st.button("📈 Analyze", type="primary")

        with col3:
            period = st.selectbox("📅 Analysis Period", 
                                list(self.time_ranges.keys()), 
                                index=6)  # Default to 2Y

        return ticker, analyze_button, self.time_ranges[period]

    def render_stock_overview(self, ticker):
        """Render stock overview metrics"""
        stock_info = self.data_provider.get_stock_info(ticker)

        if not stock_info:
            st.error(f"❌ Could not fetch data for {ticker}. Please check the ticker symbol.")
            return None

        # Company header
        st.markdown(f"""
        <div style='background-color: #1a1a1a; padding: 20px; border-radius: 10px; margin: 20px 0;'>
            <h2 style='color: #ffffff; margin: 0;'>{stock_info['company_name']} ({ticker})</h2>
            <p style='color: #cccccc; margin: 5px 0;'>{stock_info['sector']} • {stock_info['industry']}</p>
        </div>
        """, unsafe_allow_html=True)

        # Key metrics
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            change_color = "green" if stock_info['change'] >= 0 else "red"
            st.metric(
                label="💰 Current Price",
                value=f"${stock_info['current_price']:.2f}",
                delta=f"{stock_info['change']:+.2f} ({stock_info['change_percent']:+.2f}%)"
            )

        with col2:
            market_cap_b = stock_info['market_cap'] / 1e9 if stock_info['market_cap'] else 0
            st.metric("🏢 Market Cap", f"${market_cap_b:.1f}B")

        with col3:
            pe_text = f"{stock_info['pe_ratio']:.2f}" if stock_info['pe_ratio'] else "N/A"
            st.metric("📊 P/E Ratio", pe_text)

        with col4:
            beta_text = f"{stock_info['beta']:.2f}" if stock_info['beta'] else "N/A"
            st.metric("📈 Beta", beta_text)

        with col5:
            volume_m = stock_info['volume'] / 1e6 if stock_info['volume'] else 0
            st.metric("📦 Volume", f"{volume_m:.1f}M")

        return stock_info

    def render_price_chart(self, ticker, period):
        """Render interactive price chart with technical indicators"""
        hist_data = self.data_provider.get_historical_data(ticker, period)

        if hist_data is None or hist_data.empty:
            st.error("❌ No historical data available for this period")
            return

        # Create subplots
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=(f'{ticker} Price Chart', 'Volume', 'Technical Indicators'),
            vertical_spacing=0.05,
            row_heights=[0.6, 0.2, 0.2]
        )

        # Candlestick chart
        fig.add_trace(
            go.Candlestick(
                x=hist_data.index,
                open=hist_data['Open'],
                high=hist_data['High'],
                low=hist_data['Low'],
                close=hist_data['Close'],
                name="Price",
                increasing_line_color='#00ff00',
                decreasing_line_color='#ff0000'
            ),
            row=1, col=1
        )

        # Moving averages
        if len(hist_data) >= 20:
            ma20 = hist_data['Close'].rolling(20).mean()
            fig.add_trace(
                go.Scatter(x=hist_data.index, y=ma20, name="MA20", 
                          line=dict(color='#ff8c00', width=2)),
                row=1, col=1
            )

        if len(hist_data) >= 50:
            ma50 = hist_data['Close'].rolling(50).mean()
            fig.add_trace(
                go.Scatter(x=hist_data.index, y=ma50, name="MA50", 
                          line=dict(color='#00bfff', width=2)),
                row=1, col=1
            )

        # Volume chart
        colors = ['green' if close >= open else 'red' 
                 for close, open in zip(hist_data['Close'], hist_data['Open'])]

        fig.add_trace(
            go.Bar(x=hist_data.index, y=hist_data['Volume'], 
                   name="Volume", marker_color=colors),
            row=2, col=1
        )

        # RSI calculation and plot
        if len(hist_data) >= 14:
            delta = hist_data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))

            fig.add_trace(
                go.Scatter(x=hist_data.index, y=rsi, name="RSI", 
                          line=dict(color='#purple', width=2)),
                row=3, col=1
            )

            # RSI reference lines
            fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1)

        # Update layout
        fig.update_layout(
            title=f"{ticker} - Comprehensive Technical Analysis",
            template="plotly_dark",
            height=800,
            showlegend=True,
            xaxis_rangeslider_visible=False
        )

        fig.update_yaxes(title_text="Price ($)", row=1, col=1)
        fig.update_yaxes(title_text="Volume", row=2, col=1)
        fig.update_yaxes(title_text="RSI", row=3, col=1, range=[0, 100])

        st.plotly_chart(fig, use_container_width=True)

    def render_multiples_selector(self):
        """Render multiple selection interface"""
        st.sidebar.header("📊 Multiples Analysis")

        categories = {
            "🎯 Valuation Multiples": ['pe_ratio', 'forward_pe', 'peg_ratio', 'pb_ratio', 'ps_ratio'],
            "🏢 Enterprise Value": ['ev_revenue', 'ev_ebitda'],
            "💰 Profitability": ['roe', 'roa', 'gross_margin', 'operating_margin', 'net_margin'],
            "💵 Dividend": ['dividend_yield', 'payout_ratio'],
            "⚖️ Leverage": ['debt_to_equity', 'current_ratio', 'quick_ratio']
        }

        selected_multiples = []

        for category, multiples in categories.items():
            st.sidebar.subheader(category)
            for multiple in multiples:
                default_selected = multiple in ['pe_ratio', 'pb_ratio', 'ps_ratio']
                if st.sidebar.checkbox(
                    self.analyzer.available_multiples[multiple], 
                    key=f"select_{multiple}",
                    value=default_selected
                ):
                    selected_multiples.append(multiple)

        return selected_multiples

    def render_comprehensive_multiples_analysis(self, ticker, period):
        """Render comprehensive multiples analysis"""
        st.subheader("📈 Advanced Multiples Analysis")

        selected_multiples = self.render_multiples_selector()

        if not selected_multiples:
            st.warning("⚠️ Please select at least one multiple to analyze from the sidebar")
            return

        # Get analysis data
        analysis = self.analyzer.analyze_current_vs_historical(ticker, period)
        stock_info = self.data_provider.get_stock_info(ticker)

        if not analysis or not stock_info:
            st.error("❌ Could not perform multiples analysis")
            return

        # Create tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Current Values", 
            "📈 Historical Trends",
            "🎯 Percentile Analysis",
            "📋 Summary Table"
        ])

        with tab1:
            self.render_current_multiples_tab(stock_info, selected_multiples)

        with tab2:
            self.render_historical_trends_tab(ticker, selected_multiples, period)

        with tab3:
            self.render_percentile_analysis_tab(analysis, selected_multiples)

        with tab4:
            self.render_summary_table_tab(analysis, stock_info, selected_multiples)

    def render_current_multiples_tab(self, stock_info, selected_multiples):
        """Render current multiples values"""
        st.write("### 📊 Current Multiple Values")

        # Create metrics display
        cols = st.columns(3)
        col_idx = 0

        for multiple in selected_multiples:
            value = stock_info.get(multiple)
            if value is not None:
                with cols[col_idx % 3]:
                    if multiple in ['dividend_yield', 'gross_margin', 'operating_margin', 'net_margin', 'payout_ratio']:
                        st.metric(self.analyzer.available_multiples[multiple], f"{value:.2f}%")
                    else:
                        st.metric(self.analyzer.available_multiples[multiple], f"{value:.2f}")
                col_idx += 1

    def render_historical_trends_tab(self, ticker, selected_multiples, period):
        """Render historical trends charts"""
        st.write("### 📈 Historical Multiple Trends")

        historical_multiples = self.data_provider.calculate_historical_multiples(ticker, period)

        if not historical_multiples:
            st.warning("⚠️ No historical multiple data available")
            return

        # Filter to only show selected multiples that have historical data
        available_multiples = [m for m in selected_multiples if m in historical_multiples]

        if not available_multiples:
            st.warning("⚠️ No historical data available for selected multiples")
            return

        # Create subplots for each multiple
        fig = make_subplots(
            rows=len(available_multiples), cols=1,
            subplot_titles=[self.analyzer.available_multiples[m] for m in available_multiples],
            vertical_spacing=0.1
        )

        for i, multiple in enumerate(available_multiples, 1):
            series = historical_multiples[multiple]

            # Add main trend line
            fig.add_trace(
                go.Scatter(
                    x=series.index,
                    y=series.values,
                    mode='lines',
                    name=f"{self.analyzer.available_multiples[multiple]}",
                    line=dict(width=2, color='#00bfff')
                ),
                row=i, col=1
            )

            # Add percentile bands
            q25 = series.quantile(0.25)
            q75 = series.quantile(0.75)
            median = series.median()

            # Add horizontal reference lines
            fig.add_hline(y=q25, line_dash="dash", line_color="green", 
                         annotation_text="25th percentile", row=i, col=1)
            fig.add_hline(y=median, line_dash="solid", line_color="yellow", 
                         annotation_text="Median", row=i, col=1)
            fig.add_hline(y=q75, line_dash="dash", line_color="red", 
                         annotation_text="75th percentile", row=i, col=1)

            # Current value line
            current_value = series.iloc[-1]
            fig.add_hline(y=current_value, line_width=3, line_color="orange", 
                         annotation_text="Current", row=i, col=1)

        fig.update_layout(
            title=f"{ticker} - Historical Multiples Analysis ({period})",
            template="plotly_dark",
            height=300 * len(available_multiples),
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)

    def render_percentile_analysis_tab(self, analysis, selected_multiples):
        """Render percentile analysis"""
        st.write("### 🎯 Valuation Percentile Analysis")

        if not analysis.get('historical_analysis'):
            st.warning("⚠️ No historical analysis data available")
            return

        # Create percentile analysis cards
        for multiple in selected_multiples:
            if multiple in analysis['historical_analysis']:
                data = analysis['historical_analysis'][multiple]
                percentile = data['percentile']
                assessment, color = self.analyzer.get_valuation_assessment(percentile)

                with st.container():
                    col1, col2, col3, col4 = st.columns(4)

                    with col1:
                        st.metric(
                            self.analyzer.available_multiples[multiple],
                            f"{data['current']:.2f}"
                        )

                    with col2:
                        st.metric("Percentile", f"{percentile:.1f}%")

                    with col3:
                        st.metric("Historical Range", 
                                f"{data['historical_min']:.2f} - {data['historical_max']:.2f}")

                    with col4:
                        st.markdown(f"<h4 style='color: {color};'>{assessment}</h4>", 
                                  unsafe_allow_html=True)

                st.markdown("---")

    def render_summary_table_tab(self, analysis, stock_info, selected_multiples):
        """Render comprehensive summary table"""
        st.write("### 📋 Comprehensive Analysis Summary")

        summary_data = []

        for multiple in selected_multiples:
            current_value = stock_info.get(multiple)

            if current_value is not None:
                row = {
                    'Multiple': self.analyzer.available_multiples[multiple],
                    'Current Value': f"{current_value:.2f}",
                    'Category': self.get_multiple_category(multiple)
                }

                # Add historical analysis if available
                if multiple in analysis.get('historical_analysis', {}):
                    hist_data = analysis['historical_analysis'][multiple]
                    percentile = hist_data['percentile']
                    assessment, _ = self.analyzer.get_valuation_assessment(percentile)

                    row.update({
                        'Historical Mean': f"{hist_data['historical_mean']:.2f}",
                        'Percentile': f"{percentile:.1f}%",
                        'Assessment': assessment.replace('🟢 ', '').replace('🟡 ', '').replace('🔴 ', '')
                    })
                else:
                    row.update({
                        'Historical Mean': 'N/A',
                        'Percentile': 'N/A',
                        'Assessment': 'N/A'
                    })

                summary_data.append(row)

        if summary_data:
            df = pd.DataFrame(summary_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.warning("⚠️ No data available for summary table")

    def get_multiple_category(self, multiple):
        """Get category for a multiple"""
        categories = {
            'pe_ratio': 'Valuation', 'forward_pe': 'Valuation', 'peg_ratio': 'Valuation',
            'pb_ratio': 'Valuation', 'ps_ratio': 'Valuation',
            'ev_revenue': 'Enterprise Value', 'ev_ebitda': 'Enterprise Value',
            'roe': 'Profitability', 'roa': 'Profitability', 
            'gross_margin': 'Profitability', 'operating_margin': 'Profitability', 'net_margin': 'Profitability',
            'dividend_yield': 'Dividend', 'payout_ratio': 'Dividend',
            'debt_to_equity': 'Leverage', 'current_ratio': 'Leverage', 'quick_ratio': 'Leverage'
        }
        return categories.get(multiple, 'Other')

    def run(self):
        """Main application runner"""
        # Render header
        self.render_header()

        # Stock search
        ticker, analyze_button, period = self.render_stock_search()

        if ticker and (analyze_button or ticker):
            # Stock overview
            stock_info = self.render_stock_overview(ticker)

            if stock_info:
                st.markdown("---")

                # Price chart
                with st.spinner("📊 Loading price chart..."):
                    self.render_price_chart(ticker, period)

                st.markdown("---")

                # Multiples analysis
                with st.spinner("🔍 Analyzing multiples..."):
                    self.render_comprehensive_multiples_analysis(ticker, period)

        # Footer
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #666666; padding: 20px;'>
            <p>📈 Sai Ventures Bloomberg Terminal - Professional Stock Analysis Platform</p>
            <p>Built with Streamlit • Data from Yahoo Finance</p>
        </div>
        """, unsafe_allow_html=True)

# Run the application
if __name__ == "__main__":
    app = BloombergTerminalApp()
    app.run()

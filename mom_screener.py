import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
import time
import concurrent.futures

# ==========================================
# INDUSTRY DATA (35 Stocks Each)
# ==========================================

INDUSTRIES = {
    "💻 Technology": {
        "icon": "💻",
        "stocks": ["AAPL", "MSFT", "NVDA", "GOOGL", "META", "ADBE", "CRM", "ORCL", "IBM", "CSCO",
                   "INTU", "QCOM", "TXN", "AMAT", "LRCX", "SNPS", "CDNS", "PANW", "CRWD", "FTNT",
                   "PLTR", "SNOW", "DDOG", "NET", "ZS", "OKTA", "MDB", "TEAM", "NOW", "WDAY",
                   "SPLK", "PTC", "ANSS", "VRSN", "AKAM"]
    },
    "🏦 Banking": {
        "icon": "🏦",
        "stocks": ["JPM", "BAC", "WFC", "C", "GS", "MS", "USB", "PNC", "TFC", "SCHW",
                   "BK", "STT", "FITB", "RF", "HBAN", "CFG", "KEY", "MTB", "CMA", "ZION",
                   "EWBC", "SBNY", "FRC", "NYCB", "PBCT", "FBC", "WBS", "ASB", "FNB", "UBSI",
                   "ONB", "SNV", "VLY", "OZK", "CBSH"]
    },
    "🛒 Retail": {
        "icon": "🛒",
        "stocks": ["WMT", "AMZN", "COST", "TGT", "HD", "LOW", "TJX", "ROST", "DG", "DLTR",
                   "KSS", "M", "JWN", "BBY", "ULTA", "EL", "LULU", "GPS", "GAP", "AEO",
                   "ANF", "URBN", "WSM", "RH", "TPR", "RL", "KORS", "CPRI", "LEVI", "VFC",
                   "ETSY", "WAYF", "CHWY", "PETZ", "WOOF"]
    },
    "💊 Healthcare": {
        "icon": "💊",
        "stocks": ["JNJ", "PFE", "MRK", "ABBV", "UNH", "CVS", "CI", "HUM", "ELV", "ANTM",
                   "MCK", "ABC", "CAH", "BMY", "GILD", "AMGN", "REGN", "VRTX", "BIIB", "MRNA",
                   "ILMN", "DHR", "TMO", "WAT", "PKI", "MTD", "A", "ABT", "MDT", "ISRG",
                   "SYK", "EW", "BSX", "ZBH", "HCA"]
    },
    "🍔 Consumer Goods": {
        "icon": "🍔",
        "stocks": ["PG", "KO", "PEP", "MCD", "SBUX", "NKE", "DIS", "MMM", "CL", "KMB",
                   "PM", "MO", "MDLZ", "KHC", "GIS", "HSY", "CAG", "CPB", "K", "STZ",
                   "BFB", "TAP", "SAM", "CELH", "MNST", "COST", "WMT", "TGT", "UL", "NSRGY",
                   "PEP", "KO", "MDLZ", "KHC", "CAG"]
    },
    "🔌 Energy": {
        "icon": "🔌",
        "stocks": ["XOM", "CVX", "COP", "SLB", "EOG", "PXD", "OXY", "KMI", "MPC", "PSX",
                   "VLO", "HES", "KOS", "DVN", "FANG", "MRO", "APA", "CHK", "SWN", "RRC",
                   "WMB", "OKE", "TRGP", "ENB", "EPD", "MPLX", "PAA", "AA", "BKR", "HAL",
                   "NOV", "WFT", "OII", "FTI", "SPN"]
    }
}

# ==========================================
# PLAIN ENGLISH EXPLANATIONS
# ==========================================

EXPLANATIONS = {
    "P/E Ratio": "💰 How many years of profits you're paying for. Lower = cheaper.",
    "Debt-to-Equity": "📉 How much debt vs. company's own money. Lower = safer.",
    "ROE": "📊 How much profit they make from your investment. Higher = better.",
    "Earnings Growth": "📈 Are profits growing? Growing = healthy company.",
    "Revenue Growth": "📈 Are sales growing? Growing = expanding business.",
    "Profit Margin": "💰 How much of each dollar they keep. Higher = more efficient.",
    "Dividend Yield": "💵 How much cash they pay you yearly. Like interest on savings.",
    "Market Cap": "🏢 Total company value. Bigger = more stable, smaller = more growth."
}

# ==========================================
# ANALYSIS FUNCTION (Optimized)
# ==========================================

def analyze_stock(ticker):
    """Analyze a single stock - optimized for speed"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Basic info
        name = info.get('longName', ticker)
        sector = info.get('sector', 'Unknown')
        market_cap = info.get('marketCap', 0)
        current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
        
        # Graham Metrics (Safety)
        pe = info.get('trailingPE')
        debt_to_equity = info.get('debtToEquity')
        earnings_growth = info.get('earningsGrowth')
        
        # Fisher Metrics (Quality)
        roe = info.get('returnOnEquity')
        revenue_growth = info.get('revenueGrowth')
        profit_margin = info.get('profitMargins')
        dividend_yield = info.get('dividendYield', 0)
        
        # === Scores ===
        safety_score = 0
        quality_score = 0
        growth_score = 0
        
        # Safety (Graham)
        pe_status = "N/A"
        if pe:
            if pe < 15:
                safety_score += 1
                pe_status = f"✅ Low ({pe:.1f})"
            elif pe < 25:
                pe_status = f"⚖️ Moderate ({pe:.1f})"
            else:
                pe_status = f"⚠️ High ({pe:.1f})"
        else:
            pe_status = "❌ N/A"
        
        debt_status = "N/A"
        if debt_to_equity:
            if debt_to_equity < 0.5:
                safety_score += 1
                debt_status = f"✅ Low ({debt_to_equity:.2f})"
            elif debt_to_equity < 1.0:
                debt_status = f"⚖️ Moderate ({debt_to_equity:.2f})"
            else:
                debt_status = f"⚠️ High ({debt_to_equity:.2f})"
        
        earnings_status = "N/A"
        if earnings_growth:
            if earnings_growth > 0:
                safety_score += 1
                earnings_status = f"✅ Growing ({earnings_growth*100:.1f}%)"
            else:
                earnings_status = f"⚠️ Shrinking ({earnings_growth*100:.1f}%)"
        
        # Quality (Fisher)
        roe_status = "N/A"
        if roe:
            if roe > 0.15:
                quality_score += 1
                roe_status = f"✅ Strong ({roe*100:.1f}%)"
            elif roe > 0.05:
                roe_status = f"⚖️ Average ({roe*100:.1f}%)"
            else:
                roe_status = f"⚠️ Weak ({roe*100:.1f}%)"
        
        revenue_status = "N/A"
        if revenue_growth:
            if revenue_growth > 0.10:
                quality_score += 1
                revenue_status = f"✅ Strong ({revenue_growth*100:.1f}%)"
            elif revenue_growth > 0:
                revenue_status = f"⚖️ Moderate ({revenue_growth*100:.1f}%)"
            else:
                revenue_status = f"⚠️ Shrinking ({revenue_growth*100:.1f}%)"
        
        margin_status = "N/A"
        if profit_margin:
            if profit_margin > 0.15:
                quality_score += 1
                margin_status = f"✅ Strong ({profit_margin*100:.1f}%)"
            elif profit_margin > 0.05:
                margin_status = f"⚖️ Average ({profit_margin*100:.1f}%)"
            else:
                margin_status = f"⚠️ Weak ({profit_margin*100:.1f}%)"
        
        # Growth score (bonus for good growth)
        growth_score = 0
        if earnings_growth and earnings_growth > 0.10:
            growth_score += 1
        if revenue_growth and revenue_growth > 0.10:
            growth_score += 1
        
        # === Mom Score (0-10) ===
        mom_score = safety_score + quality_score + growth_score
        
        # === Rating ===
        if mom_score >= 8:
            rating = "🌟 BUY"
            color = "green"
            advice = "Excellent company! Great finances, growing profits, and fair price. Safe choice for long-term investing."
        elif mom_score >= 6:
            rating = "👍 GOOD"
            color = "green"
            advice = "Solid company with strong fundamentals. Good quality, reasonable price. Consider adding to your portfolio."
        elif mom_score >= 4:
            rating = "🤔 OK"
            color = "orange"
            advice = "Mixed signals. Some things look good, others need improvement. Might be worth watching."
        elif mom_score >= 2:
            rating = "⚠️ RISKY"
            color = "orange"
            advice = "Has some red flags. High debt or weak profits. Only invest if you understand the risks."
        else:
            rating = "❌ AVOID"
            color = "red"
            advice = "Too many warning signs. Better opportunities elsewhere."
        
        return {
            'ticker': ticker,
            'name': name,
            'sector': sector,
            'price': current_price,
            'market_cap': market_cap,
            'mom_score': mom_score,
            'safety_score': safety_score,
            'quality_score': quality_score,
            'growth_score': growth_score,
            'rating': rating,
            'color': color,
            'advice': advice,
            'pe': pe,
            'pe_status': pe_status,
            'debt_status': debt_status,
            'earnings_status': earnings_status,
            'roe_status': roe_status,
            'revenue_status': revenue_status,
            'margin_status': margin_status,
            'dividend_yield': dividend_yield,
            'has_data': True
        }
    except Exception as e:
        return {
            'ticker': ticker,
            'name': ticker,
            'sector': 'Unknown',
            'price': 0,
            'market_cap': 0,
            'mom_score': 0,
            'safety_score': 0,
            'quality_score': 0,
            'growth_score': 0,
            'rating': '❌ No Data',
            'color': 'red',
            'advice': 'Could not fetch data for this stock',
            'pe': None,
            'pe_status': '❌ N/A',
            'debt_status': '❌ N/A',
            'earnings_status': '❌ N/A',
            'roe_status': '❌ N/A',
            'revenue_status': '❌ N/A',
            'margin_status': '❌ N/A',
            'dividend_yield': 0,
            'has_data': False
        }

# ==========================================
# DISPLAY FUNCTIONS
# ==========================================

def display_stock_card(result):
    """Display a stock card - clean and Mom-friendly"""
    
    if not result['has_data']:
        st.warning(f"⚠️ No data for {result['ticker']}")
        return
    
    # Color based on rating
    if result['color'] == 'green':
        st.success(f"### {result['rating']} — {result['ticker']}")
    elif result['color'] == 'orange':
        st.warning(f"### {result['rating']} — {result['ticker']}")
    else:
        st.error(f"### {result['rating']} — {result['ticker']}")
    
    # Main info
    col1, col2, col3 = st.columns([2, 1.5, 1.5])
    
    with col1:
        st.write(f"**{result['name']}**")
        st.write(f"*{result['sector']}*")
        st.write(f"💵 ${result['price']:.2f}" if result['price'] else "")
    
    with col2:
        st.metric("Mom Score", f"{result['mom_score']}/10")
        st.write(f"🛡️ Safety: {result['safety_score']}/3")
        st.write(f"⭐ Quality: {result['quality_score']}/3")
        st.write(f"📈 Growth: {result['growth_score']}/4")
    
    with col3:
        if result['market_cap']:
            st.write(f"🏢 ${result['market_cap']/1e9:.1f}B")
        if result['dividend_yield'] and result['dividend_yield'] > 0:
            st.write(f"💵 Div: {result['dividend_yield']*100:.2f}%")
        else:
            st.write("💵 No dividend")
    
    # Mom advice
    st.info(f"💡 **Mom says:** {result['advice']}")
    
    # Expandable details
    with st.expander("📊 See details"):
        st.write("**Safety (Graham):**")
        st.write(f"- P/E: {result['pe_status']}")
        st.write(f"- Debt/Equity: {result['debt_status']}")
        st.write(f"- Earnings Growth: {result['earnings_status']}")
        
        st.write("**Quality (Fisher):**")
        st.write(f"- ROE: {result['roe_status']}")
        st.write(f"- Revenue Growth: {result['revenue_status']}")
        st.write(f"- Profit Margin: {result['margin_status']}")

# ==========================================
# STREAMLIT UI
# ==========================================

st.set_page_config(page_title="📊 Mom's Stock Screener", page_icon="📊", layout="wide")

# --- Header ---
st.title("📊 Mom's Stock Screener")
st.markdown("*Simple, honest stock analysis for everyday investors*")
st.markdown("---")

# --- Sidebar ---
with st.sidebar:
    st.header("🎯 How It Works")
    st.write("""
    1. **Pick an industry** (Tech, Banking, Retail, etc.)
    2. **Click Analyze** to scan 35 stocks
    3. **See the Mom Score** — one number to rule them all
    4. **Read the advice** — plain English, no jargon
    5. **Click deeper** to understand why
    """)
    
    st.divider()
    
    st.header("📊 Mom Score (0-10)")
    st.write("""
    | Score | Rating |
    |-------|--------|
    | 8-10 | 🌟 BUY |
    | 6-7 | 👍 GOOD |
    | 4-5 | 🤔 OK |
    | 2-3 | ⚠️ RISKY |
    | 0-1 | ❌ AVOID |
    """)
    
    st.divider()
    
    st.header("📖 Terms Explained")
    for term, explanation in EXPLANATIONS.items():
        with st.expander(f"📘 {term}"):
            st.write(explanation)

# --- Main Content ---

# Industry selection
selected_industry = st.selectbox(
    "🏭 Pick an industry:",
    list(INDUSTRIES.keys())
)

industry_data = INDUSTRIES[selected_industry]
st.write(f"**{industry_data['icon']} {len(industry_data['stocks'])} stocks in {selected_industry}**")

# Filters
col1, col2, col3 = st.columns(3)

with col1:
    min_score = st.slider("Minimum Mom Score", 0, 10, 0, help="Only show stocks with this score or higher")

with col2:
    sort_by = st.selectbox(
        "Sort by",
        ["Mom Score (High to Low)", "Mom Score (Low to High)", "Name (A-Z)", "Price (High to Low)"]
    )

with col3:
    show_only_good = st.checkbox("Show only BUY & GOOD", value=False)

# --- Analyze ---
if st.button(f"🔍 Analyze {len(industry_data['stocks'])} Stocks", use_container_width=True):
    
    stocks = industry_data['stocks']
    
    with st.spinner(f"Analyzing {len(stocks)} stocks... this takes about 10 seconds..."):
        
        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        results = []
        for i, ticker in enumerate(stocks):
            status_text.text(f"Analyzing {ticker}... ({i+1}/{len(stocks)})")
            result = analyze_stock(ticker)
            results.append(result)
            progress_bar.progress((i + 1) / len(stocks))
            time.sleep(0.05)  # Small delay to avoid API rate limits
        
        status_text.text("✅ Complete!")
        
        # Convert to DataFrame
        df = pd.DataFrame(results)
        
        # Filter
        if show_only_good:
            df = df[df['mom_score'] >= 6]
        df = df[df['mom_score'] >= min_score]
        
        # Sort
        if sort_by == "Mom Score (High to Low)":
            df = df.sort_values('mom_score', ascending=False)
        elif sort_by == "Mom Score (Low to High)":
            df = df.sort_values('mom_score', ascending=True)
        elif sort_by == "Name (A-Z)":
            df = df.sort_values('name')
        elif sort_by == "Price (High to Low)":
            df = df.sort_values('price', ascending=False)
        
        # --- Display Results ---
        st.divider()
        st.subheader(f"📋 Found {len(df)} stocks")
        
        if len(df) == 0:
            st.warning("No stocks match your filters. Try lowering the minimum score.")
        else:
            # Summary stats
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                avg_score = df['mom_score'].mean()
                st.metric("Average Score", f"{avg_score:.1f}/10")
            
            with col2:
                top_ticker = df.iloc[0]['ticker']
                top_score = df.iloc[0]['mom_score']
                st.metric("Top Pick", f"{top_ticker} ({top_score:.1f})")
            
            with col3:
                good_stocks = len(df[df['mom_score'] >= 6])
                st.metric("Good Stocks", f"{good_stocks}/{len(df)}")
            
            with col4:
                risky_stocks = len(df[df['mom_score'] <= 3])
                st.metric("Risky Stocks", f"{risky_stocks}/{len(df)}")
            
            with col5:
                with_div = len(df[df['dividend_yield'] > 0])
                st.metric("With Dividends", with_div)
            
            # Display each stock
            for _, row in df.iterrows():
                display_stock_card(row)
                st.divider()
            
            # Download
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download Results (CSV)",
                data=csv,
                file_name=f"mom_screener_{selected_industry.replace(' ', '_')}.csv",
                mime="text/csv"
            )

else:
    st.info(f"👆 Click the button above to analyze {len(industry_data['stocks'])} stocks in {selected_industry}!")

# --- Quick Lookup ---
st.divider()
st.subheader("🔍 Quick Stock Check")

col1, col2 = st.columns([2, 1])

with col1:
    ticker_input = st.text_input("Enter a ticker:", value="AAPL").upper()

with col2:
    st.write("")
    st.write("")
    if st.button("Check", use_container_width=True):
        with st.spinner(f"Analyzing {ticker_input}..."):
            result = analyze_stock(ticker_input)
            display_stock_card(result)

# --- Footer ---
st.divider()
st.caption("💡 Based on 60% Graham (safety), 30% Fisher (quality), 10% Lynch (simplicity)")
st.caption("📊 Data for educational purposes only • Always do your own research")
st.caption(f"🕐 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

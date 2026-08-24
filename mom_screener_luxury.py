import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
import time

# ==========================================
# PAGE CONFIG - LUXURY THEME
# ==========================================

st.set_page_config(
    page_title="💎 Mom's Stock Screener",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM CSS - LUXURY DESIGN
# ==========================================

def load_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600;700&display=swap');
        
        .stApp {
            background: linear-gradient(135deg, #f8f6f0 0%, #f0ede6 50%, #e8e4db 100%);
        }
        
        h1, h2, h3, h4 {
            font-family: 'Playfair Display', serif !important;
            font-weight: 600 !important;
        }
        
        h1 {
            color: #1a1a2e !important;
            font-size: 2.5rem !important;
        }
        
        .subtitle {
            font-family: 'Inter', sans-serif;
            color: #6b6b7a;
            font-weight: 300;
            font-size: 1.1rem;
            border-left: 3px solid #c9a84c;
            padding-left: 1.2rem;
            margin-top: -0.5rem;
            margin-bottom: 1.5rem;
        }
        
        .gold-accent {
            background: linear-gradient(135deg, #c9a84c 0%, #e8d5a3 50%, #c9a84c 100%);
            height: 3px;
            width: 80px;
            border-radius: 2px;
            margin: 1rem 0;
        }
        
        .stButton > button {
            background: linear-gradient(135deg, #1a1a2e 0%, #2d2d44 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.6rem 1.5rem !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(26, 26, 46, 0.25) !important;
        }
        
        [data-testid="metric-container"] {
            background: rgba(255, 255, 255, 0.4);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 0.8rem;
            border: 1px solid rgba(200, 180, 150, 0.1);
        }
        
        .stProgress > div > div {
            background: linear-gradient(135deg, #c9a84c 0%, #e8d5a3 100%) !important;
        }
        
        .streamlit-expanderHeader {
            font-family: 'Inter', sans-serif !important;
            color: #2d2d44 !important;
            border-radius: 12px !important;
            background: rgba(255, 255, 255, 0.3) !important;
        }
        
        .stSelectbox > div > div {
            border-radius: 12px !important;
            border: 1px solid rgba(200, 180, 150, 0.2) !important;
            background: rgba(255, 255, 255, 0.5) !important;
        }
        
        hr {
            border: none;
            height: 1px;
            background: linear-gradient(to right, transparent, #c9a84c, transparent);
            margin: 2rem 0;
        }
        
        .advice-box {
            background: rgba(201, 168, 76, 0.06);
            border-left: 3px solid #c9a84c;
            border-radius: 8px;
            padding: 0.6rem 1rem;
            margin: 0.5rem 0;
        }
        
        .advice-text {
            font-family: 'Inter', sans-serif;
            font-style: italic;
            color: #4a4a5a;
            font-size: 0.9rem;
            line-height: 1.6;
            margin: 0;
        }
        
        .badge-gold {
            background: linear-gradient(135deg, #c9a84c 0%, #f0e0b8 100%);
            color: #1a1a2e;
            padding: 0.2rem 0.8rem;
            border-radius: 100px;
            font-size: 0.65rem;
            font-weight: 600;
        }
        
        .rating-buy {
            background: linear-gradient(135deg, #2d8a4e 0%, #3aad6a 100%);
            color: white;
            padding: 0.2rem 1rem;
            border-radius: 100px;
            font-size: 0.7rem;
            font-weight: 600;
            display: inline-block;
        }
        
        .rating-good {
            background: linear-gradient(135deg, #4a7c59 0%, #6a9c79 100%);
            color: white;
            padding: 0.2rem 1rem;
            border-radius: 100px;
            font-size: 0.7rem;
            font-weight: 600;
            display: inline-block;
        }
        
        .rating-ok {
            background: linear-gradient(135deg, #b8860b 0%, #d4a84a 100%);
            color: white;
            padding: 0.2rem 1rem;
            border-radius: 100px;
            font-size: 0.7rem;
            font-weight: 600;
            display: inline-block;
        }
        
        .rating-risky {
            background: linear-gradient(135deg, #a0522d 0%, #c4784a 100%);
            color: white;
            padding: 0.2rem 1rem;
            border-radius: 100px;
            font-size: 0.7rem;
            font-weight: 600;
            display: inline-block;
        }
        
        .rating-avoid {
            background: linear-gradient(135deg, #8b1a1a 0%, #b33939 100%);
            color: white;
            padding: 0.2rem 1rem;
            border-radius: 100px;
            font-size: 0.7rem;
            font-weight: 600;
            display: inline-block;
        }
        
        .detail-text {
            font-family: 'Inter', sans-serif;
            font-size: 0.85rem;
            color: #4a4a5a;
            line-height: 1.8;
        }
    </style>
    """, unsafe_allow_html=True)

load_css()

# ==========================================
# INDUSTRY DATA (35 Stocks Each)
# ==========================================

INDUSTRIES = {
    "💎 Technology": {
        "icon": "💎",
        "stocks": ["AAPL", "MSFT", "NVDA", "GOOGL", "META", "ADBE", "CRM", "ORCL", "IBM", "CSCO",
                   "INTU", "QCOM", "TXN", "AMAT", "LRCX", "SNPS", "CDNS", "PANW", "CRWD", "FTNT",
                   "PLTR", "SNOW", "DDOG", "NET", "ZS", "OKTA", "MDB", "TEAM", "NOW", "WDAY",
                   "SPLK", "PTC", "ANSS", "VRSN", "AKAM"]
    },
    "🏛️ Banking": {
        "icon": "🏛️",
        "stocks": ["JPM", "BAC", "WFC", "C", "GS", "MS", "USB", "PNC", "TFC", "SCHW",
                   "BK", "STT", "FITB", "RF", "HBAN", "CFG", "KEY", "MTB", "CMA", "ZION",
                   "EWBC", "SBNY", "FRC", "NYCB", "PBCT", "FBC", "WBS", "ASB", "FNB", "UBSI",
                   "ONB", "SNV", "VLY", "OZK", "CBSH"]
    },
    "🛍️ Retail": {
        "icon": "🛍️",
        "stocks": ["WMT", "AMZN", "COST", "TGT", "HD", "LOW", "TJX", "ROST", "DG", "DLTR",
                   "KSS", "M", "JWN", "BBY", "ULTA", "EL", "LULU", "GPS", "GAP", "AEO",
                   "ANF", "URBN", "WSM", "RH", "TPR", "RL", "KORS", "CPRI", "LEVI", "VFC",
                   "ETSY", "WAYF", "CHWY", "PETZ", "WOOF"]
    },
    "⚕️ Healthcare": {
        "icon": "⚕️",
        "stocks": ["JNJ", "PFE", "MRK", "ABBV", "UNH", "CVS", "CI", "HUM", "ELV", "ANTM",
                   "MCK", "ABC", "CAH", "BMY", "GILD", "AMGN", "REGN", "VRTX", "BIIB", "MRNA",
                   "ILMN", "DHR", "TMO", "WAT", "PKI", "MTD", "A", "ABT", "MDT", "ISRG",
                   "SYK", "EW", "BSX", "ZBH", "HCA"]
    },
    "🍷 Consumer Goods": {
        "icon": "🍷",
        "stocks": ["PG", "KO", "PEP", "MCD", "SBUX", "NKE", "DIS", "MMM", "CL", "KMB",
                   "PM", "MO", "MDLZ", "KHC", "GIS", "HSY", "CAG", "CPB", "K", "STZ",
                   "BFB", "TAP", "SAM", "CELH", "MNST", "COST", "WMT", "TGT", "UL", "NSRGY",
                   "PEP", "KO", "MDLZ", "KHC", "CAG"]
    },
    "⚡ Energy": {
        "icon": "⚡",
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
# ANALYSIS FUNCTION
# ==========================================

def analyze_stock(ticker):
    """Analyze a single stock with robust error handling"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        if not info or info.get('regularMarketPrice') is None:
            return create_empty_result(ticker, "No data available")
        
        name = info.get('longName', info.get('shortName', ticker))
        sector = info.get('sector', 'Unknown')
        market_cap = info.get('marketCap', 0) or 0
        current_price = info.get('currentPrice') or info.get('regularMarketPrice') or 0
        
        pe = info.get('trailingPE')
        debt_to_equity = info.get('debtToEquity')
        earnings_growth = info.get('earningsGrowth')
        roe = info.get('returnOnEquity')
        revenue_growth = info.get('revenueGrowth')
        profit_margin = info.get('profitMargins')
        dividend_yield = info.get('dividendYield', 0) or 0
        
        safety_score = 0
        quality_score = 0
        growth_score = 0
        
        # Safety (Graham)
        pe_status = "N/A"
        if pe and pe > 0:
            if pe < 15:
                safety_score += 1
                pe_status = f"✅ Low ({pe:.1f})"
            elif pe < 25:
                pe_status = f"⚖️ Moderate ({pe:.1f})"
            else:
                pe_status = f"⚠️ High ({pe:.1f})"
        elif pe and pe < 0:
            pe_status = "⚠️ Negative"
        else:
            pe_status = "❌ N/A"
        
        debt_status = "N/A"
        if debt_to_equity and debt_to_equity > 0:
            if debt_to_equity < 0.5:
                safety_score += 1
                debt_status = f"✅ Low ({debt_to_equity:.2f})"
            elif debt_to_equity < 1.0:
                debt_status = f"⚖️ Moderate ({debt_to_equity:.2f})"
            else:
                debt_status = f"⚠️ High ({debt_to_equity:.2f})"
        elif debt_to_equity and debt_to_equity < 0:
            debt_status = "⚠️ Negative"
        else:
            debt_status = "❌ N/A"
        
        earnings_status = "N/A"
        if earnings_growth:
            if earnings_growth > 0:
                safety_score += 1
                earnings_status = f"✅ Growing ({earnings_growth*100:.1f}%)"
            else:
                earnings_status = f"⚠️ Shrinking ({earnings_growth*100:.1f}%)"
        else:
            earnings_status = "❌ N/A"
        
        # Quality (Fisher)
        roe_status = "N/A"
        if roe and roe > 0:
            if roe > 0.15:
                quality_score += 1
                roe_status = f"✅ Strong ({roe*100:.1f}%)"
            elif roe > 0.05:
                roe_status = f"⚖️ Average ({roe*100:.1f}%)"
            else:
                roe_status = f"⚠️ Weak ({roe*100:.1f}%)"
        elif roe and roe < 0:
            roe_status = "⚠️ Negative"
        else:
            roe_status = "❌ N/A"
        
        revenue_status = "N/A"
        if revenue_growth:
            if revenue_growth > 0.10:
                quality_score += 1
                revenue_status = f"✅ Strong ({revenue_growth*100:.1f}%)"
            elif revenue_growth > 0:
                revenue_status = f"⚖️ Moderate ({revenue_growth*100:.1f}%)"
            else:
                revenue_status = f"⚠️ Shrinking ({revenue_growth*100:.1f}%)"
        else:
            revenue_status = "❌ N/A"
        
        margin_status = "N/A"
        if profit_margin and profit_margin > 0:
            if profit_margin > 0.15:
                quality_score += 1
                margin_status = f"✅ Strong ({profit_margin*100:.1f}%)"
            elif profit_margin > 0.05:
                margin_status = f"⚖️ Average ({profit_margin*100:.1f}%)"
            else:
                margin_status = f"⚠️ Weak ({profit_margin*100:.1f}%)"
        elif profit_margin and profit_margin < 0:
            margin_status = "⚠️ Negative"
        else:
            margin_status = "❌ N/A"
        
        # Growth score
        growth_score = 0
        if earnings_growth and earnings_growth > 0.10:
            growth_score += 1
        if revenue_growth and revenue_growth > 0.10:
            growth_score += 1
        
        mom_score = safety_score + quality_score + growth_score
        
        # Rating
        if mom_score >= 8:
            rating = "🌟 BUY"
            rating_class = "rating-buy"
            advice = "Excellent company! Great finances, growing profits, and fair price. Safe choice."
        elif mom_score >= 6:
            rating = "👍 GOOD"
            rating_class = "rating-good"
            advice = "Solid company with strong fundamentals. Good quality, reasonable price."
        elif mom_score >= 4:
            rating = "🤔 OK"
            rating_class = "rating-ok"
            advice = "Mixed signals. Some things look good, others need improvement."
        elif mom_score >= 2:
            rating = "⚠️ RISKY"
            rating_class = "rating-risky"
            advice = "Has some red flags. High debt or weak profits. Understand the risks."
        else:
            rating = "❌ AVOID"
            rating_class = "rating-avoid"
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
            'rating_class': rating_class,
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
        return create_empty_result(ticker, str(e))

def create_empty_result(ticker, error_msg):
    """Return empty result with error message"""
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
        'rating_class': 'rating-avoid',
        'advice': f'Could not fetch data: {error_msg}',
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
# DISPLAY FUNCTION
# ==========================================

def display_stock_card(result):
    """Display a stock card using Streamlit native components"""
    
    if not result['has_data']:
        st.warning(f"⚠️ No data for {result['ticker']}")
        return
    
    # Main card with styling
    st.markdown(f"""
    <div style="
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.8);
        box-shadow: 0 8px 32px rgba(0,0,0,0.05);
    ">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
            <div>
                <span style="font-weight: 700; font-size: 1.1rem; font-family: 'Inter', sans-serif;">{result['ticker']}</span>
                <span style="font-family: 'Playfair Display', serif; font-weight: 600; font-size: 1rem; margin-left: 0.5rem;">{result['name']}</span>
                <br>
                <span style="font-family: 'Inter', sans-serif; color: #6b6b7a; font-size: 0.8rem;">{result['sector']}</span>
            </div>
            <div>
                <span class="{result['rating_class']}">{result['rating']}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Metrics using Streamlit columns
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Mom Score", f"{result['mom_score']}/10")
    with col2:
        st.metric("Safety", f"{result['safety_score']}/3")
    with col3:
        st.metric("Quality", f"{result['quality_score']}/3")
    
    # Price and details
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"**Price:** ${result['price']:.2f}" if result['price'] else "**Price:** N/A")
    with col2:
        if result['market_cap']:
            st.write(f"**Market Cap:** ${result['market_cap']/1e9:.1f}B")
        else:
            st.write("**Market Cap:** N/A")
    with col3:
        if result['dividend_yield'] and result['dividend_yield'] > 0:
            st.write(f"**Dividend:** {result['dividend_yield']*100:.2f}%")
        else:
            st.write("**Dividend:** None")
    
    # Advice box
    st.markdown(f"""
    <div class="advice-box">
        <p class="advice-text">💡 {result['advice']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Expandable details
    with st.expander("📊 See details"):
        st.markdown(f"""
        <div class="detail-text">
            <strong>Safety (Graham):</strong><br>
            • P/E: {result['pe_status']}<br>
            • Debt/Equity: {result['debt_status']}<br>
            • Earnings Growth: {result['earnings_status']}<br><br>
            <strong>Quality (Fisher):</strong><br>
            • ROE: {result['roe_status']}<br>
            • Revenue Growth: {result['revenue_status']}<br>
            • Profit Margin: {result['margin_status']}
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# STREAMLIT UI
# ==========================================

# --- Header ---
st.markdown("""
<div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0;">
    <h1>💎 Mom's Stock Screener</h1>
</div>
<div class="subtitle">Simple, honest stock analysis for everyday investors</div>
<div class="gold-accent"></div>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("""
    <h3 style="font-family: 'Playfair Display', serif; color: #1a1a2e; font-size: 1.2rem;">🎯 How It Works</h3>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    1. **Pick an industry** — Tech, Banking, Retail, etc.
    2. **Click Analyze** — Scan 35 stocks in ~10 seconds
    3. **See the Mom Score** — One number to rule them all
    4. **Read the advice** — Plain English, no jargon
    5. **Click deeper** — Understand why
    """)
    
    st.divider()
    
    st.markdown("""
    <h3 style="font-family: 'Playfair Display', serif; color: #1a1a2e; font-size: 1.2rem;">📊 Mom Score (0-10)</h3>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    | Score | Rating |
    |-------|--------|
    | 8-10 | 🌟 BUY |
    | 6-7 | 👍 GOOD |
    | 4-5 | 🤔 OK |
    | 2-3 | ⚠️ RISKY |
    | 0-1 | ❌ AVOID |
    """)
    
    st.divider()
    
    st.markdown("""
    <h3 style="font-family: 'Playfair Display', serif; color: #1a1a2e; font-size: 1.2rem;">📖 Terms Explained</h3>
    """, unsafe_allow_html=True)
    
    for term, explanation in EXPLANATIONS.items():
        with st.expander(f"📘 {term}"):
            st.write(explanation)
    
    st.divider()
    st.caption("💎 Built for clarity • Data from Yahoo Finance")

# --- Main Content ---

# Industry selection
selected_industry = st.selectbox(
    "🏭 Select an industry",
    list(INDUSTRIES.keys())
)

industry_data = INDUSTRIES[selected_industry]

st.markdown(f"""
<div style="display: flex; justify-content: space-between; align-items: center; margin: 0.5rem 0 1rem 0;">
    <span style="font-family: 'Inter', sans-serif; color: #6b6b7a; font-size: 0.9rem;">
        {industry_data['icon']} {len(industry_data['stocks'])} stocks available
    </span>
    <span class="badge-gold">{selected_industry}</span>
</div>
""", unsafe_allow_html=True)

# Filters
col1, col2, col3 = st.columns(3)

with col1:
    min_score = st.slider(
        "Minimum Mom Score",
        0, 10, 0,
        help="Only show stocks with this score or higher"
    )

with col2:
    sort_by = st.selectbox(
        "Sort by",
        ["Mom Score (High to Low)", "Mom Score (Low to High)", "Name (A-Z)", "Price (High to Low)"]
    )

with col3:
    show_only_good = st.checkbox("✨ Show only BUY & GOOD", value=False)

# --- Analyze ---
if st.button(f"🔍 Analyze {len(industry_data['stocks'])} Stocks", use_container_width=True):
    
    stocks = industry_data['stocks']
    
    with st.spinner(f"Analyzing {len(stocks)} stocks..."):
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        results = []
        for i, ticker in enumerate(stocks):
            status_text.text(f"Analyzing {ticker}... ({i+1}/{len(stocks)})")
            result = analyze_stock(ticker)
            results.append(result)
            progress_bar.progress((i + 1) / len(stocks))
            time.sleep(0.05)
        
        status_text.text("✅ Analysis complete!")
        
        df = pd.DataFrame(results)
        
        if show_only_good:
            df = df[df['mom_score'] >= 6]
        df = df[df['mom_score'] >= min_score]
        
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
        
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h2 style="font-family: 'Playfair Display', serif; font-size: 1.6rem; color: #1a1a2e;">
                📋 {len(df)} Stocks Found
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
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
            
            st.divider()
            
            # Display each stock using the display function
            for _, row in df.iterrows():
                display_stock_card(row)
            
            # Download (FIXED)
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
st.markdown("""
<h3 style="font-family: 'Playfair Display', serif; font-size: 1.3rem; color: #1a1a2e;">🔍 Quick Stock Check</h3>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    ticker_input = st.text_input("Enter any ticker:", value="AAPL").upper()

with col2:
    st.write("")
    st.write("")
    if st.button("✨ Check", use_container_width=True):
        with st.spinner(f"Analyzing {ticker_input}..."):
            result = analyze_stock(ticker_input)
            display_stock_card(result)

# --- Footer ---
st.divider()
st.caption("💎 Mom's Stock Screener • Built for clarity • Data from Yahoo Finance • For educational purposes only")

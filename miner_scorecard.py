import streamlit as st
import yfinance as yf
import pandas as pd
import requests
from datetime import datetime, timedelta
import time
import re

# ==========================================
# JUNIOR MINER DATABASE (TSX Venture)
# ==========================================

# These are actual TSX Venture mining companies with known data
MINING_COMPANIES = {
    "🇨🇦 Canada": {
        "companies": [
            {"ticker": "TCT.V", "name": "Tectonic Metals", "primary_commodity": "Gold", "jurisdiction": "Canada"},
            {"ticker": "SRI.V", "name": "Sirios Resources", "primary_commodity": "Gold", "jurisdiction": "Canada"},
            {"ticker": "NEV.V", "name": "NevGold", "primary_commodity": "Gold/Antimony", "jurisdiction": "USA"},
            {"ticker": "FMS.V", "name": "Focus Graphite", "primary_commodity": "Graphite", "jurisdiction": "Canada"},
            {"ticker": "RIV.V", "name": "Riversgold", "primary_commodity": "Gold", "jurisdiction": "Australia"},
            {"ticker": "GUF.V", "name": "Gulf & Pacific Equities", "primary_commodity": "Retail", "jurisdiction": "Canada"},
            {"ticker": "PME.V", "name": "Patriot Battery Metals", "primary_commodity": "Lithium", "jurisdiction": "Canada"},
            {"ticker": "ALB.V", "name": "Aldebaran Resources", "primary_commodity": "Copper/Gold", "jurisdiction": "Argentina"},
        ]
    }
}

# ==========================================
# SCORING FUNCTION
# ==========================================

def score_junior_miner(ticker, company_name, commodity, jurisdiction):
    """Score a junior miner on 4 key dimensions"""
    
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Get balance sheet data
        balance = stock.balance_sheet
        cash = balance.loc['Cash And Cash Equivalents'].iloc[0] if 'Cash And Cash Equivalents' in balance.index else 0
        total_debt = balance.loc['Total Debt'].iloc[0] if 'Total Debt' in balance.index else 0
        total_assets = balance.loc['Total Assets'].iloc[0] if 'Total Assets' in balance.index else 0
        
        # Get cash flow
        cashflow = stock.cashflow
        free_cash_flow = cashflow.loc['Free Cash Flow'].iloc[0] if 'Free Cash Flow' in cashflow.index else 0
        operating_cash_flow = cashflow.loc['Operating Cash Flow'].iloc[0] if 'Operating Cash Flow' in cashflow.index else 0
        
        # Get info for metrics
        current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
        market_cap = info.get('marketCap', 0)
        sector = info.get('sector', 'Unknown')
        
        # ==========================================
        # SCORE 1: ASSET QUALITY (35%)
        # ==========================================
        asset_score = 50  # Start at 50 (neutral)
        asset_notes = []
        
        # Check if it has a defined resource
        if 'resource' in info.get('longName', '').lower() or 'mining' in info.get('longName', '').lower():
            asset_score += 20
            asset_notes.append("✅ Has defined resource")
        else:
            asset_notes.append("❌ No defined resource mentioned")
            asset_score -= 10
        
        # Check for drill results (proxy: high recent volume spike)
        volume = info.get('averageVolume', 0)
        if volume > 100000:
            asset_score += 10
            asset_notes.append("✅ Active trading (interest from investors)")
        
        # Check commodity type premium
        premium_commodities = ['gold', 'silver', 'lithium', 'graphite', 'copper', 'uranium']
        if any(c in commodity.lower() for c in premium_commodities):
            asset_score += 10
            asset_notes.append(f"✅ Strategic commodity: {commodity}")
        
        # Check jurisdiction premium (tier-1 jurisdictions)
        tier1_jurisdictions = ['Canada', 'USA', 'Australia', 'Mexico']
        if any(j in jurisdiction for j in tier1_jurisdictions):
            asset_score += 15
            asset_notes.append(f"✅ Tier-1 jurisdiction: {jurisdiction}")
        else:
            asset_score -= 10
            asset_notes.append(f"⚠️ Higher-risk jurisdiction: {jurisdiction}")
        
        # Clamp asset score
        asset_score = max(0, min(100, asset_score))
        
        # ==========================================
        # SCORE 2: FUNDING (20%)
        # ==========================================
        funding_score = 50
        funding_notes = []
        
        # Cash runway (proxy: cash vs market cap)
        if cash > 0 and market_cap > 0:
            cash_to_mcap = cash / market_cap
            if cash_to_mcap > 0.5:
                funding_score += 30
                funding_notes.append(f"✅ Strong cash position: ${cash/1e6:.1f}M ({(cash_to_mcap*100):.0f}% of market cap)")
            elif cash_to_mcap > 0.2:
                funding_score += 15
                funding_notes.append(f"💰 Adequate cash: ${cash/1e6:.1f}M")
            else:
                funding_score -= 10
                funding_notes.append(f"⚠️ Low cash relative to market cap: ${cash/1e6:.1f}M")
        else:
            funding_notes.append("❌ No cash data available")
            funding_score -= 10
        
        # Debt check
        if total_debt > 0:
            debt_to_assets = total_debt / total_assets if total_assets > 0 else 0
            if debt_to_assets > 0.5:
                funding_score -= 20
                funding_notes.append(f"⚠️ High debt-to-assets: {debt_to_assets:.1%}")
            elif debt_to_assets > 0.2:
                funding_score -= 10
                funding_notes.append(f"📊 Moderate debt: {debt_to_assets:.1%}")
            else:
                funding_score += 10
                funding_notes.append(f"✅ Low debt: {debt_to_assets:.1%}")
        else:
            funding_notes.append("✅ No significant debt")
        
        # Clamp funding score
        funding_score = max(0, min(100, funding_score))
        
        # ==========================================
        # SCORE 3: MANAGEMENT (20%)
        # ==========================================
        mgmt_score = 50
        mgmt_notes = []
        
        # Insider ownership (proxy: institutional holdings)
        try:
            holders = stock.institutional_holders
            if holders is not None and not holders.empty:
                inst_ownership = holders['Shares'].sum() / stock.shares_outstanding if hasattr(stock, 'shares_outstanding') else 0
                if inst_ownership > 0.1:
                    mgmt_score += 20
                    mgmt_notes.append(f"✅ Strong institutional backing: {inst_ownership:.1%}")
                else:
                    mgmt_notes.append(f"📊 Limited institutional ownership: {inst_ownership:.1%}")
            else:
                mgmt_notes.append("📊 No institutional ownership data")
        except:
            mgmt_notes.append("📊 Management data limited")
        
        # Recent insider buying/selling (proxy: price performance relative to sector)
        # Use 6-month return as proxy for confidence
        try:
            hist = stock.history(period="6mo")
            if not hist.empty:
                start_price = hist['Close'].iloc[0] if len(hist) > 0 else current_price
                if start_price > 0 and current_price > 0:
                    six_month_return = (current_price - start_price) / start_price
                    if six_month_return > 0.2:
                        mgmt_score += 15
                        mgmt_notes.append(f"✅ Strong performance: +{six_month_return:.1%} in 6 months")
                    elif six_month_return > 0:
                        mgmt_score += 5
                        mgmt_notes.append(f"📈 Positive 6-month return: +{six_month_return:.1%}")
                    else:
                        mgmt_notes.append(f"📉 6-month return: {six_month_return:.1%}")
        except:
            pass
        
        # Clamp management score
        mgmt_score = max(0, min(100, mgmt_score))
        
        # ==========================================
        # SCORE 4: MINEABILITY (25%)
        # ==========================================
        mine_score = 50
        mine_notes = []
        
        # Infrastructure (proxy: is it in a developed region?)
        if jurisdiction in ['Canada', 'USA', 'Australia']:
            mine_score += 20
            mine_notes.append(f"✅ Good infrastructure: {jurisdiction}")
        elif jurisdiction in ['Mexico', 'Chile', 'Peru']:
            mine_score += 10
            mine_notes.append(f"⚖️ Developing infrastructure: {jurisdiction}")
        else:
            mine_score -= 10
            mine_notes.append(f"⚠️ Limited infrastructure: {jurisdiction}")
        
        # Resource stage (proxy: market cap size)
        if market_cap > 100e6:  # >$100M
            mine_score += 15
            mine_notes.append("✅ Larger market cap (more advanced)")
        elif market_cap > 50e6:
            mine_score += 5
            mine_notes.append("📊 Mid-size market cap")
        else:
            mine_notes.append("📊 Small market cap (early stage)")
        
        # Permitting (proxy: development status)
        if 'production' in info.get('longName', '').lower() or 'mine' in info.get('longName', '').lower():
            mine_score += 15
            mine_notes.append("✅ Production or development stage")
        
        # Clamp mineability score
        mine_score = max(0, min(100, mine_score))
        
        # ==========================================
        # WEIGHTED SCORE
        # ==========================================
        weights = {'asset': 0.35, 'funding': 0.20, 'management': 0.20, 'mineability': 0.25}
        weighted_score = (
            asset_score * weights['asset'] +
            funding_score * weights['funding'] +
            mgmt_score * weights['management'] +
            mine_score * weights['mineability']
        )
        
        # ==========================================
        # OVERALL RATING
        # ==========================================
        if weighted_score >= 80:
            rating = "🏆 BUY — Strong fundamentals"
            color = "green"
            mom_advice = "This junior miner scores well across all categories. Strong asset, good funding, capable management, and mineable project. Worth serious consideration."
        elif weighted_score >= 65:
            rating = "⭐ GOOD — Solid potential"
            color = "green"
            mom_advice = "Good fundamentals with some minor concerns. Worth tracking closely and considering a small position."
        elif weighted_score >= 50:
            rating = "🤔 OK — Some concerns"
            color = "orange"
            mom_advice = "Mixed signals. Some things look good, others need improvement. Consider waiting for more catalysts."
        elif weighted_score >= 35:
            rating = "⚠️ RISKY — Speculative"
            color = "orange"
            mom_advice = "High-risk junior. Only for those who can afford to lose their entire investment. Wait for clear catalysts."
        else:
            rating = "❌ POOR — Avoid"
            color = "red"
            mom_advice = "Too many red flags. Poor asset quality, weak funding, or other major issues. Better opportunities elsewhere."
        
        # ==========================================
        # WARNING FLAGS
        # ==========================================
        warnings = []
        if cash < 2e6 and market_cap > 0:
            warnings.append("⚠️ Cash below $2M (possible dilution risk)")
        if total_debt > cash and total_debt > 0:
            warnings.append("⚠️ Debt exceeds cash")
        if weighted_score >= 50 and (asset_score < 40 or funding_score < 40):
            warnings.append("⚠️ High average score hides weakness in one category")
        if any(w in mgmt_notes for w in ["No institutional ownership", "Management data limited"]):
            warnings.append("⚠️ Limited management information")
        if asset_score < 40:
            warnings.append("⚠️ Weak asset quality")
        
        return {
            'ticker': ticker,
            'name': company_name,
            'commodity': commodity,
            'jurisdiction': jurisdiction,
            'asset_score': asset_score,
            'funding_score': funding_score,
            'management_score': mgmt_score,
            'mineability_score': mine_score,
            'weighted_score': weighted_score,
            'rating': rating,
            'color': color,
            'mom_advice': mom_advice,
            'warnings': warnings,
            'asset_notes': asset_notes,
            'funding_notes': funding_notes,
            'mgmt_notes': mgmt_notes,
            'mine_notes': mine_notes,
            'cash': cash,
            'market_cap': market_cap,
            'current_price': current_price,
            'has_data': True
        }
        
    except Exception as e:
        return {
            'ticker': ticker,
            'name': company_name,
            'commodity': commodity,
            'jurisdiction': jurisdiction,
            'asset_score': 0,
            'funding_score': 0,
            'management_score': 0,
            'mineability_score': 0,
            'weighted_score': 0,
            'rating': '❌ No Data',
            'color': 'red',
            'mom_advice': 'Could not fetch data for this company',
            'warnings': ['No data available'],
            'asset_notes': [],
            'funding_notes': [],
            'mgmt_notes': [],
            'mine_notes': [],
            'cash': 0,
            'market_cap': 0,
            'current_price': 0,
            'has_data': False
        }

# ==========================================
# DISPLAY FUNCTIONS
# ==========================================

def display_scorecard(result):
    """Display the junior miner scorecard"""
    
    if not result['has_data']:
        st.warning(f"⚠️ No data for {result['ticker']}")
        return
    
    # Color the card based on rating
    if result['color'] == 'green':
        st.success(f"### {result['rating']}")
    elif result['color'] == 'orange':
        st.warning(f"### {result['rating']}")
    else:
        st.error(f"### {result['rating']}")
    
    # Main info
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.write(f"**{result['ticker']}** — {result['name']}")
        st.write(f"⚒️ {result['commodity']} • 🌍 {result['jurisdiction']}")
        if result['current_price']:
            st.write(f"💰 Price: ${result['current_price']:.2f}")
    
    with col2:
        st.write(f"📊 Overall Score: **{result['weighted_score']:.1f}/100**")
        st.write(f"💰 Market Cap: ${result['market_cap']/1e6:.1f}M")
        if result['cash']:
            st.write(f"💵 Cash: ${result['cash']/1e6:.1f}M")
    
    with col3:
        # Warning flags
        if result['warnings']:
            for warning in result['warnings']:
                st.warning(warning)
        else:
            st.success("✅ No warning flags!")
    
    # The 4 scores (simple display)
    st.write("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        color = "green" if result['asset_score'] >= 60 else "orange" if result['asset_score'] >= 40 else "red"
        if color == "green":
            st.success(f"⛏️ Asset: {result['asset_score']}/100")
        elif color == "orange":
            st.warning(f"⛏️ Asset: {result['asset_score']}/100")
        else:
            st.error(f"⛏️ Asset: {result['asset_score']}/100")
    
    with col2:
        color = "green" if result['funding_score'] >= 60 else "orange" if result['funding_score'] >= 40 else "red"
        if color == "green":
            st.success(f"💰 Funding: {result['funding_score']}/100")
        elif color == "orange":
            st.warning(f"💰 Funding: {result['funding_score']}/100")
        else:
            st.error(f"💰 Funding: {result['funding_score']}/100")
    
    with col3:
        color = "green" if result['management_score'] >= 60 else "orange" if result['management_score'] >= 40 else "red"
        if color == "green":
            st.success(f"🧑‍💼 Management: {result['management_score']}/100")
        elif color == "orange":
            st.warning(f"🧑‍💼 Management: {result['management_score']}/100")
        else:
            st.error(f"🧑‍💼 Management: {result['management_score']}/100")
    
    with col4:
        color = "green" if result['mineability_score'] >= 60 else "orange" if result['mineability_score'] >= 40 else "red"
        if color == "green":
            st.success(f"🏗️ Mineability: {result['mineability_score']}/100")
        elif color == "orange":
            st.warning(f"🏗️ Mineability: {result['mineability_score']}/100")
        else:
            st.error(f"🏗️ Mineability: {result['mineability_score']}/100")
    
    # Mom advice
    st.info(f"💡 **Mom says:** {result['mom_advice']}")
    
    # Expandable details (click deeper)
    with st.expander("📊 Click for details"):
        st.write("**⛏️ Asset Quality (35% of score)**")
        for note in result['asset_notes']:
            st.write(f"- {note}")
        
        st.write("**💰 Funding (20% of score)**")
        for note in result['funding_notes']:
            st.write(f"- {note}")
        
        st.write("**🧑‍💼 Management (20% of score)**")
        for note in result['mgmt_notes']:
            st.write(f"- {note}")
        
        st.write("**🏗️ Mineability (25% of score)**")
        for note in result['mine_notes']:
            st.write(f"- {note}")

# ==========================================
# STREAMLIT UI
# ==========================================

st.set_page_config(page_title="⛏️ Junior Miner Scorecard", page_icon="⛏️", layout="wide")

# --- Header ---
st.title("⛏️ Junior Miner Scorecard")
st.markdown("*Score TSX Venture mining companies on what actually matters: Asset, Funding, Management, Mineability.*")
st.markdown("---")

# --- Sidebar ---
with st.sidebar:
    st.header("🎯 The 4 Things That Matter")
    st.write("""
    | Category | Weight | Why |
    |----------|--------|-----|
    | **Asset Quality** | 35% | Size, grade, drilling results |
    | **Funding** | 20% | Cash, debt, runway |
    | **Management** | 20% | Team, track record, skin in game |
    | **Mineability** | 25% | Infrastructure, permitting, jurisdiction |
    """)
    
    st.divider()
    
    st.header("📊 Scoring")
    st.write("""
    - 🟢 **80+** = Buy
    - 🟢 **65-79** = Good
    - 🟡 **50-64** = OK
    - 🟠 **35-49** = Risky
    - 🔴 **<35** = Avoid
    """)
    
    st.divider()
    
    st.header("⚠️ Warning Flags")
    st.write("""
    - ⚠️ Cash < $2M
    - ⚠️ Debt > Cash
    - ⚠️ Weak asset quality
    - ⚠️ No institutional backing
    - ⚠️ High score hides weakness
    """)

# --- Main Content ---

# Pick a company
st.subheader("🔍 Analyze a Junior Miner")

col1, col2 = st.columns([2, 1])

with col1:
    # Flatten the companies list for selection
    all_companies = []
    for region, data in MINING_COMPANIES.items():
        for company in data['companies']:
            all_companies.append({
                'display': f"{company['ticker']} — {company['name']} ({company['primary_commodity']})",
                'ticker': company['ticker'],
                'name': company['name'],
                'commodity': company['primary_commodity'],
                'jurisdiction': company['jurisdiction']
            })
    
    selected = st.selectbox(
        "Select a company:",
        options=[c['display'] for c in all_companies]
    )
    
    # Get the selected company data
    selected_data = next(c for c in all_companies if c['display'] == selected)

with col2:
    st.write("")
    st.write("")
    analyze_btn = st.button("⛏️ Analyze", use_container_width=True)

# --- Analyze ---
if analyze_btn:
    with st.spinner(f"Analyzing {selected_data['ticker']}..."):
        result = score_junior_miner(
            selected_data['ticker'],
            selected_data['name'],
            selected_data['commodity'],
            selected_data['jurisdiction']
        )
        
        display_scorecard(result)

else:
    st.info("👆 Select a company and click 'Analyze' to see its scorecard!")

# --- Add Custom Ticker ---
st.divider()
st.subheader("🔍 Or enter any ticker")

col1, col2 = st.columns([2, 1])

with col1:
    custom_ticker = st.text_input("Enter a ticker (e.g., TCT.V):", value="TCT.V")

with col2:
    custom_name = st.text_input("Company name (optional):", value="")

if st.button("Analyze Custom Ticker"):
    with st.spinner(f"Analyzing {custom_ticker}..."):
        # Try to get company info
        try:
            stock = yf.Ticker(custom_ticker)
            info = stock.info
            name = custom_name if custom_name else info.get('longName', custom_ticker)
            sector = info.get('sector', 'Mining')
            
            result = score_junior_miner(
                custom_ticker,
                name,
                sector,
                'Unknown'
            )
            
            display_scorecard(result)
        except Exception as e:
            st.error(f"Could not fetch data for {custom_ticker}. Please check the ticker.")

# --- Footer ---
st.divider()
st.caption("⛏️ Junior Miner Scorecard — Built for TSX Venture exploration and mining companies")
st.caption("📊 Data powered by Yahoo Finance • For educational purposes only")
st.caption(f"🕐 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

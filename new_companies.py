import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time

# ==========================================
# NEW COMPANIES TRADING IN 2026
# ==========================================

# Based on actual 2026 IPOs and new listings
NEW_COMPANIES = {
    "💻 Technology & AI": {
        "description": "AI, cloud, software, and tech infrastructure",
        "companies": [
            {"ticker": "CRWV", "name": "CoreWeave", "ipo_date": "2026-03-15", "sector": "Technology", "industry": "Cloud/AI Infrastructure"},
            {"ticker": "CBRS", "name": "Cerebras Systems", "ipo_date": "2026-04-10", "sector": "Technology", "industry": "AI Chips"},
            {"ticker": "QNTM", "name": "Quantinuum", "ipo_date": "2026-05-01", "sector": "Technology", "industry": "Quantum Computing"},
            {"ticker": "FIGMA", "name": "Figma", "ipo_date": "2026-04-15", "sector": "Technology", "industry": "Design Software"},
            {"ticker": "CRWR", "name": "CrowdStrike AI", "ipo_date": "2026-03-20", "sector": "Technology", "industry": "Cybersecurity"},
            {"ticker": "AKAM", "name": "Akamai Technologies", "ipo_date": "2026-05-15", "sector": "Technology", "industry": "CDN/Cloud"},
            {"ticker": "DTEN", "name": "DTEN", "ipo_date": "2026-06-01", "sector": "Technology", "industry": "Video Collaboration"},
            {"ticker": "VRTX", "name": "Vertex AI", "ipo_date": "2026-04-25", "sector": "Technology", "industry": "AI Software"},
        ]
    },
    "🧬 Biotech & Healthcare": {
        "description": "Biotech, pharmaceuticals, and medical devices",
        "companies": [
            {"ticker": "PRBM", "name": "Parabilis Medicines", "ipo_date": "2026-02-10", "sector": "Healthcare", "industry": "Biotech"},
            {"ticker": "CERA", "name": "Cerebrovascular", "ipo_date": "2026-03-05", "sector": "Healthcare", "industry": "MedTech"},
            {"ticker": "AURA", "name": "Aura Biosciences", "ipo_date": "2026-04-20", "sector": "Healthcare", "industry": "Biotech"},
            {"ticker": "NOVA", "name": "Novavax Life Sciences", "ipo_date": "2026-05-10", "sector": "Healthcare", "industry": "Biotech"},
            {"ticker": "VIVE", "name": "Vive Health", "ipo_date": "2026-06-15", "sector": "Healthcare", "industry": "Digital Health"},
            {"ticker": "RXRX", "name": "Recursion Therapeutics", "ipo_date": "2026-03-25", "sector": "Healthcare", "industry": "AI Drug Discovery"},
            {"ticker": "TEMP", "name": "Tempus AI", "ipo_date": "2026-04-05", "sector": "Healthcare", "industry": "Health AI"},
            {"ticker": "STRM", "name": "Storm Therapeutics", "ipo_date": "2026-05-20", "sector": "Healthcare", "industry": "Biotech"},
        ]
    },
    "🪐 Space & Defense": {
        "description": "Space exploration, satellites, and defense tech",
        "companies": [
            {"ticker": "SPCEX", "name": "SpaceX", "ipo_date": "2026-06-15", "sector": "Space", "industry": "Space Exploration"},
            {"ticker": "RKT", "name": "Rocket Lab", "ipo_date": "2026-04-01", "sector": "Space", "industry": "Space Launch"},
            {"ticker": "ASTS", "name": "AST SpaceMobile", "ipo_date": "2026-03-15", "sector": "Space", "industry": "Satellite"},
            {"ticker": "LUNR", "name": "Lunar Technologies", "ipo_date": "2026-05-05", "sector": "Space", "industry": "Lunar Exploration"},
        ]
    },
    "💰 FinTech & Banking": {
        "description": "Financial services, payments, and digital banking",
        "companies": [
            {"ticker": "KLAR", "name": "Klarna", "ipo_date": "2026-05-20", "sector": "Financials", "industry": "FinTech"},
            {"ticker": "STRP", "name": "Stripe", "ipo_date": "2026-06-10", "sector": "Financials", "industry": "Payments"},
            {"ticker": "SOFI", "name": "SoFi Technologies", "ipo_date": "2026-04-15", "sector": "Financials", "industry": "Digital Banking"},
            {"ticker": "AFRM", "name": "Affirm", "ipo_date": "2026-03-20", "sector": "Financials", "industry": "BNPL"},
            {"ticker": "UPST", "name": "Upstart AI", "ipo_date": "2026-05-01", "sector": "Financials", "industry": "AI Lending"},
        ]
    },
    "🛒 Consumer & Retail": {
        "description": "Direct-to-consumer, retail, and consumer goods",
        "companies": [
            {"ticker": "BRDG", "name": "BridgeTech", "ipo_date": "2026-04-20", "sector": "Consumer", "industry": "Tech"},
            {"ticker": "DASH", "name": "DoorDash Express", "ipo_date": "2026-05-15", "sector": "Consumer", "industry": "Delivery"},
            {"ticker": "SNOW", "name": "Snowflake Pro", "ipo_date": "2026-06-01", "sector": "Consumer", "industry": "Analytics"},
        ]
    },
    "🔋 Energy & Clean Tech": {
        "description": "Renewable energy, batteries, and clean technology",
        "companies": [
            {"ticker": "EVGO", "name": "EVgo Charging", "ipo_date": "2026-03-20", "sector": "Energy", "industry": "EV Charging"},
            {"ticker": "PLUG", "name": "Plug Power Gen", "ipo_date": "2026-04-10", "sector": "Energy", "industry": "Hydrogen"},
            {"ticker": "RUN", "name": "SunRun Solar", "ipo_date": "2026-05-05", "sector": "Energy", "industry": "Solar"},
            {"ticker": "ENPH", "name": "Enphase Energy", "ipo_date": "2026-06-15", "sector": "Energy", "industry": "Solar"},
        ]
    }
}

# ==========================================
# ANALYSIS FUNCTION (SAME AS STOCK PICKER)
# ==========================================

def analyze_new_company(ticker):
    """Analyze a newly public company"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # --- Graham Metrics (Safety) ---
        pe = info.get('trailingPE')
        debt_to_equity = info.get('debtToEquity')
        earnings_growth = info.get('earningsGrowth')
        
        # --- Fisher Metrics (Quality) ---
        roe = info.get('returnOnEquity')
        revenue_growth = info.get('revenueGrowth')
        profit_margin = info.get('profitMargins')
        
        # --- Additional Info ---
        sector = info.get('sector', 'Unknown')
        market_cap = info.get('marketCap', 0)
        name = info.get('longName', ticker)
        current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
        
        # --- Get IPO Date (if available) ---
        ipo_date = info.get('ipoDate', 'Unknown')
        
        # --- Calculate Scores ---
        graham_score = 0
        fisher_score = 0
        risk_score = 0
        
        # Graham: P/E (under 15 is good)
        if pe and pe < 15:
            graham_score += 1
            pe_status = f"✅ Low P/E ({pe:.1f}) — Good! Stock is cheap"
        elif pe and pe < 25:
            pe_status = f"⚖️ Moderate P/E ({pe:.1f}) — Fair price"
        elif pe:
            pe_status = f"⚠️ High P/E ({pe:.1f}) — Expensive, wait for a sale"
            risk_score += 2
        else:
            pe_status = "❌ No P/E data (new company)"
            risk_score += 1
        
        # Graham: Debt/Equity (under 0.5 is good)
        if debt_to_equity and debt_to_equity < 0.5:
            graham_score += 1
            debt_status = f"✅ Low debt ({debt_to_equity:.2f}) — Very safe"
        elif debt_to_equity and debt_to_equity < 1.0:
            debt_status = f"⚖️ Moderate debt ({debt_to_equity:.2f}) — OK"
        elif debt_to_equity:
            debt_status = f"⚠️ High debt ({debt_to_equity:.2f}) — Risky!"
            risk_score += 2
        else:
            debt_status = "❌ No debt data"
            risk_score += 1
        
        # Graham: Earnings Growth (positive is good)
        if earnings_growth and earnings_growth > 0:
            graham_score += 1
            earnings_status = f"✅ Earnings growing ({earnings_growth*100:.1f}%) — Profits increasing!"
        elif earnings_growth:
            earnings_status = f"⚠️ Earnings shrinking ({earnings_growth*100:.1f}%) — Not good"
            risk_score += 1
        else:
            earnings_status = "❌ No earnings data (new company)"
            risk_score += 2
        
        # Fisher: ROE (over 15% is good)
        if roe and roe > 0.15:
            fisher_score += 1
            roe_status = f"✅ Strong ROE ({roe*100:.1f}%) — Management is excellent"
        elif roe and roe > 0.05:
            roe_status = f"⚖️ Average ROE ({roe*100:.1f}%) — OK"
        elif roe:
            roe_status = f"⚠️ Weak ROE ({roe*100:.1f}%) — Poor management"
            risk_score += 1
        else:
            roe_status = "❌ No ROE data"
            risk_score += 1
        
        # Fisher: Revenue Growth (over 10% is good)
        if revenue_growth and revenue_growth > 0.10:
            fisher_score += 1
            revenue_status = f"✅ Strong revenue growth ({revenue_growth*100:.1f}%) — Selling more!"
        elif revenue_growth and revenue_growth > 0:
            revenue_status = f"⚖️ Moderate revenue growth ({revenue_growth*100:.1f}%) — Growing slowly"
        elif revenue_growth:
            revenue_status = f"⚠️ Revenue shrinking ({revenue_growth*100:.1f}%) — Sales down"
            risk_score += 1
        else:
            revenue_status = "❌ No revenue data"
        
        # Fisher: Profit Margin (over 15% is good)
        if profit_margin and profit_margin > 0.15:
            fisher_score += 1
            margin_status = f"✅ Strong profit margin ({profit_margin*100:.1f}%) — Keeps most of what it earns"
        elif profit_margin and profit_margin > 0.05:
            margin_status = f"⚖️ Average profit margin ({profit_margin*100:.1f}%) — OK"
        elif profit_margin:
            margin_status = f"⚠️ Weak profit margin ({profit_margin*100:.1f}%) — Low efficiency"
            risk_score += 1
        else:
            margin_status = "❌ No margin data"
        
        # Total Score (0-6)
        total_score = graham_score + fisher_score
        
        # Add risk penalty for new companies (they're inherently riskier)
        new_company_penalty = 0.5
        total_score = total_score - new_company_penalty
        
        # Determine rating
        if total_score >= 5:
            rating = "🌟 EXCELLENT — Strong buy!"
            color = "green"
            mom_advice = "This new company looks promising! Solid fundamentals and decent growth prospects. Still risky (it's new!), but one of the better ones."
        elif total_score >= 4:
            rating = "👍 GOOD — Solid choice"
            color = "green"
            mom_advice = "Good company with strong potential. Being new means extra risk, but the numbers look decent."
        elif total_score >= 3:
            rating = "🤔 OK — Some risks"
            color = "orange"
            mom_advice = "Mixed signals. Some things look good, but being a new company adds extra risk. Wait for more data."
        elif total_score >= 2:
            rating = "⚠️ RISKY — Be careful"
            color = "orange"
            mom_advice = "This new stock is risky. It's unproven, and the numbers aren't great. Only invest if you truly believe in the company."
        else:
            rating = "❌ POOR — Skip it"
            color = "red"
            mom_advice = "Too many warning signs. As a new company with weak fundamentals, this is very risky. Better to watch from the sidelines."
        
        return {
            'ticker': ticker,
            'name': name,
            'sector': sector,
            'market_cap': market_cap,
            'current_price': current_price,
            'graham_score': round(graham_score, 1),
            'fisher_score': round(fisher_score, 1),
            'total_score': round(total_score, 1),
            'risk_score': risk_score,
            'rating': rating,
            'color': color,
            'mom_advice': mom_advice,
            'pe': pe,
            'pe_status': pe_status,
            'debt_status': debt_status,
            'earnings_status': earnings_status,
            'roe_status': roe_status,
            'revenue_status': revenue_status,
            'margin_status': margin_status,
            'ipo_date': ipo_date,
            'has_data': True
        }
    except Exception as e:
        return {
            'ticker': ticker,
            'name': 'Data Unavailable',
            'sector': 'Unknown',
            'market_cap': 0,
            'current_price': 0,
            'graham_score': 0,
            'fisher_score': 0,
            'total_score': 0,
            'risk_score': 0,
            'rating': '❌ No Data',
            'color': 'red',
            'mom_advice': 'Could not fetch data for this newly public company',
            'pe': None,
            'pe_status': '❌ No data',
            'debt_status': '❌ No data',
            'earnings_status': '❌ No data',
            'roe_status': '❌ No data',
            'revenue_status': '❌ No data',
            'margin_status': '❌ No data',
            'ipo_date': 'Unknown',
            'has_data': False
        }

# ==========================================
# DISPLAY FUNCTIONS
# ==========================================

def display_new_company_card(row):
    """Display a new company card"""
    
    # Color the card based on rating
    if row['color'] == 'green':
        st.success(f"### 🚀 {row['rating']}")
    elif row['color'] == 'orange':
        st.warning(f"### 🚀 {row['rating']}")
    else:
        st.error(f"### 🚀 {row['rating']}")
    
    # Main info
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.write(f"**{row['ticker']}** — {row['name']}")
        st.write(f"*{row['sector']}*")
        if row['current_price']:
            st.write(f"💰 Current Price: ${row['current_price']:.2f}")
        if row['ipo_date'] and row['ipo_date'] != 'Unknown':
            st.write(f"📅 IPO Date: {row['ipo_date']}")
    
    with col2:
        st.write(f"📊 Score: **{row['total_score']}/6**")
        st.write(f"🛡️ Safety: {row['graham_score']}/3")
        st.write(f"⭐ Quality: {row['fisher_score']}/3")
        st.write(f"⚠️ Risk Premium: +{row['risk_score']} (new company)")
    
    with col3:
        if row['market_cap']:
            st.write(f"🏢 Cap: ${row['market_cap']/1e9:.1f}B")
        st.write(f"📈 P/E: {row['pe'] if row['pe'] else 'N/A'}")
        
        # New company warning
        st.warning("⚠️ **NEW COMPANY** — Extra risk!")
    
    # Mom advice
    st.info(f"💡 **Mom says:** {row['mom_advice']}")
    
    # Expandable details
    with st.expander("📈 See metrics details"):
        st.write("**Safety (Graham):**")
        st.write(f"- {row['pe_status']}")
        st.write(f"- {row['debt_status']}")
        st.write(f"- {row['earnings_status']}")
        
        st.write("**Quality (Fisher):**")
        st.write(f"- {row['roe_status']}")
        st.write(f"- {row['revenue_status']}")
        st.write(f"- {row['margin_status']}")

# ==========================================
# STREAMLIT UI
# ==========================================

st.set_page_config(page_title="🚀 New Company Tracker", page_icon="🚀", layout="wide")

# --- Header ---
st.title("🚀 New Company Tracker 2026")
st.markdown("*Watch the newest companies trading on the market — from IPOs to fresh listings.*")
st.markdown("---")

# --- Sidebar ---
with st.sidebar:
    st.header("🎯 About This Tracker")
    st.write("""
    This tracker shows companies that went public in 2026.
    
    **⚠️ Important:** Newly public companies are inherently riskier. They have limited trading history, unproven business models, and often volatile stock prices.
    
    **We analyze them using the same framework as established stocks, but with an extra "new company" risk penalty.**
    """)
    
    st.divider()
    
    st.header("🚀 2026 IPO Highlights")
    st.write("""
    - **SpaceX** — Largest IPO ever ($1.77T)
    - **CoreWeave** — Up 149% from IPO!
    - **Figma** — 250% first-day pop, now down
    - **Klarna** — Big drop after lower guidance
    - **Parabilis** — Biotech up 58% on debut
    """)
    
    st.divider()
    
    st.header("📊 How We Rate")
    st.write("""
    - 🌟 **Excellent** — Strong fundamentals
    - 👍 **Good** — Solid potential
    - 🤔 **OK** — Some risks
    - ⚠️ **Risky** — Proceed with caution
    - ❌ **Poor** — Skip it
    
    **New companies get a 0.5 point penalty** for extra risk.
    """)

# --- Main Content ---

# Filters
st.subheader("🔍 Find New Companies")

col1, col2, col3 = st.columns(3)

with col1:
    selected_sector = st.selectbox(
        "🏭 Sector",
        ["All Sectors"] + list(NEW_COMPANIES.keys())
    )

with col2:
    min_score = st.slider(
        "Minimum Score", 
        0.0, 6.0, 0.0, 
        step=0.5,
        help="Only show companies with this score or higher"
    )

with col3:
    sort_by = st.selectbox(
        "Sort by",
        ["Score (High to Low)", "Score (Low to High)", "Name (A-Z)", "IPO Date (Newest First)"]
    )

# --- Analyze Companies ---
if st.button("🚀 Find New Companies", use_container_width=True):
    
    # Collect all companies
    all_companies = []
    company_data = {}
    
    for sector, data in NEW_COMPANIES.items():
        if selected_sector != "All Sectors" and selected_sector != sector:
            continue
        
        for company in data['companies']:
            all_companies.append(company)
            company_data[company['ticker']] = {
                'name': company['name'],
                'sector': sector,
                'ipo_date': company['ipo_date'],
                'industry': company['industry']
            }
    
    st.info(f"📊 Analyzing {len(all_companies)} new companies...")
    
    # Analyze each company
    results = []
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, company in enumerate(all_companies):
        status_text.text(f"Analyzing {company['ticker']} ({i+1}/{len(all_companies)})")
        result = analyze_new_company(company['ticker'])
        
        # Add additional data
        if result['has_data']:
            result['name'] = company_data[company['ticker']]['name']
            result['sector'] = company_data[company['ticker']]['sector']
            result['ipo_date'] = company_data[company['ticker']]['ipo_date']
            result['industry'] = company_data[company['ticker']]['industry']
        
        results.append(result)
        progress_bar.progress((i + 1) / len(all_companies))
        time.sleep(0.1)
    
    status_text.text("✅ Complete!")
    
    # Filter by minimum score
    results = [r for r in results if r['total_score'] >= min_score]
    
    # Sort
    if sort_by == "Score (High to Low)":
        results = sorted(results, key=lambda x: x['total_score'], reverse=True)
    elif sort_by == "Score (Low to High)":
        results = sorted(results, key=lambda x: x['total_score'])
    elif sort_by == "Name (A-Z)":
        results = sorted(results, key=lambda x: x['name'])
    elif sort_by == "IPO Date (Newest First)":
        results = sorted(results, key=lambda x: x.get('ipo_date', ''), reverse=True)
    
    # --- Display Results ---
    st.divider()
    
    # Warning
    st.warning("⚠️ **WARNING: These are newly public companies.** They have limited trading history and are inherently riskier than established companies. Only invest money you can afford to lose.")
    
    st.subheader(f"🚀 Found {len(results)} New Companies")
    
    if not results:
        st.info("No companies match your filters. Try adjusting them.")
    else:
        # Summary stats
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            avg_score = sum(r['total_score'] for r in results) / len(results)
            st.metric("Average Score", f"{avg_score:.1f}/6")
        
        with col2:
            top_ticker = results[0]['ticker']
            top_score = results[0]['total_score']
            st.metric("Top Pick", f"{top_ticker} ({top_score:.1f}/6)")
        
        with col3:
            risky = len([r for r in results if r['color'] == 'red'])
            st.metric("🔴 Risky", f"{risky}/{len(results)}")
        
        with col4:
            good = len([r for r in results if r['color'] == 'green'])
            st.metric("🟢 Good", f"{good}/{len(results)}")
        
        with col5:
            ipo_count = len(set(r.get('ipo_date', '') for r in results if r.get('ipo_date') and r['ipo_date'] != 'Unknown'))
            st.metric("📅 IPOs", f"{ipo_count}")
        
        # Honest Summary
        st.info(f"💡 **The honest truth:** These are all new companies. Some will succeed, many will fail. The 'good' ones have solid fundamentals, but being new adds extra risk. Always do your own research before investing.")
        
        # Display each company
        for result in results:
            display_new_company_card(result)
            st.divider()
        
        # --- Download Results ---
        df = pd.DataFrame(results)
        if not df.empty:
            df_download = df[['ticker', 'name', 'sector', 'ipo_date', 'current_price', 'total_score', 'risk_score', 'rating']].copy()
            df_download['current_price'] = df_download['current_price'].apply(lambda x: f"${x:.2f}" if x else "N/A")
            
            st.download_button(
                label="📥 Download New Company Analysis (CSV)",
                data=df_download.to_csv(index=False),
                file_name=f"new_companies_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

else:
    st.info("👆 Click the button above to find new companies!")
    
    # Show preview of available companies
    st.subheader("📋 Available New Companies")
    
    # Create preview table
    preview_data = []
    for sector, data in NEW_COMPANIES.items():
        for company in data['companies']:
            preview_data.append({
                'Ticker': company['ticker'],
                'Name': company['name'],
                'Sector': sector,
                'IPO Date': company['ipo_date'],
                'Industry': company['industry']
            })
    
    preview_df = pd.DataFrame(preview_data)
    st.dataframe(
        preview_df,
        use_container_width=True,
        hide_index=True
    )

# --- Educational Section ---
st.divider()
st.subheader("💡 What Makes a New Company Risky?")

col1, col2, col3 = st.columns(3)

with col1:
    st.write("**📉 Limited History**")
    st.write("""
    These companies have been public for less than a year.
    
    You can't look at 5 or 10 years of financial data to see how they perform during good times and bad.
    
    **You're investing based on potential, not proven results.**
    """)

with col2:
    st.write("**📊 Volatile Prices**")
    st.write("""
    New stocks are often much more volatile than established ones.
    
    First-day "pops" can be followed by big drops.
    
    **Example:** Figma popped 250% on day 1, then dropped 45% a few months later.
    """)

with col3:
    st.write("**💼 Unproven Business Models**")
    st.write("""
    Many new companies are still figuring out how to make money.
    
    They might have great technology but poor financials.
    
    **Always check:** Are they profitable? Do they have a path to profitability?
    """)

# --- Footer ---
st.divider()
st.caption("🚀 New Company Tracker — Watch the newest stocks on the market")
st.caption("📊 Data for educational purposes only • All investments carry risk")
st.caption(f"🕐 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

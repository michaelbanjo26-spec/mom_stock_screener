import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# ==========================================
# STOCK DATA FOR EACH INDUSTRY
# ==========================================

INDUSTRIES = {
    "💻 Technology": ["AAPL", "MSFT", "NVDA", "GOOGL", "META", "ADBE", "CRM", "ORCL", "IBM", "CSCO"],
    "🏦 Banking": ["JPM", "BAC", "WFC", "C", "GS", "MS", "USB", "PNC", "TFC", "SCHW"],
    "🛒 Retail": ["WMT", "AMZN", "COST", "TGT", "HD", "LOW", "TJX", "ROST", "DG", "DLTR"],
    "💊 Healthcare": ["JNJ", "PFE", "MRK", "ABBV", "UNH", "CVS", "CI", "HUM", "ELV", "ANTM"],
    "🍔 Consumer Goods": ["PG", "KO", "PEP", "MCD", "SBUX", "NKE", "DIS", "MMM", "CL", "KMB"],
    "🔌 Energy": ["XOM", "CVX", "COP", "SLB", "EOG", "PXD", "OXY", "KMI", "MPC", "PSX"],
    "🏗️ Industrials": ["GE", "CAT", "BA", "LMT", "RTX", "HON", "UNP", "UPS", "FDX", "DE"],
    "📞 Telecom": ["VZ", "T", "TMUS", "CHTR", "CMCSA", "DISH", "ATNI", "LUMN", "USM", "IHS"],
    "🧪 Biotech": ["AMGN", "GILD", "BIIB", "REGN", "VRTX", "MRNA", "IONS", "ALNY", "NBIX", "EXEL"],
    "🏠 Real Estate": ["AMT", "PLD", "EQIX", "PSA", "VICI", "WELL", "SPG", "O", "DLR", "AVB"],
}

# ==========================================
# NEWS FUNCTION
# ==========================================

def get_stock_news(ticker, limit=5):
    """Get recent news for a stock from Yahoo Finance"""
    try:
        stock = yf.Ticker(ticker)
        news = stock.news
        
        if not news:
            return []
        
        # Format news articles
        articles = []
        for item in news[:limit]:
            # Extract title and link
            title = item.get('title', 'No title')
            link = item.get('link', '#')
            
            # Get publisher and time
            publisher = item.get('publisher', 'Unknown source')
            
            # Get content snippet (if available)
            content = item.get('content', '')
            snippet = content[:200] + '...' if content else ''
            
            # Determine sentiment (basic keyword analysis)
            positive_words = ['surge', 'beat', 'up', 'gain', 'record', 'strong', 'positive', 'growth', 'profit', 'success']
            negative_words = ['drop', 'fall', 'down', 'loss', 'cut', 'negative', 'weak', 'decline', 'risk', 'concern']
            
            title_lower = title.lower()
            sentiment = 'neutral'
            
            pos_count = sum(1 for word in positive_words if word in title_lower)
            neg_count = sum(1 for word in negative_words if word in title_lower)
            
            if pos_count > neg_count:
                sentiment = 'positive'
            elif neg_count > pos_count:
                sentiment = 'negative'
            
            articles.append({
                'title': title,
                'link': link,
                'publisher': publisher,
                'snippet': snippet,
                'sentiment': sentiment
            })
        
        return articles
    
    except Exception as e:
        return []

# ==========================================
# ANALYSIS FUNCTION
# ==========================================

def analyze_stock(ticker):
    """Analyze a stock and return all metrics + score"""
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
    dividend_yield = info.get('dividendYield', 0)
    name = info.get('longName', ticker)
    
    # --- Calculate Scores ---
    graham_score = 0
    fisher_score = 0
    
    # Graham: P/E (under 15 is good)
    if pe and pe < 15:
        graham_score += 1
        pe_status = "✅ Low P/E"
    elif pe and pe < 25:
        pe_status = "⚖️ Moderate P/E"
    elif pe:
        pe_status = "⚠️ High P/E"
    else:
        pe_status = "❌ No P/E data"
    
    # Graham: Debt/Equity (under 0.5 is good)
    if debt_to_equity and debt_to_equity < 0.5:
        graham_score += 1
        debt_status = "✅ Low debt"
    elif debt_to_equity and debt_to_equity < 1.0:
        debt_status = "⚖️ Moderate debt"
    elif debt_to_equity:
        debt_status = "⚠️ High debt"
    else:
        debt_status = "❌ No debt data"
    
    # Graham: Earnings Growth (positive is good)
    if earnings_growth and earnings_growth > 0:
        graham_score += 1
        earnings_status = "✅ Earnings growing"
    elif earnings_growth:
        earnings_status = "⚠️ Earnings shrinking"
    else:
        earnings_status = "❌ No earnings data"
    
    # Fisher: ROE (over 15% is good)
    if roe and roe > 0.15:
        fisher_score += 1
        roe_status = "✅ Strong ROE"
    elif roe and roe > 0.05:
        roe_status = "⚖️ Average ROE"
    elif roe:
        roe_status = "⚠️ Weak ROE"
    else:
        roe_status = "❌ No ROE data"
    
    # Fisher: Revenue Growth (over 10% is good)
    if revenue_growth and revenue_growth > 0.10:
        fisher_score += 1
        revenue_status = "✅ Strong revenue growth"
    elif revenue_growth and revenue_growth > 0:
        revenue_status = "⚖️ Moderate revenue growth"
    elif revenue_growth:
        revenue_status = "⚠️ Revenue shrinking"
    else:
        revenue_status = "❌ No revenue data"
    
    # Fisher: Profit Margin (over 15% is good)
    if profit_margin and profit_margin > 0.15:
        fisher_score += 1
        margin_status = "✅ Strong profit margin"
    elif profit_margin and profit_margin > 0.05:
        margin_status = "⚖️ Average profit margin"
    elif profit_margin:
        margin_status = "⚠️ Weak profit margin"
    else:
        margin_status = "❌ No margin data"
    
    # Total Score (0-6)
    total_score = graham_score + fisher_score
    
    # Determine rating
    if total_score >= 5:
        rating = "🌟 EXCELLENT — Buy it!"
        color = "green"
        mom_advice = "This is a wonderful company! Great finances, growing profits, and you probably know their products. Safe choice for long-term investing!"
    elif total_score >= 4:
        rating = "👍 GOOD — Solid choice"
        color = "green"
        mom_advice = "Good company with strong fundamentals. Might be a little expensive, but quality is there. Keep an eye on it!"
    elif total_score >= 3:
        rating = "🤔 OK — Some risks"
        color = "orange"
        mom_advice = "Mixed signals here. Some things look good, others need improvement. Maybe wait for better news or a lower price."
    elif total_score >= 2:
        rating = "⚠️ RISKY — Be careful"
        color = "orange"
        mom_advice = "This one has some red flags. High debt or weak profits. Only invest if you really understand the business and can handle risk."
    else:
        rating = "❌ POOR — Skip it"
        color = "red"
        mom_advice = "Too many warning signs. Avoid this one — there are better options out there for your hard-earned money."
    
    return {
        'ticker': ticker,
        'name': name,
        'sector': sector,
        'market_cap': market_cap,
        'graham_score': graham_score,
        'fisher_score': fisher_score,
        'total_score': total_score,
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
        'dividend_yield': dividend_yield,
    }

# ==========================================
# DISPLAY NEWS FUNCTION
# ==========================================

def display_news(ticker):
    """Display news for a stock with sentiment indicators"""
    articles = get_stock_news(ticker)
    
    if not articles:
        st.info("📭 No recent news found for this stock")
        return
    
    # Count positive/negative
    pos_count = sum(1 for a in articles if a['sentiment'] == 'positive')
    neg_count = sum(1 for a in articles if a['sentiment'] == 'negative')
    
    # Show sentiment summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Articles", len(articles))
    with col2:
        st.metric("📈 Positive", pos_count, delta=None, delta_color="normal")
    with col3:
        st.metric("📉 Negative", neg_count, delta=None, delta_color="inverse")
    
    # Show articles
    for i, article in enumerate(articles):
        # Color based on sentiment
        if article['sentiment'] == 'positive':
            st.success(f"**📈 {article['title']}**")
        elif article['sentiment'] == 'negative':
            st.error(f"**📉 {article['title']}**")
        else:
            st.info(f"**📰 {article['title']}**")
        
        st.write(f"*{article['publisher']}*")
        if article['snippet']:
            st.write(article['snippet'])
        
        # Link to full article
        if article['link'] and article['link'] != '#':
            st.markdown(f"[Read full article →]({article['link']})")
        
        st.divider()

# ==========================================
# DISPLAY STOCK CARD FUNCTION
# ==========================================

def display_stock_card(row, show_news=True):
    """Display a single stock card with optional news"""
    # Color the card based on rating
    if row['color'] == 'green':
        st.success(f"### {row['rating']}")
    elif row['color'] == 'orange':
        st.warning(f"### {row['rating']}")
    else:
        st.error(f"### {row['rating']}")
    
    # Main info
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.write(f"**{row['ticker']}** — {row['name']}")
        st.write(f"*{row['sector']}*")
        
        # Mom advice
        st.info(f"💡 **Mom says:** {row['mom_advice']}")
    
    with col2:
        st.write(f"📊 Score: **{row['total_score']}/6**")
        st.write(f"🛡️ Safety: {row['graham_score']}/3")
        st.write(f"⭐ Quality: {row['fisher_score']}/3")
    
    with col3:
        if row['dividend_yield'] and row['dividend_yield'] > 0:
            st.write(f"💰 Div: {row['dividend_yield']*100:.2f}%")
        else:
            st.write("💰 No dividend")
        if row['market_cap']:
            st.write(f"🏢 Cap: ${row['market_cap']/1e9:.1f}B")
    
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
    
    # News section
    if show_news:
        with st.expander("📰 Latest News & Articles"):
            display_news(row['ticker'])

# ==========================================
# STREAMLIT UI
# ==========================================

st.set_page_config(page_title="Mom's Stock Picker", page_icon="📊", layout="wide")

# --- Header ---
st.title("📊 Mom's Stock Picker")
st.markdown("*Find safe, quality stocks in industries you know!*")
st.markdown("---")

# --- Sidebar ---
with st.sidebar:
    st.header("🎯 About This Tool")
    st.write("""
    **60% Graham** — Safety first! Low debt, fair price
    
    **30% Fisher** — Quality matters! Strong profits, growth
    
    **10% Lynch** — Keep it simple! Buy what you know
    """)
    
    st.divider()
    
    st.header("📰 News Sentiment")
    st.write("""
    📈 **Green** = Positive news
    📉 **Red** = Negative news
    📰 **Blue** = Neutral news
    """)

# --- Industry Selection ---
selected_industry = st.selectbox(
    "🏭 Pick an industry:",
    list(INDUSTRIES.keys())
)

# Get stocks for selected industry
stocks = INDUSTRIES[selected_industry]

st.write(f"**Top {len(stocks)} stocks in {selected_industry}**")

# --- Analyze All Stocks in Industry ---
col1, col2 = st.columns([3, 1])
with col1:
    analyze_btn = st.button(f"🔍 Analyze {selected_industry} Stocks", use_container_width=True)
with col2:
    show_news_toggle = st.checkbox("Show News", value=True)

if analyze_btn:
    with st.spinner("Fetching data... this takes about 10-15 seconds..."):
        results = []
        
        # Progress bar
        progress_bar = st.progress(0)
        for i, ticker in enumerate(stocks):
            result = analyze_stock(ticker)
            results.append(result)
            progress_bar.progress((i + 1) / len(stocks))
        
        # Convert to DataFrame
        df = pd.DataFrame(results)
        
        # Sort by score (highest first)
        df = df.sort_values('total_score', ascending=False)
        
        # --- Display Results ---
        st.success("✅ Analysis complete!")
        
        # Show top picks
        st.subheader(f"🏆 Top Picks in {selected_industry}")
        
        # Display each stock as a card
        for _, row in df.iterrows():
            display_stock_card(row, show_news_toggle)
            st.divider()
        
        # --- Summary Stats ---
        st.subheader("📊 Industry Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            avg_score = df['total_score'].mean()
            st.metric("Average Score", f"{avg_score:.1f}/6")
        with col2:
            top_ticker = df.iloc[0]['ticker']
            top_score = df.iloc[0]['total_score']
            st.metric("Top Pick", f"{top_ticker} ({top_score}/6)")
        with col3:
            good_stocks = len(df[df['total_score'] >= 4])
            st.metric("Good Stocks", f"{good_stocks}/{len(df)}")
        with col4:
            # Best mom advice
            best_row = df.iloc[0]
            st.metric("Best Advice", f"⭐ {best_row['rating'][:10]}...")
        
        # --- Download Results ---
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Results (CSV)",
            data=csv,
            file_name=f"{selected_industry}_analysis.csv",
            mime="text/csv"
        )

else:
    st.info("👆 Click the button above to analyze all stocks in this industry!")

# --- Individual Stock Lookup ---
st.divider()
st.subheader("🔍 Or search a specific stock")

col1, col2 = st.columns([3, 1])
with col1:
    ticker_input = st.text_input("Enter any ticker:", value="AAPL").upper()
with col2:
    show_news_single = st.checkbox("Show News for this stock", value=True)

if st.button("Analyze This Stock"):
    with st.spinner(f"Analyzing {ticker_input}..."):
        result = analyze_stock(ticker_input)
        
        # Display result as a card
        display_stock_card(pd.Series(result), show_news_single)

# --- Footer ---
st.divider()
st.caption("💡 Based on 60% Graham (safety), 30% Fisher (quality), 10% Lynch (simplicity)")
st.caption("📰 News powered by Yahoo Finance • For educational purposes only")

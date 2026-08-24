import streamlit as st
import pandas as pd
from datetime import datetime

# ==========================================
# GLOBAL BOND DATA BY COUNTRY
# ==========================================

GLOBAL_BONDS = {
    "🇺🇸 United States": {
        "currency": "USD",
        "risk": "🟢 Very Low",
        "bonds": [
            {"name": "3-Month T-Bill", "yield": 5.25, "maturity": "0.25 years", "rating": "AAA"},
            {"name": "2-Year Treasury", "yield": 4.85, "maturity": "2 years", "rating": "AAA"},
            {"name": "5-Year Treasury", "yield": 4.50, "maturity": "5 years", "rating": "AAA"},
            {"name": "10-Year Treasury", "yield": 4.25, "maturity": "10 years", "rating": "AAA"},
            {"name": "30-Year Treasury", "yield": 4.40, "maturity": "30 years", "rating": "AAA"},
            {"name": "Apple 4.65% 2046", "yield": 4.80, "maturity": "22 years", "rating": "AA+"},
            {"name": "Microsoft 3.45% 2050", "yield": 4.60, "maturity": "26 years", "rating": "AAA"},
            {"name": "JPMorgan 4.95% 2035", "yield": 5.10, "maturity": "11 years", "rating": "A"},
            {"name": "Walmart 3.70% 2045", "yield": 4.75, "maturity": "21 years", "rating": "AA"},
            {"name": "Tesla 5.30% 2045", "yield": 6.80, "maturity": "21 years", "rating": "BB"},
            {"name": "Ford 6.10% 2040", "yield": 7.20, "maturity": "16 years", "rating": "BB-"},
            {"name": "Macy's 6.75% 2043", "yield": 8.10, "maturity": "19 years", "rating": "B"},
        ]
    },
    "🇬🇧 United Kingdom": {
        "currency": "GBP",
        "risk": "🟢 Low",
        "bonds": [
            {"name": "UK 2-Year Gilt", "yield": 4.75, "maturity": "2 years", "rating": "AA"},
            {"name": "UK 5-Year Gilt", "yield": 4.40, "maturity": "5 years", "rating": "AA"},
            {"name": "UK 10-Year Gilt", "yield": 4.20, "maturity": "10 years", "rating": "AA"},
            {"name": "UK 30-Year Gilt", "yield": 4.50, "maturity": "30 years", "rating": "AA"},
            {"name": "Shell 4.50% 2045", "yield": 5.20, "maturity": "21 years", "rating": "AA-"},
            {"name": "HSBC 5.00% 2040", "yield": 5.80, "maturity": "16 years", "rating": "A"},
            {"name": "BP 4.75% 2048", "yield": 5.40, "maturity": "24 years", "rating": "A"},
            {"name": "Vodafone 5.20% 2048", "yield": 6.20, "maturity": "24 years", "rating": "BB"},
            {"name": "Barclays 6.00% 2045", "yield": 7.00, "maturity": "21 years", "rating": "BB+"},
            {"name": "Tesco 5.50% 2043", "yield": 6.50, "maturity": "19 years", "rating": "BBB"},
        ]
    },
    "🇩🇪 Germany": {
        "currency": "EUR",
        "risk": "🟢 Very Low",
        "bonds": [
            {"name": "German 2-Year Bund", "yield": 3.20, "maturity": "2 years", "rating": "AAA"},
            {"name": "German 5-Year Bund", "yield": 2.90, "maturity": "5 years", "rating": "AAA"},
            {"name": "German 10-Year Bund", "yield": 2.60, "maturity": "10 years", "rating": "AAA"},
            {"name": "German 30-Year Bund", "yield": 2.80, "maturity": "30 years", "rating": "AAA"},
            {"name": "Siemens 3.50% 2045", "yield": 4.00, "maturity": "21 years", "rating": "AA"},
            {"name": "BMW 3.80% 2040", "yield": 4.20, "maturity": "16 years", "rating": "AA-"},
            {"name": "Volkswagen 4.50% 2048", "yield": 5.00, "maturity": "24 years", "rating": "A"},
            {"name": "Deutsche Bank 5.50% 2045", "yield": 6.50, "maturity": "21 years", "rating": "BBB+"},
        ]
    },
    "🇫🇷 France": {
        "currency": "EUR",
        "risk": "🟢 Low",
        "bonds": [
            {"name": "French 2-Year OAT", "yield": 3.30, "maturity": "2 years", "rating": "AA"},
            {"name": "French 5-Year OAT", "yield": 3.00, "maturity": "5 years", "rating": "AA"},
            {"name": "French 10-Year OAT", "yield": 2.80, "maturity": "10 years", "rating": "AA"},
            {"name": "French 30-Year OAT", "yield": 3.10, "maturity": "30 years", "rating": "AA"},
            {"name": "TotalEnergies 3.80% 2045", "yield": 4.30, "maturity": "21 years", "rating": "AA-"},
            {"name": "LVMH 3.50% 2050", "yield": 4.00, "maturity": "26 years", "rating": "A+"},
            {"name": "BNP Paribas 4.50% 2048", "yield": 5.20, "maturity": "24 years", "rating": "A"},
            {"name": "Airbus 4.20% 2045", "yield": 4.80, "maturity": "21 years", "rating": "A"},
        ]
    },
    "🇯🇵 Japan": {
        "currency": "JPY",
        "risk": "🟢 Low",
        "bonds": [
            {"name": "Japan 2-Year JGB", "yield": 0.10, "maturity": "2 years", "rating": "A+"},
            {"name": "Japan 5-Year JGB", "yield": 0.20, "maturity": "5 years", "rating": "A+"},
            {"name": "Japan 10-Year JGB", "yield": 0.40, "maturity": "10 years", "rating": "A+"},
            {"name": "Japan 30-Year JGB", "yield": 1.00, "maturity": "30 years", "rating": "A+"},
            {"name": "Toyota 2.50% 2045", "yield": 3.50, "maturity": "21 years", "rating": "AA"},
            {"name": "Sony 3.00% 2040", "yield": 4.00, "maturity": "16 years", "rating": "A"},
            {"name": "Mitsubishi 3.20% 2048", "yield": 4.20, "maturity": "24 years", "rating": "A"},
            {"name": "SoftBank 4.50% 2045", "yield": 6.00, "maturity": "21 years", "rating": "BBB"},
            {"name": "Nissan 4.80% 2045", "yield": 6.40, "maturity": "21 years", "rating": "BB-"},
        ]
    },
    "🇨🇳 China": {
        "currency": "CNY",
        "risk": "🟡 Moderate",
        "bonds": [
            {"name": "China 2-Year Gov't", "yield": 2.50, "maturity": "2 years", "rating": "A+"},
            {"name": "China 5-Year Gov't", "yield": 2.80, "maturity": "5 years", "rating": "A+"},
            {"name": "China 10-Year Gov't", "yield": 3.00, "maturity": "10 years", "rating": "A+"},
            {"name": "China 30-Year Gov't", "yield": 3.30, "maturity": "30 years", "rating": "A+"},
            {"name": "Alibaba 3.50% 2045", "yield": 5.00, "maturity": "21 years", "rating": "A"},
            {"name": "Tencent 3.80% 2048", "yield": 5.20, "maturity": "24 years", "rating": "A"},
            {"name": "China Mobile 4.00% 2040", "yield": 5.50, "maturity": "16 years", "rating": "A+"},
            {"name": "Baidu 4.50% 2045", "yield": 6.00, "maturity": "21 years", "rating": "BBB+"},
            {"name": "Evergrande 8.00% 2043", "yield": 12.00, "maturity": "19 years", "rating": "CCC"},
        ]
    },
    "🇮🇳 India": {
        "currency": "INR",
        "risk": "🟠 Moderate-High",
        "bonds": [
            {"name": "India 2-Year Gov't", "yield": 7.50, "maturity": "2 years", "rating": "BBB-"},
            {"name": "India 5-Year Gov't", "yield": 7.80, "maturity": "5 years", "rating": "BBB-"},
            {"name": "India 10-Year Gov't", "yield": 7.20, "maturity": "10 years", "rating": "BBB-"},
            {"name": "India 30-Year Gov't", "yield": 7.50, "maturity": "30 years", "rating": "BBB-"},
            {"name": "Reliance 4.50% 2045", "yield": 8.00, "maturity": "21 years", "rating": "BBB"},
            {"name": "ICICI Bank 5.00% 2040", "yield": 8.50, "maturity": "16 years", "rating": "BBB"},
            {"name": "HDFC 4.80% 2048", "yield": 8.20, "maturity": "24 years", "rating": "BBB+"},
            {"name": "Tata Motors 5.50% 2045", "yield": 9.00, "maturity": "21 years", "rating": "BB+"},
            {"name": "Vedanta 6.00% 2043", "yield": 11.00, "maturity": "19 years", "rating": "BB"},
        ]
    },
    "🇧🇷 Brazil": {
        "currency": "BRL",
        "risk": "🔴 High",
        "bonds": [
            {"name": "Brazil 2-Year Gov't", "yield": 11.50, "maturity": "2 years", "rating": "BB-"},
            {"name": "Brazil 5-Year Gov't", "yield": 11.80, "maturity": "5 years", "rating": "BB-"},
            {"name": "Brazil 10-Year Gov't", "yield": 11.20, "maturity": "10 years", "rating": "BB-"},
            {"name": "Brazil 30-Year Gov't", "yield": 11.50, "maturity": "30 years", "rating": "BB-"},
            {"name": "Petrobras 5.50% 2045", "yield": 12.00, "maturity": "21 years", "rating": "BB"},
            {"name": "Vale 4.80% 2040", "yield": 10.50, "maturity": "16 years", "rating": "BB+"},
            {"name": "Ambev 4.50% 2048", "yield": 10.00, "maturity": "24 years", "rating": "BB"},
            {"name": "Itau 5.00% 2045", "yield": 11.50, "maturity": "21 years", "rating": "BB"},
            {"name": "Embraer 6.00% 2043", "yield": 13.00, "maturity": "19 years", "rating": "B+"},
        ]
    },
    "🇿🇦 South Africa": {
        "currency": "ZAR",
        "risk": "🔴 High",
        "bonds": [
            {"name": "SA 2-Year Gov't", "yield": 10.50, "maturity": "2 years", "rating": "BB"},
            {"name": "SA 5-Year Gov't", "yield": 10.80, "maturity": "5 years", "rating": "BB"},
            {"name": "SA 10-Year Gov't", "yield": 10.20, "maturity": "10 years", "rating": "BB"},
            {"name": "SA 30-Year Gov't", "yield": 10.50, "maturity": "30 years", "rating": "BB"},
            {"name": "MTN 5.00% 2045", "yield": 11.50, "maturity": "21 years", "rating": "BB"},
            {"name": "Sasol 4.80% 2040", "yield": 10.50, "maturity": "16 years", "rating": "BB-"},
            {"name": "Standard Bank 5.50% 2048", "yield": 11.00, "maturity": "24 years", "rating": "BB"},
            {"name": "Eskom 6.00% 2045", "yield": 13.00, "maturity": "21 years", "rating": "B"},
        ]
    }
}

# ==========================================
# BOND ANALYSIS FUNCTION
# ==========================================

def analyze_bond(bond, country, currency, risk_level):
    """Analyze a single bond"""
    
    yield_rate = bond['yield']
    rating = bond['rating']
    maturity = bond['maturity']
    
    # Determine yield category
    if yield_rate < 3.0:
        yield_category = "🟢 Normal (0-3%)"
        yield_score = 3
    elif yield_rate < 5.0:
        yield_category = "🟡 Medium (3-5%)"
        yield_score = 2
    elif yield_rate < 8.0:
        yield_category = "🟠 High (5-8%)"
        yield_score = 1
    else:
        yield_category = "🔴 Very High (8%+)"
        yield_score = 0
    
    # Credit risk assessment
    if rating in ['AAA', 'AA+', 'AA']:
        credit_risk = "🟢 Very Low"
        credit_score = 3
    elif rating in ['AA-', 'A+', 'A']:
        credit_risk = "🟢 Low"
        credit_score = 2
    elif rating in ['A-', 'BBB+', 'BBB']:
        credit_risk = "🟡 Moderate"
        credit_score = 1
    elif rating in ['BBB-', 'BB+', 'BB']:
        credit_risk = "🟠 Some Risk"
        credit_score = 0
    elif rating in ['BB-', 'B+', 'B']:
        credit_risk = "🔴 High Risk"
        credit_score = -1
    else:
        credit_risk = "🔴 Very High Risk"
        credit_score = -2
    
    # Combined score
    total_score = yield_score + credit_score
    
    # Determine overall rating
    if total_score >= 5:
        stars = "⭐⭐⭐⭐⭐"
        recommendation = "🌟 EXCELLENT — Great yield, low risk!"
        color = "green"
        mom_advice = "This bond offers excellent value! High yield with manageable risk. A great addition to any portfolio."
    elif total_score >= 4:
        stars = "⭐⭐⭐⭐"
        recommendation = "👍 GOOD — Solid choice"
        color = "green"
        mom_advice = "Good balance of yield and risk. This bond is worth considering for steady income."
    elif total_score >= 3:
        stars = "⭐⭐⭐"
        recommendation = "🤔 FAIR — Decent option"
        color = "orange"
        mom_advice = "This bond has some trade-offs. The yield is decent but there are better options available."
    elif total_score >= 2:
        stars = "⭐⭐"
        recommendation = "⚠️ RISKY — Be careful"
        color = "orange"
        mom_advice = "Higher yield comes with higher risk. Only consider if you understand the risks involved."
    else:
        stars = "⭐"
        recommendation = "❌ POOR — Skip it"
        color = "red"
        mom_advice = "Too much risk for the yield. There are much better options elsewhere."
    
    return {
        'country': country,
        'currency': currency,
        'risk_level': risk_level,
        'name': bond['name'],
        'yield': yield_rate,
        'yield_category': yield_category,
        'maturity': maturity,
        'rating': rating,
        'credit_risk': credit_risk,
        'stars': stars,
        'recommendation': recommendation,
        'color': color,
        'mom_advice': mom_advice,
        'total_score': total_score,
        'credit_score': credit_score,
        'yield_score': yield_score
    }

# ==========================================
# DISPLAY FUNCTIONS
# ==========================================

def display_bond_card(analysis):
    """Display a bond as a simple card"""
    
    # Color the card based on rating
    if analysis['color'] == 'green':
        st.success(f"### {analysis['stars']} {analysis['recommendation']}")
    elif analysis['color'] == 'orange':
        st.warning(f"### {analysis['stars']} {analysis['recommendation']}")
    else:
        st.error(f"### {analysis['stars']} {analysis['recommendation']}")
    
    col1, col2, col3, col4 = st.columns([2, 1.5, 1.5, 1])
    
    with col1:
        st.write(f"**{analysis['name']}**")
        st.write(f"🌍 {analysis['country']} • {analysis['currency']}")
        st.write(f"*Rating: {analysis['rating']}*")
    
    with col2:
        st.metric("📊 Yield", f"{analysis['yield']:.2f}%")
        st.caption(analysis['yield_category'])
    
    with col3:
        st.metric("⏰ Maturity", analysis['maturity'])
        st.caption(analysis['credit_risk'])
    
    with col4:
        st.metric("📈 Score", f"{analysis['total_score']}/6")
        st.caption(f"Yield: {analysis['yield_score']}/3 • Credit: {analysis['credit_score']}/3")
    
    st.info(f"💡 **Mom says:** {analysis['mom_advice']}")

# ==========================================
# STREAMLIT UI
# ==========================================

st.set_page_config(page_title="Global Bond Tracker", page_icon="🌍", layout="wide")

# --- Header ---
st.title("🌍 Global Bond Tracker")
st.markdown("*Find the best bond yields around the world — sorted by yield, risk, and country!*")
st.markdown("---")

# --- Sidebar ---
with st.sidebar:
    st.header("🎯 How It Works")
    st.write("""
    1. **Pick a country** or view all countries
    2. **Filter by yield** — Normal, Medium, High, Very High
    3. **Check credit risk** — From safe to risky
    4. **Find the best deals** — Compare across countries
    """)
    
    st.divider()
    
    st.header("📊 Yield Categories")
    st.write("""
    - 🟢 **Normal (0-3%)** — Very safe, low return
    - 🟡 **Medium (3-5%)** — Good balance
    - 🟠 **High (5-8%)** — More risk, more reward
    - 🔴 **Very High (8%+)** — High risk, high reward
    """)
    
    st.divider()
    
    st.header("📖 Bond Terms")
    with st.expander("📘 Yield"):
        st.write("The annual interest you earn. Higher yield = more income, but often more risk.")
    with st.expander("📘 Credit Rating"):
        st.write("AAA = safest. D = risky. Like a credit score for companies and countries.")
    with st.expander("📘 Maturity"):
        st.write("When you get your money back. Longer = more risk, but often higher yield.")
    with st.expander("📘 Currency Risk"):
        st.write("If you buy bonds in another currency, exchange rates can affect your returns.")

# --- Main Content ---

# Filters
st.subheader("🔍 Filter Bonds")

col1, col2, col3, col4 = st.columns(4)

with col1:
    selected_country = st.selectbox(
        "🌍 Country",
        ["All Countries"] + list(GLOBAL_BONDS.keys())
    )

with col2:
    yield_filters = st.multiselect(
        "📊 Yield Range",
        ["🟢 Normal (0-3%)", "🟡 Medium (3-5%)", "🟠 High (5-8%)", "🔴 Very High (8%+)"],
        default=["🟢 Normal (0-3%)", "🟡 Medium (3-5%)", "🟠 High (5-8%)", "🔴 Very High (8%+)"]
    )

with col3:
    min_yield = st.slider("Minimum Yield (%)", 0.0, 15.0, 0.0, step=0.5)

with col4:
    sort_by = st.selectbox(
        "Sort by",
        ["Yield (High to Low)", "Yield (Low to High)", "Country", "Maturity", "Rating"]
    )

# --- Analyze Bonds ---
if st.button("🔍 Find Bonds", use_container_width=True):
    
    # Collect all bonds
    all_bonds = []
    
    for country, data in GLOBAL_BONDS.items():
        # Skip if country filter is active
        if selected_country != "All Countries" and selected_country != country:
            continue
        
        for bond in data['bonds']:
            analysis = analyze_bond(
                bond, 
                country, 
                data['currency'], 
                data['risk']
            )
            
            # Apply yield filter
            if analysis['yield_category'] not in yield_filters:
                continue
            
            # Apply min yield filter
            if analysis['yield'] < min_yield:
                continue
            
            all_bonds.append(analysis)
    
    # Sort
    if sort_by == "Yield (High to Low)":
        all_bonds = sorted(all_bonds, key=lambda x: x['yield'], reverse=True)
    elif sort_by == "Yield (Low to High)":
        all_bonds = sorted(all_bonds, key=lambda x: x['yield'])
    elif sort_by == "Country":
        all_bonds = sorted(all_bonds, key=lambda x: x['country'])
    elif sort_by == "Maturity":
        all_bonds = sorted(all_bonds, key=lambda x: float(x['maturity'].split()[0]) if 'years' in x['maturity'] else 0)
    elif sort_by == "Rating":
        rating_order = {'AAA': 1, 'AA+': 2, 'AA': 3, 'AA-': 4, 'A+': 5, 'A': 6, 'A-': 7, 
                       'BBB+': 8, 'BBB': 9, 'BBB-': 10, 'BB+': 11, 'BB': 12, 'BB-': 13,
                       'B+': 14, 'B': 15, 'B-': 16, 'CCC': 17}
        all_bonds = sorted(all_bonds, key=lambda x: rating_order.get(x['rating'], 99))
    
    # --- Display Results ---
    st.divider()
    st.subheader(f"📋 Found {len(all_bonds)} Bonds")
    
    if not all_bonds:
        st.warning("No bonds match your filters. Try adjusting them.")
    else:
        # Summary stats
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            avg_yield = sum(b['yield'] for b in all_bonds) / len(all_bonds)
            st.metric("Average Yield", f"{avg_yield:.2f}%")
        
        with col2:
            max_yield = max(b['yield'] for b in all_bonds)
            st.metric("Highest Yield", f"{max_yield:.2f}%")
        
        with col3:
            min_yield_display = min(b['yield'] for b in all_bonds)
            st.metric("Lowest Yield", f"{min_yield_display:.2f}%")
        
        with col4:
            good_bonds = len([b for b in all_bonds if b['total_score'] >= 4])
            st.metric("Good Bonds", f"{good_bonds}/{len(all_bonds)}")
        
        with col5:
            countries_represented = len(set(b['country'] for b in all_bonds))
            st.metric("Countries", countries_represented)
        
        # Display each bond
        for bond in all_bonds:
            display_bond_card(bond)
            st.divider()
        
        # --- Download Results ---
        df = pd.DataFrame(all_bonds)
        df_download = df[['country', 'currency', 'name', 'yield', 'rating', 'maturity', 'credit_risk', 'recommendation']].copy()
        df_download['yield'] = df_download['yield'].apply(lambda x: f"{x:.2f}%")
        
        st.download_button(
            label="📥 Download Bond Analysis (CSV)",
            data=df_download.to_csv(index=False),
            file_name=f"global_bonds_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

else:
    st.info("👆 Click 'Find Bonds' to see all bonds matching your criteria!")

# --- Country Comparison Table ---
st.divider()
st.subheader("📊 Country Yield Comparison")

# Show average yield by country
country_yields = {}
for country, data in GLOBAL_BONDS.items():
    yields = [b['yield'] for b in data['bonds']]
    country_yields[country] = {
        'avg': sum(yields) / len(yields),
        'max': max(yields),
        'min': min(yields),
        'count': len(yields),
        'risk': data['risk']
    }

# Create comparison dataframe
comparison_data = []
for country, data in country_yields.items():
    comparison_data.append({
        'Country': country,
        'Risk': data['risk'],
        'Average Yield': data['avg'],
        'Max Yield': data['max'],
        'Min Yield': data['min'],
        'Bonds Available': data['count']
    })

comparison_df = pd.DataFrame(comparison_data).sort_values('Average Yield', ascending=False)

st.dataframe(
    comparison_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Country": "🌍 Country",
        "Risk": "🛡️ Risk Level",
        "Average Yield": st.column_config.NumberColumn("📊 Avg Yield", format="%.2f%%"),
        "Max Yield": st.column_config.NumberColumn("📈 Max Yield", format="%.2f%%"),
        "Min Yield": st.column_config.NumberColumn("📉 Min Yield", format="%.2f%%"),
        "Bonds Available": "📋 Bonds"
    }
)

# --- Yield Distribution (Text-based) ---
st.divider()
st.subheader("📈 Yield Distribution by Country")

# Create a simple bar chart using Streamlit's native bar chart
chart_data = pd.DataFrame([
    {
        'Country': country,
        'Average Yield': data['avg']
    }
    for country, data in country_yields.items()
]).set_index('Country')

st.bar_chart(chart_data, height=400)

# --- Educational Section ---
st.divider()
st.subheader("💡 Understanding Global Bonds")

col1, col2, col3 = st.columns(3)

with col1:
    st.write("**🏠 Safe Countries (AAA/AA)**")
    st.write("""
    - 🇺🇸 US Treasuries (4-5%)
    - 🇩🇪 German Bunds (2-3%)
    - 🇯🇵 Japanese JGBs (0-1%)
    - 🇬🇧 UK Gilts (4-5%)
    """)
    st.caption("🟢 Lowest risk, lowest returns")

with col2:
    st.write("**🌍 Emerging Markets (BBB/BB)**")
    st.write("""
    - 🇨🇳 China (3-6%)
    - 🇮🇳 India (7-9%)
    - 🇧🇷 Brazil (10-12%)
    - 🇿🇦 South Africa (10-13%)
    """)
    st.caption("🟡 Moderate risk, higher returns")

with col3:
    st.write("**⚠️ High Risk (B/CCC)**")
    st.write("""
    - 🇨🇳 Evergrande (12%+)
    - 🇧🇷 Embraer (13%+)
    - 🇿🇦 Eskom (13%+)
    """)
    st.caption("🔴 High risk, highest returns")

# --- Footer ---
st.divider()
st.caption("🌍 Global Bond Tracker — Find the best yields around the world")
st.caption("📊 Data for educational purposes only • Yields shown are approximate")
st.caption(f"🕐 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

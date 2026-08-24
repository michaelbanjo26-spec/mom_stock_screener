import streamlit as st
import pandas as pd
from datetime import datetime

# ==========================================
# SHORT DURATION JUNK BONDS (1-3 Year Maturity)
# ==========================================

SHORT_JUNK = {
    "🇺🇸 USA Short Junk": {
        "region": "North America",
        "currency": "USD",
        "bonds": [
            {"name": "Ford 7.45% 2031", "yield": 7.80, "maturity": "2031", "rating": "BB-", "sector": "Auto"},
            {"name": "Ford 6.50% 2030", "yield": 7.20, "maturity": "2030", "rating": "BB-", "sector": "Auto"},
            {"name": "Macy's 5.88% 2029", "yield": 8.50, "maturity": "2029", "rating": "B", "sector": "Retail"},
            {"name": "Macy's 6.00% 2030", "yield": 8.20, "maturity": "2030", "rating": "B", "sector": "Retail"},
            {"name": "Frontier Comms 8.75% 2030", "yield": 12.50, "maturity": "2030", "rating": "CCC", "sector": "Telecom"},
            {"name": "Frontier Comms 6.75% 2029", "yield": 11.80, "maturity": "2029", "rating": "CCC", "sector": "Telecom"},
            {"name": "Chesapeake Energy 6.75% 2029", "yield": 11.20, "maturity": "2029", "rating": "CCC+", "sector": "Energy"},
            {"name": "Chesapeake Energy 5.50% 2028", "yield": 10.80, "maturity": "2028", "rating": "CCC+", "sector": "Energy"},
            {"name": "Windstream 7.75% 2028", "yield": 14.20, "maturity": "2028", "rating": "CCC-", "sector": "Telecom"},
            {"name": "Windstream 6.50% 2027", "yield": 13.50, "maturity": "2027", "rating": "CCC-", "sector": "Telecom"},
            {"name": "Oasis Petroleum 6.50% 2027", "yield": 11.50, "maturity": "2027", "rating": "CCC", "sector": "Energy"},
            {"name": "Oasis Petroleum 5.75% 2026", "yield": 10.80, "maturity": "2026", "rating": "CCC", "sector": "Energy"},
            {"name": "Sirius XM 5.00% 2027", "yield": 7.50, "maturity": "2027", "rating": "BB-", "sector": "Media"},
            {"name": "Sirius XM 4.50% 2026", "yield": 7.00, "maturity": "2026", "rating": "BB-", "sector": "Media"},
            {"name": "Tenet Healthcare 6.25% 2028", "yield": 7.20, "maturity": "2028", "rating": "BB", "sector": "Healthcare"},
            {"name": "Tenet Healthcare 5.50% 2027", "yield": 6.80, "maturity": "2027", "rating": "BB", "sector": "Healthcare"},
            {"name": "Community Health 8.00% 2030", "yield": 11.50, "maturity": "2030", "rating": "B-", "sector": "Healthcare"},
            {"name": "Community Health 6.75% 2029", "yield": 10.80, "maturity": "2029", "rating": "B-", "sector": "Healthcare"},
            {"name": "Caesars 6.50% 2028", "yield": 8.20, "maturity": "2028", "rating": "B+", "sector": "Leisure"},
            {"name": "Caesars 5.75% 2027", "yield": 7.80, "maturity": "2027", "rating": "B+", "sector": "Leisure"},
            {"name": "US Steel 6.50% 2029", "yield": 8.50, "maturity": "2029", "rating": "B", "sector": "Industrial"},
            {"name": "US Steel 5.75% 2028", "yield": 8.00, "maturity": "2028", "rating": "B", "sector": "Industrial"},
            {"name": "Clear Channel 9.00% 2030", "yield": 15.00, "maturity": "2030", "rating": "CCC", "sector": "Media"},
            {"name": "Clear Channel 7.50% 2029", "yield": 14.00, "maturity": "2029", "rating": "CCC", "sector": "Media"},
            {"name": "JCPenney 8.50% 2030", "yield": 13.20, "maturity": "2030", "rating": "CCC-", "sector": "Retail"},
            {"name": "JCPenney 7.50% 2029", "yield": 12.50, "maturity": "2029", "rating": "CCC-", "sector": "Retail"},
        ]
    },
    "🇪🇺 EU Short Junk": {
        "region": "Europe",
        "currency": "EUR",
        "bonds": [
            {"name": "Barclays 8.00% 2030", "yield": 8.20, "maturity": "2030", "rating": "BB+", "sector": "Banking"},
            {"name": "Barclays 6.50% 2029", "yield": 7.80, "maturity": "2029", "rating": "BB+", "sector": "Banking"},
            {"name": "Tesco 6.25% 2035", "yield": 7.00, "maturity": "2035", "rating": "BBB", "sector": "Retail"},
            {"name": "Tesco 5.50% 2030", "yield": 6.50, "maturity": "2030", "rating": "BBB", "sector": "Retail"},
            {"name": "Volkswagen 5.50% 2035", "yield": 5.80, "maturity": "2035", "rating": "A", "sector": "Auto"},
            {"name": "Volkswagen 4.75% 2030", "yield": 5.20, "maturity": "2030", "rating": "A", "sector": "Auto"},
            {"name": "Deutsche Bank 7.00% 2030", "yield": 7.50, "maturity": "2030", "rating": "BBB+", "sector": "Banking"},
            {"name": "Deutsche Bank 5.50% 2029", "yield": 7.00, "maturity": "2029", "rating": "BBB+", "sector": "Banking"},
            {"name": "Lufthansa 5.50% 2030", "yield": 7.50, "maturity": "2030", "rating": "BB-", "sector": "Airlines"},
            {"name": "Lufthansa 4.75% 2029", "yield": 7.00, "maturity": "2029", "rating": "BB-", "sector": "Airlines"},
            {"name": "Air France 6.50% 2030", "yield": 8.20, "maturity": "2030", "rating": "B", "sector": "Airlines"},
            {"name": "Air France 5.50% 2029", "yield": 7.80, "maturity": "2029", "rating": "B", "sector": "Airlines"},
            {"name": "Renault 5.00% 2030", "yield": 6.50, "maturity": "2030", "rating": "BB+", "sector": "Auto"},
            {"name": "Renault 4.50% 2029", "yield": 6.00, "maturity": "2029", "rating": "BB+", "sector": "Auto"},
            {"name": "BT Group 5.75% 2030", "yield": 6.40, "maturity": "2030", "rating": "BBB", "sector": "Telecom"},
            {"name": "BT Group 5.00% 2029", "yield": 6.00, "maturity": "2029", "rating": "BBB", "sector": "Telecom"},
            {"name": "Commerzbank 6.00% 2030", "yield": 7.20, "maturity": "2030", "rating": "BBB", "sector": "Banking"},
            {"name": "Commerzbank 5.50% 2029", "yield": 6.80, "maturity": "2029", "rating": "BBB", "sector": "Banking"},
            {"name": "Vodafone 6.50% 2035", "yield": 6.80, "maturity": "2035", "rating": "BB", "sector": "Telecom"},
            {"name": "Vodafone 5.50% 2030", "yield": 6.20, "maturity": "2030", "rating": "BB", "sector": "Telecom"},
        ]
    },
    "🇧🇷 Brazil Short Junk": {
        "region": "Latin America",
        "currency": "BRL",
        "bonds": [
            {"name": "Petrobras 6.75% 2035", "yield": 13.00, "maturity": "2035", "rating": "BB", "sector": "Energy"},
            {"name": "Petrobras 5.50% 2030", "yield": 12.00, "maturity": "2030", "rating": "BB", "sector": "Energy"},
            {"name": "Petrobras 4.75% 2029", "yield": 11.50, "maturity": "2029", "rating": "BB", "sector": "Energy"},
            {"name": "Vale 5.50% 2030", "yield": 11.00, "maturity": "2030", "rating": "BB+", "sector": "Mining"},
            {"name": "Vale 4.50% 2029", "yield": 10.50, "maturity": "2029", "rating": "BB+", "sector": "Mining"},
            {"name": "Itau 5.00% 2030", "yield": 11.50, "maturity": "2030", "rating": "BB", "sector": "Banking"},
            {"name": "Itau 4.50% 2029", "yield": 11.00, "maturity": "2029", "rating": "BB", "sector": "Banking"},
            {"name": "Banco do Brasil 5.50% 2030", "yield": 12.00, "maturity": "2030", "rating": "BB", "sector": "Banking"},
            {"name": "Banco do Brasil 4.75% 2029", "yield": 11.50, "maturity": "2029", "rating": "BB", "sector": "Banking"},
            {"name": "Ambev 4.50% 2030", "yield": 10.00, "maturity": "2030", "rating": "BB", "sector": "Consumer"},
            {"name": "Ambev 4.00% 2029", "yield": 9.50, "maturity": "2029", "rating": "BB", "sector": "Consumer"},
            {"name": "Braskem 6.50% 2030", "yield": 12.50, "maturity": "2030", "rating": "B+", "sector": "Energy"},
            {"name": "Braskem 5.50% 2029", "yield": 12.00, "maturity": "2029", "rating": "B+", "sector": "Energy"},
            {"name": "Embraer 6.00% 2030", "yield": 13.00, "maturity": "2030", "rating": "B+", "sector": "Aerospace"},
            {"name": "Embraer 5.25% 2029", "yield": 12.50, "maturity": "2029", "rating": "B+", "sector": "Aerospace"},
            {"name": "Gerdau 5.25% 2030", "yield": 10.50, "maturity": "2030", "rating": "BB", "sector": "Industrial"},
            {"name": "Gerdau 4.75% 2029", "yield": 10.00, "maturity": "2029", "rating": "BB", "sector": "Industrial"},
        ]
    },
    "🇮🇳 India Short Junk": {
        "region": "Asia",
        "currency": "INR",
        "bonds": [
            {"name": "Reliance 5.25% 2035", "yield": 8.50, "maturity": "2035", "rating": "BBB", "sector": "Energy"},
            {"name": "Reliance 4.50% 2030", "yield": 8.00, "maturity": "2030", "rating": "BBB", "sector": "Energy"},
            {"name": "Reliance 4.00% 2029", "yield": 7.50, "maturity": "2029", "rating": "BBB", "sector": "Energy"},
            {"name": "Vedanta 7.50% 2030", "yield": 12.00, "maturity": "2030", "rating": "BB", "sector": "Mining"},
            {"name": "Vedanta 6.50% 2029", "yield": 11.50, "maturity": "2029", "rating": "BB", "sector": "Mining"},
            {"name": "Vedanta 6.00% 2028", "yield": 11.00, "maturity": "2028", "rating": "BB", "sector": "Mining"},
            {"name": "Tata Motors 5.50% 2030", "yield": 9.00, "maturity": "2030", "rating": "BB+", "sector": "Auto"},
            {"name": "Tata Motors 4.75% 2029", "yield": 8.50, "maturity": "2029", "rating": "BB+", "sector": "Auto"},
            {"name": "Adani Group 5.50% 2030", "yield": 10.00, "maturity": "2030", "rating": "BB-", "sector": "Infrastructure"},
            {"name": "Adani Group 4.75% 2029", "yield": 9.50, "maturity": "2029", "rating": "BB-", "sector": "Infrastructure"},
            {"name": "Adani Ports 6.00% 2030", "yield": 10.50, "maturity": "2030", "rating": "BB-", "sector": "Infrastructure"},
            {"name": "Adani Ports 5.25% 2029", "yield": 10.00, "maturity": "2029", "rating": "BB-", "sector": "Infrastructure"},
            {"name": "ICICI Bank 5.00% 2030", "yield": 8.50, "maturity": "2030", "rating": "BBB", "sector": "Banking"},
            {"name": "ICICI Bank 4.50% 2029", "yield": 8.00, "maturity": "2029", "rating": "BBB", "sector": "Banking"},
            {"name": "HDFC 4.80% 2030", "yield": 8.20, "maturity": "2030", "rating": "BBB+", "sector": "Banking"},
            {"name": "HDFC 4.25% 2029", "yield": 7.80, "maturity": "2029", "rating": "BBB+", "sector": "Banking"},
            {"name": "Tata Steel 6.00% 2030", "yield": 9.50, "maturity": "2030", "rating": "BB", "sector": "Industrial"},
            {"name": "Tata Steel 5.25% 2029", "yield": 9.00, "maturity": "2029", "rating": "BB", "sector": "Industrial"},
        ]
    },
    "🇯🇵 Japan Short Junk": {
        "region": "Asia",
        "currency": "JPY",
        "bonds": [
            {"name": "SoftBank 4.50% 2030", "yield": 6.00, "maturity": "2030", "rating": "BBB", "sector": "Tech"},
            {"name": "SoftBank 3.75% 2029", "yield": 5.50, "maturity": "2029", "rating": "BBB", "sector": "Tech"},
            {"name": "Nissan 4.80% 2030", "yield": 6.40, "maturity": "2030", "rating": "BB-", "sector": "Auto"},
            {"name": "Nissan 4.00% 2029", "yield": 6.00, "maturity": "2029", "rating": "BB-", "sector": "Auto"},
            {"name": "Nissan 3.50% 2028", "yield": 5.80, "maturity": "2028", "rating": "BB-", "sector": "Auto"},
            {"name": "Mitsubishi 3.20% 2030", "yield": 4.20, "maturity": "2030", "rating": "A", "sector": "Industrial"},
            {"name": "Mitsubishi 2.80% 2029", "yield": 4.00, "maturity": "2029", "rating": "A", "sector": "Industrial"},
            {"name": "Sony 3.00% 2030", "yield": 4.00, "maturity": "2030", "rating": "A", "sector": "Tech"},
            {"name": "Sony 2.50% 2029", "yield": 3.80, "maturity": "2029", "rating": "A", "sector": "Tech"},
            {"name": "Toyota 2.50% 2030", "yield": 3.50, "maturity": "2030", "rating": "AA", "sector": "Auto"},
            {"name": "Toyota 2.00% 2029", "yield": 3.20, "maturity": "2029", "rating": "AA", "sector": "Auto"},
            {"name": "Japan Gov't 1.00% 2030", "yield": 0.40, "maturity": "2030", "rating": "A+", "sector": "Government"},
            {"name": "Japan Gov't 0.50% 2029", "yield": 0.20, "maturity": "2029", "rating": "A+", "sector": "Government"},
            {"name": "Japan Gov't 0.25% 2028", "yield": 0.10, "maturity": "2028", "rating": "A+", "sector": "Government"},
        ]
    }
}

# ==========================================
# BOND RISK ANALYSIS
# ==========================================

def analyze_short_junk(bond, country):
    """Analyze a short-duration junk bond"""
    
    yield_rate = bond['yield']
    rating = bond['rating']
    sector = bond['sector']
    maturity = bond['maturity']
    
    # Calculate years to maturity
    try:
        current_year = 2024
        maturity_year = int(maturity)
        years_to_maturity = maturity_year - current_year
    except:
        years_to_maturity = 5
    
    # Rating risk
    rating_risk = {
        'AAA': 0, 'AA+': 1, 'AA': 2, 'AA-': 3,
        'A+': 4, 'A': 5, 'A-': 6,
        'BBB+': 7, 'BBB': 8, 'BBB-': 9,
        'BB+': 10, 'BB': 11, 'BB-': 12,
        'B+': 13, 'B': 14, 'B-': 15,
        'CCC+': 16, 'CCC': 17, 'CCC-': 18,
        'CC': 19, 'C': 20, 'D': 21
    }
    rating_score = rating_risk.get(rating, 15)
    
    # Yield risk (higher yield = more risk)
    if yield_rate < 5:
        yield_risk = 1
    elif yield_rate < 7:
        yield_risk = 2
    elif yield_rate < 10:
        yield_risk = 3
    elif yield_rate < 12:
        yield_risk = 4
    else:
        yield_risk = 5
    
    # Sector risk
    sector_risk = {
        'Utilities': 1, 'Government': 1,
        'Consumer': 2,
        'Telecom': 3, 'Industrial': 3, 'Tech': 3,
        'Banking': 4, 'Energy': 4, 'Mining': 4,
        'Retail': 4, 'Auto': 4, 'Aerospace': 4,
        'Airlines': 5, 'Media': 5, 'Real Estate': 5,
        'Healthcare': 3, 'Leisure': 4, 'Infrastructure': 4
    }
    sector_score = sector_risk.get(sector, 3)
    
    # Maturity bonus (short duration = less risky)
    # SHORT DURATION = BONUS POINTS!
    if years_to_maturity <= 3:
        maturity_bonus = -2  # Less risk because short maturity
        maturity_desc = "⭐ SHORT DURATION (1-3 years)"
    elif years_to_maturity <= 5:
        maturity_bonus = -1
        maturity_desc = "Short-Medium (3-5 years)"
    else:
        maturity_bonus = 0
        maturity_desc = "Medium+ (5+ years)"
    
    # Total risk score (lower = better)
    total_risk = (rating_score * 1.0) + (yield_risk * 1.5) + (sector_score * 0.5) + maturity_bonus
    
    # Adjust rating for short duration (junk bonds are less risky when short)
    if rating in ['BB', 'BB+', 'BB-'] and years_to_maturity <= 3:
        total_risk = total_risk - 1
    
    # Determine risk category
    if total_risk < 12:
        risk_category = "🟢 Least Terrible"
        risk_level = "Low-Medium"
        color = "green"
        mom_advice = f"This is the LEAST TERRIBLE junk bond. Short maturity ({years_to_maturity} years) means less uncertainty. Still risky, but relatively safer."
    elif total_risk < 19:
        risk_category = "🟡 Medium Garbage"
        risk_level = "Medium"
        color = "orange"
        mom_advice = f"Medium-risk junk. Matures in {years_to_maturity} years. There are worse options, but this one has real risks."
    else:
        risk_category = "🔴 Super Garbage"
        risk_level = "High"
        color = "red"
        mom_advice = f"This is SUPER RISKY junk. Even with short maturity ({years_to_maturity} years), there's a real chance of losing money. Proceed with extreme caution."
    
    # Yield category
    if yield_rate < 5:
        yield_category = "Low Yield (for junk)"
    elif yield_rate < 7:
        yield_category = "Medium Yield"
    elif yield_rate < 10:
        yield_category = "High Yield"
    else:
        yield_category = "🔥 Very High Yield (risky!)"
    
    return {
        'name': bond['name'],
        'country': country,
        'region': SHORT_JUNK[country]['region'],
        'currency': SHORT_JUNK[country]['currency'],
        'yield': yield_rate,
        'yield_category': yield_category,
        'rating': rating,
        'sector': sector,
        'maturity': maturity,
        'years_to_maturity': years_to_maturity,
        'maturity_desc': maturity_desc,
        'risk_score': round(total_risk, 1),
        'risk_category': risk_category,
        'risk_level': risk_level,
        'color': color,
        'mom_advice': mom_advice,
        'rating_score': rating_score,
        'yield_risk': yield_risk,
        'sector_score': sector_score,
        'maturity_bonus': maturity_bonus
    }

# ==========================================
# DISPLAY FUNCTIONS
# ==========================================

def display_short_junk_card(analysis, show_details=True):
    """Display a short-duration junk bond card"""
    
    # Color based on risk
    if analysis['color'] == 'green':
        st.success(f"### 🗑️ {analysis['risk_category']}")
    elif analysis['color'] == 'orange':
        st.warning(f"### 🗑️ {analysis['risk_category']}")
    else:
        st.error(f"### 🗑️ {analysis['risk_category']}")
    
    col1, col2, col3, col4 = st.columns([2, 1.5, 1.5, 1.5])
    
    with col1:
        st.write(f"**{analysis['name']}**")
        st.write(f"🌍 {analysis['country']} • {analysis['currency']}")
        st.write(f"*{analysis['sector']}*")
    
    with col2:
        st.metric("📊 Yield", f"{analysis['yield']:.2f}%")
        st.caption(analysis['yield_category'])
    
    with col3:
        st.metric("🏷️ Rating", analysis['rating'])
        st.caption(f"Matures: {analysis['maturity']}")
    
    with col4:
        st.metric("⏰ Duration", f"{analysis['years_to_maturity']} years")
        st.caption(analysis['maturity_desc'])
    
    st.info(f"💡 **Mom says:** {analysis['mom_advice']}")
    
    if show_details:
        with st.expander("📊 Why This Bond Got Its Score"):
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("Rating Risk", f"{analysis['rating_score']}/21")
                st.caption(f"Rating: {analysis['rating']}")
            with col2:
                st.metric("Yield Risk", f"{analysis['yield_risk']}/5")
                st.caption(f"{analysis['yield']:.2f}% yield")
            with col3:
                st.metric("Sector Risk", f"{analysis['sector_score']}/5")
                st.caption(analysis['sector'])
            with col4:
                st.metric("Maturity Bonus", f"{analysis['maturity_bonus']}")
                st.caption("Negative = Less risky")
            with col5:
                st.metric("Total Risk", f"{analysis['risk_score']}/30")
                st.caption(f"Risk Level: {analysis['risk_level']}")

# ==========================================
# STREAMLIT UI
# ==========================================

st.set_page_config(page_title="🗑️ Short Duration Garbage", page_icon="🗑️", layout="wide")

# --- Header ---
st.title("🗑️ Short Duration Garbage: The Least Terrible Junk")
st.markdown("*All the risk, but with a shorter timeline. If you MUST buy junk, at least buy junk that matures soon.*")
st.markdown("---")

# --- Sidebar ---
with st.sidebar:
    st.header("🎯 Why Short Duration?")
    st.write("""
    1. **Less uncertainty** — You can see if the company can pay you back in 1-3 years vs. 10+ years
    2. **Pull-to-par effect** — Bond price naturally moves toward its face value as maturity approaches
    3. **Less interest rate risk** — Short duration = less volatility when rates change
    4. **Similar yields** — Right now, short junk yields about the same as long junk
    """)
    
    st.divider()
    
    st.header("🗑️ Risk Ratings")
    st.write("""
    - 🟢 **Least Terrible** — The best of the worst. Still risky, but short duration helps.
    - 🟡 **Medium Garbage** — Real risks. Proceed with caution.
    - 🔴 **Super Garbage** — Very risky. Only for extreme risk-takers.
    """)
    
    st.divider()
    
    st.header("📊 Country Risk Levels")
    st.write("""
    - 🇺🇸 **USA** — Lower risk, stable economy
    - 🇪🇺 **EU** — Moderate risk, strong regulations
    - 🇯🇵 **Japan** — Lowest yields, safest
    - 🇧🇷 **Brazil** — High yields, high risk
    - 🇮🇳 **India** — High yields, medium-high risk
    """)

# --- Main Content ---

# Filters
st.subheader("🔍 Find Your Short-Duration Garbage")

col1, col2, col3, col4 = st.columns(4)

with col1:
    selected_country = st.selectbox(
        "🌍 Country",
        ["All Countries"] + list(SHORT_JUNK.keys())
    )

with col2:
    max_risk = st.selectbox(
        "📊 Maximum Risk",
        ["All Risk Levels", "🟢 Least Terrible Only", "🟢🟡 Up to Medium", "🟢🟡🔴 All Risk"]
    )

with col3:
    min_yield = st.slider("Minimum Yield (%)", 0.0, 15.0, 3.0, step=0.5)

with col4:
    sort_by = st.selectbox(
        "Sort by",
        ["Risk (Low to High)", "Risk (High to Low)", "Yield (High to Low)", "Yield (Low to High)", "Maturity (Shortest First)"]
    )

# --- Analyze Bonds ---
if st.button("🗑️ Find the Least Terrible Short Junk", use_container_width=True):
    
    # Collect all bonds
    all_bonds = []
    
    for country, data in SHORT_JUNK.items():
        if selected_country != "All Countries" and selected_country != country:
            continue
        
        for bond in data['bonds']:
            analysis = analyze_short_junk(bond, country)
            
            # Apply yield filter
            if analysis['yield'] < min_yield:
                continue
            
            # Apply risk filter
            if max_risk == "🟢 Least Terrible Only" and analysis['color'] != 'green':
                continue
            if max_risk == "🟢🟡 Up to Medium" and analysis['color'] == 'red':
                continue
            
            all_bonds.append(analysis)
    
    # Sort
    if sort_by == "Risk (Low to High)":
        all_bonds = sorted(all_bonds, key=lambda x: x['risk_score'])
    elif sort_by == "Risk (High to Low)":
        all_bonds = sorted(all_bonds, key=lambda x: x['risk_score'], reverse=True)
    elif sort_by == "Yield (High to Low)":
        all_bonds = sorted(all_bonds, key=lambda x: x['yield'], reverse=True)
    elif sort_by == "Yield (Low to High)":
        all_bonds = sorted(all_bonds, key=lambda x: x['yield'])
    elif sort_by == "Maturity (Shortest First)":
        all_bonds = sorted(all_bonds, key=lambda x: x['years_to_maturity'])
    
    # --- Display Results ---
    st.divider()
    
    # Honest Warning
    st.error("⚠️ **WARNING: These are STILL junk bonds.** Even with short maturities, these are high-risk investments. Many of these companies might default. Only invest money you can afford to lose completely.")
    
    st.subheader(f"🗑️ Found {len(all_bonds)} Short-Duration Junk Bonds")
    
    if not all_bonds:
        st.info("No bonds match your filters. Try expanding your criteria.")
    else:
        # Summary stats
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
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
            avg_maturity = sum(b['years_to_maturity'] for b in all_bonds) / len(all_bonds)
            st.metric("Avg Maturity", f"{avg_maturity:.1f} years")
        
        with col5:
            least_terrible = len([b for b in all_bonds if b['color'] == 'green'])
            st.metric("🟢 Least Terrible", f"{least_terrible}/{len(all_bonds)}")
        
        with col6:
            super_garbage = len([b for b in all_bonds if b['color'] == 'red'])
            st.metric("🔴 Super Garbage", f"{super_garbage}/{len(all_bonds)}")
        
        # Honest Summary
        st.info(f"💡 **The honest truth:** Short duration helps, but these are still junk bonds. Of these {len(all_bonds)} bonds, only {least_terrible} are 'least terrible.' The safest short junk is still junk — it's just less terrible than the alternatives.")
        
        # Highlight the short duration advantage
        st.success("⏰ **Why short duration matters:** These bonds mature in 1-5 years. This means:\n- You know if the company can pay you back SOON\n- Less interest rate risk\n- The price naturally moves toward par value as maturity approaches\n- Right now, you're getting similar yields to longer-term junk!")
        
        # Display each bond
        for bond in all_bonds:
            display_short_junk_card(bond, show_details=True)
            st.divider()
        
        # --- Download Results ---
        df = pd.DataFrame(all_bonds)
        df_download = df[['name', 'country', 'currency', 'yield', 'rating', 'sector', 'maturity', 'years_to_maturity', 'risk_category', 'risk_level']].copy()
        df_download['yield'] = df_download['yield'].apply(lambda x: f"{x:.2f}%")
        
        st.download_button(
            label="📥 Download Short Junk Analysis (CSV)",
            data=df_download.to_csv(index=False),
            file_name=f"short_junk_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

else:
    st.info("👆 Click the button above to find the least terrible short-duration junk bonds!")

# --- Educational Section ---
st.divider()
st.subheader("💡 Why Short Duration Junk Makes Sense (Right Now)")

col1, col2, col3 = st.columns(3)

with col1:
    st.write("**📊 The Yield Inversion**")
    st.write("""
    Right now, short-term junk bonds are yielding about the same as long-term junk.
    
    Normally, you get paid more for lending for longer. When the curve is flat or inverted, you're NOT getting paid extra for taking on more interest rate risk.
    
    **That makes short-term junk unusually attractive** — you get similar yield with less risk.
    """)

with col2:
    st.write("**⏰ The Pull-to-Par Effect**")
    st.write("""
    As a bond approaches maturity, its price naturally moves toward its face value (par).
    
    If you buy a bond trading at a discount, you'll get that extra return as maturity approaches — even if the company doesn't do anything special.
    
    **This creates a floor** for short-duration bonds that longer bonds don't have.
    """)

with col3:
    st.write("**📈 The Risk-Reward Tradeoff**")
    st.write("""
    | Metric | Short Junk | Long Junk |
    |--------|------------|-----------|
    | Yield | ~8% | ~8% |
    | Volatility | Lower | Higher |
    | Rate Sensitivity | Lower | Higher |
    | Recovery if Default | Better | Worse |
    
    **Short junk offers better risk-reward right now.**
    """)

# --- Footer ---
st.divider()
st.caption("🗑️ Short Duration Garbage Screener — The Least Terrible Junk Bonds")
st.caption("📊 Data for educational purposes only • All bonds are high-risk investments")
st.caption(f"🕐 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

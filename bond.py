import streamlit as st
import pandas as pd
from datetime import datetime

# ==========================================
# BOND DATA (Simplified for Mom)
# ==========================================

BOND_CATEGORIES = {
    "🏛️ US Treasuries": {
        "description": "Backed by the US government — safest investment",
        "risk": "🟢 Lowest",
        "examples": [
            {"name": "3-Month T-Bill", "yield": 5.25, "maturity": "0.25 years", "rating": "AAA", "callable": False},
            {"name": "6-Month T-Bill", "yield": 5.30, "maturity": "0.5 years", "rating": "AAA", "callable": False},
            {"name": "1-Year T-Bill", "yield": 5.15, "maturity": "1 year", "rating": "AAA", "callable": False},
            {"name": "2-Year Treasury", "yield": 4.85, "maturity": "2 years", "rating": "AAA", "callable": False},
            {"name": "5-Year Treasury", "yield": 4.50, "maturity": "5 years", "rating": "AAA", "callable": False},
            {"name": "10-Year Treasury", "yield": 4.25, "maturity": "10 years", "rating": "AAA", "callable": False},
            {"name": "30-Year Treasury", "yield": 4.40, "maturity": "30 years", "rating": "AAA", "callable": False},
        ]
    },
    "🏢 Investment Grade Corporate": {
        "description": "Large, stable companies — very safe",
        "risk": "🟡 Low to Moderate",
        "examples": [
            {"name": "Apple 4.65% 2046", "yield": 4.80, "maturity": "22 years", "rating": "AA+", "callable": False},
            {"name": "Microsoft 3.45% 2050", "yield": 4.60, "maturity": "26 years", "rating": "AAA", "callable": False},
            {"name": "JPMorgan 4.95% 2035", "yield": 5.10, "maturity": "11 years", "rating": "A", "callable": True},
            {"name": "Walmart 3.70% 2045", "yield": 4.75, "maturity": "21 years", "rating": "AA", "callable": False},
            {"name": "IBM 4.15% 2040", "yield": 4.90, "maturity": "16 years", "rating": "A", "callable": True},
            {"name": "Disney 4.70% 2050", "yield": 5.00, "maturity": "26 years", "rating": "A", "callable": False},
            {"name": "Coca-Cola 3.85% 2045", "yield": 4.65, "maturity": "21 years", "rating": "AA", "callable": False},
            {"name": "McDonald's 4.20% 2048", "yield": 4.80, "maturity": "24 years", "rating": "A+", "callable": True},
            {"name": "Amazon 3.80% 2047", "yield": 4.70, "maturity": "23 years", "rating": "AA-", "callable": False},
            {"name": "Berkshire 3.50% 2050", "yield": 4.55, "maturity": "26 years", "rating": "AA", "callable": False},
        ]
    },
    "💰 High-Yield Corporate (Junk)": {
        "description": "Riskier companies — higher yields but more risk",
        "risk": "🟠 Moderate to High",
        "examples": [
            {"name": "Tesla 5.30% 2045", "yield": 6.80, "maturity": "21 years", "rating": "BB", "callable": True},
            {"name": "Ford 6.10% 2040", "yield": 7.20, "maturity": "16 years", "rating": "BB-", "callable": True},
            {"name": "Uber 6.25% 2048", "yield": 7.50, "maturity": "24 years", "rating": "BB", "callable": False},
            {"name": "Delta Air 5.25% 2050", "yield": 6.50, "maturity": "26 years", "rating": "BB", "callable": True},
            {"name": "Macy's 6.75% 2043", "yield": 8.10, "maturity": "19 years", "rating": "B", "callable": True},
            {"name": "American Airlines 5.50% 2046", "yield": 7.00, "maturity": "22 years", "rating": "B+", "callable": True},
            {"name": "Nissan 4.80% 2045", "yield": 6.40, "maturity": "21 years", "rating": "BB-", "callable": False},
            {"name": "Vodafone 5.20% 2048", "yield": 6.20, "maturity": "24 years", "rating": "BB", "callable": True},
        ]
    },
    "🏛️ Municipal Bonds": {
        "description": "Government bonds — often tax-free! 🎉",
        "risk": "🟢 Low (AAA ratings common)",
        "examples": [
            {"name": "NYC GO 5.00% 2045", "yield": 4.20, "maturity": "21 years", "rating": "AAA", "callable": True, "tax_free": True},
            {"name": "California 4.75% 2050", "yield": 4.10, "maturity": "26 years", "rating": "AA+", "callable": True, "tax_free": True},
            {"name": "Texas 4.50% 2048", "yield": 4.00, "maturity": "24 years", "rating": "AAA", "callable": False, "tax_free": True},
            {"name": "Florida 5.20% 2046", "yield": 4.30, "maturity": "22 years", "rating": "AA", "callable": True, "tax_free": True},
            {"name": "Illinois 6.00% 2045", "yield": 5.50, "maturity": "21 years", "rating": "A", "callable": True, "tax_free": True},
            {"name": "Massachusetts 4.30% 2050", "yield": 3.90, "maturity": "26 years", "rating": "AA+", "callable": False, "tax_free": True},
        ]
    },
    "📈 Agency Bonds": {
        "description": "Backed by government agencies — very safe",
        "risk": "🟢 Low",
        "examples": [
            {"name": "Fannie Mae 4.50% 2035", "yield": 4.80, "maturity": "11 years", "rating": "AAA", "callable": True},
            {"name": "Freddie Mac 4.75% 2040", "yield": 4.90, "maturity": "16 years", "rating": "AAA", "callable": True},
            {"name": "Ginnie Mae 5.00% 2045", "yield": 5.10, "maturity": "21 years", "rating": "AAA", "callable": False},
            {"name": "FHLB 4.60% 2038", "yield": 4.85, "maturity": "14 years", "rating": "AAA", "callable": True},
        ]
    }
}

# ==========================================
# TREASURY YIELDS (Current rates)
# ==========================================

def get_treasury_yields():
    """Get current Treasury yields (simplified)"""
    # These are approximate current rates (as of 2024)
    return {
        '3mo': 5.25,
        '2yr': 4.85,
        '5yr': 4.50,
        '10yr': 4.25,
        '30yr': 4.40
    }

# ==========================================
# BOND ANALYSIS FUNCTION
# ==========================================

def analyze_bond(bond_data, treasury_yields):
    """Analyze a bond and return a simple scorecard"""
    
    # Get yield
    yield_rate = bond_data['yield']
    
    # Get maturity
    maturity_str = bond_data['maturity']
    maturity_years = float(maturity_str.split()[0]) if 'years' in maturity_str else 10
    
    # Determine closest Treasury for comparison
    if maturity_years <= 1:
        treasury_key = '3mo'
    elif maturity_years <= 3:
        treasury_key = '2yr'
    elif maturity_years <= 7:
        treasury_key = '5yr'
    elif maturity_years <= 15:
        treasury_key = '10yr'
    else:
        treasury_key = '30yr'
    
    treasury_yield = treasury_yields.get(treasury_key, 4.0)
    
    # Calculate spread (extra yield over Treasury)
    spread = yield_rate - treasury_yield
    
    # Credit risk assessment
    rating = bond_data['rating']
    if rating in ['AAA', 'AA+', 'AA']:
        credit_risk = "🟢 Very Low"
        credit_score = 5
    elif rating in ['AA-', 'A+', 'A']:
        credit_risk = "🟢 Low"
        credit_score = 4
    elif rating in ['A-', 'BBB+', 'BBB']:
        credit_risk = "🟡 Moderate"
        credit_score = 3
    elif rating in ['BBB-', 'BB+', 'BB']:
        credit_risk = "🟠 Some Risk"
        credit_score = 2
    elif rating in ['BB-', 'B+', 'B']:
        credit_risk = "🔴 High Risk"
        credit_score = 1
    else:
        credit_risk = "🔴 Very High Risk"
        credit_score = 0
    
    # Call risk
    if bond_data.get('callable', False):
        call_risk = "⚠️ Callable (they might pay you back early)"
        call_score = 0
    else:
        call_risk = "✅ Not callable (you get interest until maturity)"
        call_score = 1
    
    # Tax-free bonus
    if bond_data.get('tax_free', False):
        tax_note = "🎉 Tax-free! (Good for high-tax states)"
        tax_score = 1
    else:
        tax_note = "💰 Taxable (normal income tax applies)"
        tax_score = 0
    
    # Overall rating
    total_score = credit_score + call_score + tax_score
    
    # Normalize to 5-star
    if total_score >= 6:
        stars = "⭐⭐⭐⭐⭐"
        rating_text = "🌟 EXCELLENT — Strong buy!"
        color = "green"
        mom_advice = "This bond is a winner! Great yield, low risk, and good protection against early repayment."
    elif total_score >= 5:
        stars = "⭐⭐⭐⭐"
        rating_text = "👍 GOOD — Solid choice"
        color = "green"
        mom_advice = "Good bond with attractive features. Consider adding to your portfolio."
    elif total_score >= 4:
        stars = "⭐⭐⭐"
        rating_text = "🤔 OK — Decent option"
        color = "orange"
        mom_advice = "This bond is fine, but there might be better options. Compare the yield with the risks."
    elif total_score >= 3:
        stars = "⭐⭐"
        rating_text = "⚠️ RISKY — Be careful"
        color = "orange"
        mom_advice = "Higher yield comes with higher risk. Make sure you're comfortable with the credit quality."
    else:
        stars = "⭐"
        rating_text = "❌ POOR — Skip it"
        color = "red"
        mom_advice = "Too much risk for the yield. You can find better returns with less risk elsewhere."
    
    return {
        'name': bond_data['name'],
        'yield': yield_rate,
        'spread': spread,
        'maturity': maturity_str,
        'rating': rating,
        'credit_risk': credit_risk,
        'call_risk': call_risk,
        'tax_note': tax_note,
        'stars': stars,
        'rating_text': rating_text,
        'color': color,
        'mom_advice': mom_advice,
        'treasury_benchmark': treasury_key,
        'treasury_yield': treasury_yield,
        'call_score': call_score,
        'tax_score': tax_score,
        'credit_score': credit_score,
        'total_score': total_score
    }

# ==========================================
# DISPLAY FUNCTIONS
# ==========================================

def display_bond_card(analysis):
    """Display a bond as a simple scorecard"""
    
    # Color the card based on rating
    if analysis['color'] == 'green':
        st.success(f"### {analysis['stars']} {analysis['rating_text']}")
    elif analysis['color'] == 'orange':
        st.warning(f"### {analysis['stars']} {analysis['rating_text']}")
    else:
        st.error(f"### {analysis['stars']} {analysis['rating_text']}")
    
    # Main bond info
    st.write(f"**{analysis['name']}**")
    st.write(f"*Rating: {analysis['rating']}*")
    
    # Yield and spread (most important)
    col1, col2, col3 = st.columns(3)
    with col1:
        spread_display = f"+{analysis['spread']:.2f}%" if analysis['spread'] > 0 else f"{analysis['spread']:.2f}%"
        delta_color = "normal" if analysis['spread'] > 0 else "inverse"
        st.metric(
            "📊 Yield",
            f"{analysis['yield']:.2f}%",
            delta=f"{spread_display} vs Treasury",
            delta_color=delta_color
        )
        st.caption(f"Treasury: {analysis['treasury_benchmark']} @ {analysis['treasury_yield']:.2f}%")
    
    with col2:
        st.metric("⏰ Maturity", analysis['maturity'])
        st.caption("When you get your money back")
    
    with col3:
        st.metric("🛡️ Credit Risk", analysis['credit_risk'])
        st.caption(f"Rating: {analysis['rating']}")
    
    # Risk summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"**Call Risk:** {analysis['call_risk']}")
    with col2:
        st.write(f"**Tax Status:** {analysis['tax_note']}")
    with col3:
        st.write(f"**Score:** {analysis['total_score']}/7")
        st.write(f"- Credit: {analysis['credit_score']}/5")
        st.write(f"- Call: {analysis['call_score']}/1")
        if analysis['tax_score'] == 1:
            st.write(f"- Tax-Free: {analysis['tax_score']}/1")
    
    # Mom advice
    st.info(f"💡 **Mom says:** {analysis['mom_advice']}")

def display_explanation():
    """Display bond term explanations"""
    explanations = {
        "Yield": "💰 The annual interest you earn. Higher = more money, but often means more risk.",
        "Credit Rating": "📊 A grade from AAA (safest) to D (risky). Think of it like a credit score for companies.",
        "Maturity": "📅 When you get your original investment back. Longer = more risk but often higher yield.",
        "Callable": "⚠️ The company can pay you back early. Bad for you if interest rates drop.",
        "Spread": "📈 Extra yield compared to Treasuries. Higher spread = more compensation for risk.",
        "Treasuries": "🏛️ US government bonds — the safest investment. Everything else is measured against them.",
        "Tax-Free": "🎉 Interest is exempt from state/local taxes. Great for high-tax states!",
    }
    
    for term, explanation in explanations.items():
        with st.expander(f"📘 {term}"):
            st.write(explanation)

# ==========================================
# STREAMLIT UI
# ==========================================

st.set_page_config(page_title="Mom's Bond Picker", page_icon="🏦", layout="wide")

# --- Header ---
st.title("🏦 Mom's Bond Picker")
st.markdown("*Find bonds that pay you well without taking too much risk!*")
st.markdown("---")

# --- Sidebar ---
with st.sidebar:
    st.header("🎯 How It Works")
    st.write("""
    1. **Pick a bond category** (Treasuries, Corporate, etc.)
    2. **Compare yields** to US Treasuries
    3. **Check risks** (credit, call, maturity)
    4. **Get a simple rating** — Buy, Hold, or Skip!
    """)
    
    st.divider()
    
    st.header("📖 Bond Terms Made Simple")
    display_explanation()
    
    st.divider()
    
    # Treasury yield display
    st.header("📊 Current Treasury Yields")
    yields = get_treasury_yields()
    for key, value in yields.items():
        st.write(f"- {key}: **{value:.2f}%**")
    st.caption("Updated daily • Benchmark for all bonds")

# --- Main Content ---

# Get current Treasury yields
treasury_yields = get_treasury_yields()

# Bond category selection
selected_category = st.selectbox(
    "🏭 Pick a bond category:",
    list(BOND_CATEGORIES.keys())
)

category = BOND_CATEGORIES[selected_category]

# Display category info
col1, col2 = st.columns([2, 1])
with col1:
    st.write(f"**{category['description']}**")
    st.write(f"Risk Level: {category['risk']}")
with col2:
    st.metric("Available Bonds", len(category['examples']))

st.divider()

# --- Display Bonds ---
st.subheader(f"📋 {selected_category} Bonds")

# Add filters
col1, col2, col3 = st.columns(3)
with col1:
    min_yield = st.slider("Minimum Yield (%)", 0.0, 10.0, 0.0, step=0.5)
with col2:
    max_maturity = st.slider("Max Maturity (years)", 1, 30, 30, step=5)
with col3:
    only_callable = st.selectbox(
        "Callable?", 
        ["All", "Not Callable", "Callable Only"],
        help="Callable = company can pay you back early"
    )

# Analyze each bond
results = []
for bond in category['examples']:
    analysis = analyze_bond(bond, treasury_yields)
    
    # Apply filters
    maturity_years = float(analysis['maturity'].split()[0]) if 'years' in analysis['maturity'] else 0
    
    if analysis['yield'] >= min_yield and maturity_years <= max_maturity:
        if only_callable == "Not Callable" and bond.get('callable', False):
            continue
        elif only_callable == "Callable Only" and not bond.get('callable', False):
            continue
        results.append(analysis)

# Sort by yield (highest first)
results = sorted(results, key=lambda x: x['yield'], reverse=True)

if not results:
    st.warning("No bonds match your filters. Try adjusting them.")
else:
    st.success(f"Found {len(results)} bonds matching your criteria")
    
    # Display each bond
    for result in results:
        display_bond_card(result)
        st.divider()

# --- Comparison Table ---
st.subheader("📊 Quick Comparison")

if results:
    df = pd.DataFrame(results)
    display_df = df[['name', 'rating', 'yield', 'spread', 'maturity', 'credit_risk']].copy()
    display_df['yield'] = display_df['yield'].apply(lambda x: f"{x:.2f}%")
    display_df['spread'] = display_df['spread'].apply(lambda x: f"+{x:.2f}%" if x > 0 else f"{x:.2f}%")
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "name": "Bond Name",
            "rating": "Rating",
            "yield": "Yield",
            "spread": "Spread vs Treasury",
            "maturity": "Maturity",
            "credit_risk": "Credit Risk"
        }
    )

    # Download button
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download Bond Analysis (CSV)",
        data=csv,
        file_name=f"bond_analysis_{selected_category}.csv",
        mime="text/csv"
    )

# --- Educational Section ---
st.divider()
st.subheader("💡 Understanding Bond Yields")

col1, col2, col3 = st.columns(3)

with col1:
    st.write("**What is a good yield?**")
    st.write("""
    - **4-5%:** Good for safe bonds
    - **5-6%:** Fair for moderate risk
    - **6%+:** Higher risk typically required
    """)

with col2:
    st.write("**What does spread tell me?**")
    st.write("""
    - **>1.5%:** Good compensation for risk
    - **0.5-1.5%:** Fair compensation
    - **<0.5%:** Not worth the extra risk
    """)

with col3:
    st.write("**When to avoid bonds:**")
    st.write("""
    - ❌ Callable if rates are falling
    - ❌ Low rating (BB or lower)
    - ❌ Negative spread vs Treasuries
    - ❌ Long maturity + poor rating
    """)

# --- Footer ---
st.divider()
st.caption("💡 Simplified bond analysis for everyday investors")
st.caption("📊 Data for educational purposes only • Yields shown are approximate")
st.caption(f"🕐 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# --- Yield Calculator in Sidebar ---
with st.sidebar.expander("🧮 Bond Yield Calculator"):
    st.write("Calculate your annual income from a bond:")
    
    col1, col2 = st.columns(2)
    with col1:
        investment = st.number_input("Investment ($)", min_value=1000, value=10000, step=1000)
    with col2:
        yield_rate = st.number_input("Yield (%)", min_value=0.0, max_value=20.0, value=5.0, step=0.5)
    
    annual_income = investment * (yield_rate / 100)
    monthly_income = annual_income / 12
    
    st.write(f"**Annual income:** ${annual_income:,.2f}")
    st.write(f"**Monthly income:** ${monthly_income:,.2f}")
    
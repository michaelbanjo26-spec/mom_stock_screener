import streamlit as st

st.set_page_config(
    page_title="Junior Mining Screener",
    page_icon="⛏️",
    layout="centered"
)

st.title("⛏️ Junior Mining Screener")
st.caption("A simple first-pass screen for TSX / TSXV junior mining companies.")


# -------------------------
# Helper functions
# -------------------------

def score_runway(months):
    if months >= 24:
        return 100
    elif months >= 18:
        return 85
    elif months >= 12:
        return 65
    elif months >= 6:
        return 35
    else:
        return 10


def calculate_scores(data):

    asset = (
        data["resource_size"] * 0.25 +
        data["grade"] * 0.30 +
        data["exploration"] * 0.20 +
        data["resource_confidence"] * 0.25
    )

    runway = score_runway(data["cash_runway"])

    funding = (
        runway * 0.50 +
        data["debt"] * 0.25 +
        data["dilution"] * 0.25
    )

    management = (
        data["track_record"] * 0.50 +
        data["insider_alignment"] * 0.50
    )

    mineability = (
        data["infrastructure"] * 0.20 +
        data["jurisdiction"] * 0.15 +
        data["permitting"] * 0.15 +
        data["metallurgy"] * 0.20 +
        data["economics"] * 0.30
    )

    overall = (
        asset * 0.35 +
        funding * 0.20 +
        management * 0.20 +
        mineability * 0.25
    )

    return {
        "Asset": round(asset),
        "Funding": round(funding),
        "Management": round(management),
        "Mineability": round(mineability),
        "Overall": round(overall)
    }


def get_status(score):
    if score >= 80:
        return "🟢 Strong"
    elif score >= 65:
        return "🟡 Moderate"
    elif score >= 50:
        return "🟠 Speculative"
    else:
        return "🔴 Weak"


def get_verdict(scores, data):

    warnings = []

    if data["cash_runway"] < 6:
        warnings.append("Severe financing risk")

    if data["cash_runway"] < 12:
        warnings.append("Financing may be needed soon")

    if data["dilution"] < 40:
        warnings.append("Dilution risk")

    if data["permitting"] < 30:
        warnings.append("Major permitting risk")

    if data["metallurgy"] < 30:
        warnings.append("Metallurgical risk")

    if "Severe financing risk" in warnings:
        verdict = "⚠️ HIGH RISK"

    elif scores["Overall"] >= 80:
        verdict = "⭐ WORTH INVESTIGATING"

    elif scores["Overall"] >= 65:
        verdict = "🔎 INTERESTING"

    elif scores["Overall"] >= 50:
        verdict = "🟠 SPECULATIVE"

    else:
        verdict = "🔴 LOW PRIORITY"

    return verdict, warnings


# -------------------------
# Company information
# -------------------------

st.header("Company")

ticker = st.text_input(
    "Ticker",
    placeholder="e.g. ABC.V"
)

company_name = st.text_input(
    "Company name",
    placeholder="e.g. ABC Mining"
)


# -------------------------
# Asset
# -------------------------

st.header("⛏️ Asset")

st.caption(
    "How attractive is the mineral deposit itself?"
)

resource_size = st.slider(
    "Resource size",
    0, 100, 50
)

grade = st.slider(
    "Grade",
    0, 100, 50
)

exploration = st.slider(
    "Exploration upside",
    0, 100, 50
)

resource_confidence = st.slider(
    "Resource confidence",
    0, 100, 50
)


# -------------------------
# Funding
# -------------------------

st.header("💰 Funding")

st.caption(
    "Can the company survive long enough to prove the project?"
)

cash_runway = st.number_input(
    "Cash runway (months)",
    min_value=0.0,
    value=18.0,
    step=1.0
)

debt = st.slider(
    "Debt position",
    0, 100, 75
)

dilution = st.slider(
    "Shareholder dilution profile",
    0, 100, 70
)


# -------------------------
# Management
# -------------------------

st.header("🧑‍💼 Management")

st.caption(
    "Does management have the experience and incentives to create value?"
)

track_record = st.slider(
    "Track record",
    0, 100, 50
)

insider_alignment = st.slider(
    "Insider ownership / alignment",
    0, 100, 50
)


# -------------------------
# Mineability
# -------------------------

st.header("🏗️ Mineability")

st.caption(
    "Could this realistically become an economically viable mine?"
)

infrastructure = st.slider(
    "Infrastructure",
    0, 100, 50
)

jurisdiction = st.slider(
    "Jurisdiction",
    0, 100, 50
)

permitting = st.slider(
    "Permitting",
    0, 100, 50
)

metallurgy = st.slider(
    "Metallurgy",
    0, 100, 50
)

economics = st.slider(
    "Potential economics",
    0, 100, 50
)


# -------------------------
# Calculate
# -------------------------

data = {
    "resource_size": resource_size,
    "grade": grade,
    "exploration": exploration,
    "resource_confidence": resource_confidence,

    "cash_runway": cash_runway,
    "debt": debt,
    "dilution": dilution,

    "track_record": track_record,
    "insider_alignment": insider_alignment,

    "infrastructure": infrastructure,
    "jurisdiction": jurisdiction,
    "permitting": permitting,
    "metallurgy": metallurgy,
    "economics": economics
}


if st.button("Analyze Company", type="primary"):

    scores = calculate_scores(data)

    verdict, warnings = get_verdict(
        scores,
        data
    )

    st.divider()

    st.header(
        f"{company_name or 'Junior Mining Company'}"
    )

    if ticker:
        st.caption(ticker)

    # Overall
    st.metric(
        "Overall Score",
        f"{scores['Overall']}/100"
    )

    st.subheader(verdict)

    st.divider()

    # Four-question scorecard
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "⛏️ Asset",
            f"{scores['Asset']}/100"
        )
        st.write(get_status(scores["Asset"]))

    with col2:
        st.metric(
            "💰 Funding",
            f"{scores['Funding']}/100"
        )
        st.write(get_status(scores["Funding"]))

    col3, col4 = st.columns(2)

    with col3:
        st.metric(
            "🧑‍💼 Management",
            f"{scores['Management']}/100"
        )
        st.write(get_status(scores["Management"]))

    with col4:
        st.metric(
            "🏗️ Mineability",
            f"{scores['Mineability']}/100"
        )
        st.write(get_status(scores["Mineability"]))

    # Warnings
    st.divider()

    st.subheader("⚠️ Things to investigate")

    if warnings:
        for warning in warnings:
            st.warning(warning)
    else:
        st.success("No major warning flags.")

    # Explanation
    st.divider()

    st.subheader("What does this mean?")

    if scores["Asset"] >= 80:
        st.write(
            "The underlying mineral asset looks strong based "
            "on the inputs provided."
        )
    else:
        st.write(
            "The mineral asset deserves additional investigation."
        )

    if scores["Funding"] < 60:
        st.write(
            "Funding is a concern. Future financing could result "
            "in significant shareholder dilution."
        )
    else:
        st.write(
            "The company appears reasonably positioned to fund "
            "its next stage of development."
        )

    if scores["Management"] >= 80:
        st.write(
            "Management scores strongly on experience and "
            "shareholder alignment."
        )

    if scores["Mineability"] >= 80:
        st.write(
            "The project appears to have a relatively strong "
            "path toward potential development."
        )
        
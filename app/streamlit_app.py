import streamlit as st
import requests
import time

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="DealMind AI",
    page_icon="🧠",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

/* ---------- GLOBAL GRADIENT DARK THEME ---------- */

.stApp {
    background: linear-gradient(135deg, #0a0a12 0%, #12122a 35%, #1a1033 70%, #0d1520 100%);
    background-attachment: fixed;
}

.stApp::before {
    content: "";
    position: fixed;
    top: -20%;
    left: -10%;
    width: 50%;
    height: 50%;
    background: radial-gradient(circle, rgba(255, 77, 202, 0.12) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}

.stApp::after {
    content: "";
    position: fixed;
    bottom: -20%;
    right: -10%;
    width: 55%;
    height: 55%;
    background: radial-gradient(circle, rgba(91, 140, 255, 0.14) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}

html, body, [class*="css"] {
    color: #e8e8f0;
    font-family: 'Segoe UI', system-ui, sans-serif;
}

.block-container {
    padding-top: 2rem;
    max-width: 960px;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* ---------- TITLE ---------- */

.title {
    font-size: clamp(48px, 8vw, 72px);
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg, #FF4DCA, #5B8CFF, #B8FF5A);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-top: 10px;
    letter-spacing: -1px;
}

.subtitle {
    text-align: center;
    color: #a0a0c0;
    font-size: 20px;
    margin-bottom: 36px;
}

/* ---------- LABELS & TEXT ---------- */

label, .stMarkdown, .stMarkdown p, .stWrite {
    color: #e0e0f0 !important;
}

h3, [data-testid="stMarkdownContainer"] h3 {
    color: #ffffff !important;
    font-weight: 700 !important;
    background: linear-gradient(90deg, #FF4DCA, #5B8CFF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* ---------- INPUT ---------- */

.stTextInput label {
    color: #c8c8e0 !important;
    font-size: 16px !important;
    font-weight: 600 !important;
}

.stTextInput input {
    background: linear-gradient(145deg, #1a1a2e, #222240) !important;
    color: #ffffff !important;
    border: 1px solid rgba(91, 140, 255, 0.5) !important;
    border-radius: 14px !important;
    padding: 14px 18px !important;
    font-size: 16px !important;
    box-shadow: 0 4px 24px rgba(91, 140, 255, 0.1), inset 0 1px 0 rgba(255,255,255,0.05) !important;
}

.stTextInput input:focus {
    border-color: #FF4DCA !important;
    box-shadow: 0 0 0 2px rgba(255, 77, 202, 0.25), 0 4px 24px rgba(255, 77, 202, 0.15) !important;
}

/* ---------- BUTTON ---------- */

.stButton button {
    width: 100%;
    background: linear-gradient(90deg, #FF4DCA, #5B8CFF) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 14px 24px !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 8px 32px rgba(91, 140, 255, 0.35) !important;
}

.stButton button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 40px rgba(255, 77, 202, 0.4) !important;
}

/* ---------- DEAL CARDS (bordered containers) ---------- */

[data-testid="stVerticalBlockBorderWrapper"] {
    background: linear-gradient(145deg, rgba(26, 26, 46, 0.95), rgba(35, 35, 58, 0.9)) !important;
    border: 1px solid rgba(91, 140, 255, 0.25) !important;
    border-radius: 20px !important;
    padding: 8px 12px !important;
    margin-bottom: 16px !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35), 0 0 0 1px rgba(255, 77, 202, 0.08) inset !important;
    backdrop-filter: blur(12px);
}

[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: rgba(255, 77, 202, 0.35) !important;
    box-shadow: 0 12px 40px rgba(91, 140, 255, 0.15) !important;
}

/* ---------- PROGRESS BAR ---------- */

.stProgress > div > div {
    background: linear-gradient(90deg, #FF4DCA, #5B8CFF, #B8FF5A) !important;
    border-radius: 8px !important;
}

.stProgress > div {
    background-color: rgba(255, 255, 255, 0.08) !important;
    border-radius: 8px !important;
}

/* ---------- ALERTS ---------- */

[data-testid="stAlert"] {
    background: linear-gradient(145deg, rgba(26, 26, 46, 0.9), rgba(35, 35, 58, 0.85)) !important;
    border: 1px solid rgba(91, 140, 255, 0.3) !important;
    border-radius: 14px !important;
    color: #e0e0f0 !important;
}

div[data-baseweb="notification"] {
    background: transparent !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.markdown(
    '<div class="title">DealMind AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-powered Ecommerce Deal Intelligence Engine</div>',
    unsafe_allow_html=True
)

# ---------------------------------------------------
# INPUT
# ---------------------------------------------------

url = st.text_input(
    "Paste Ecommerce URL",
    key="product_url_input"
)

# ---------------------------------------------------
# ANALYZE BUTTON
# ---------------------------------------------------

if st.button("Analyze Deals"):

    if not url.strip():

        st.warning("Please enter a URL.")

    else:

        loading_placeholder = st.empty()

        loading_steps = [
            "🔍 Scraping ecommerce page...",
            "🧠 Detecting products...",
            "💰 Evaluating discounts...",
            "⚠ Detecting suspicious pricing...",
            "📊 Ranking best deals...",
            "🚀 Generating AI report..."
        ]

        for step in loading_steps:
            loading_placeholder.info(step)
            time.sleep(0.6)

        try:

            response = requests.get(
                "http://127.0.0.1:8000/analyze",
                params={"url": url}
            )

            data = response.json()
            analysis = data["analysis"]

            loading_placeholder.empty()

            if "error" in analysis:

                st.error(analysis["error"])

            else:

                top_deals = analysis["top_deals"]

                st.subheader("🚀 AI Ranked Best Deals")

                for index, deal in enumerate(top_deals):

                    trust_score = deal["trust_score"]

                    if trust_score >= 80:
                        score_color = "#B8FF5A"
                        badge_text = "🔥 HOT DEAL"
                    elif trust_score >= 50:
                        score_color = "#FFB84D"
                        badge_text = "⚠ DECENT DEAL"
                    else:
                        score_color = "#FF5A5A"
                        badge_text = "🚨 RISKY DEAL"

                    suspicious = deal["suspicious"]
                    status_text = "SUSPICIOUS" if suspicious else "SAFE"
                    status_color = "#FF5A5A" if suspicious else "#B8FF5A"

                    with st.container(border=True):
                        st.markdown(f"### #{index + 1} — {deal['product_name']}")
                        st.markdown(
                            f"<span style='display:inline-block; padding:8px 16px; border-radius:999px; "
                            f"font-weight:700; font-size:14px; "
                            f"background:linear-gradient(90deg, rgba(255,77,202,0.25), rgba(91,140,255,0.25)); "
                            f"border:1px solid rgba(91,140,255,0.45); color:{score_color};'>{badge_text}</span>",
                            unsafe_allow_html=True,
                        )

                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Original Price:** {deal['original_price']}")
                            st.write(f"**Discounted Price:** {deal['discounted_price']}")
                        with col2:
                            st.write(f"**Estimated Discount:** {deal['estimated_discount_percentage']}%")
                            st.markdown(
                                f"**Status:** <span style='color:{status_color}; font-weight:bold;'>{status_text}</span>",
                                unsafe_allow_html=True,
                            )

                        st.write(f"**Final Verdict:** {deal['final_verdict']}")

                        st.markdown(
                            f"<p style='font-size:22px; font-weight:bold; color:{score_color}; margin-bottom:0;'>Trust Score: {trust_score}</p>",
                            unsafe_allow_html=True,
                        )
                        st.progress(trust_score / 100)

        except Exception as e:

            st.error(f"Application Error: {str(e)}")

import streamlit as st
import base64
from pathlib import Path
from PIL import Image
from typing import Optional

def setup_page(
    title: str = "Email Spam Detector",
    logo_path: Optional[Path] = Path("image/logo.png"),
    initial_sidebar_state: str = "collapsed",
):
    """
    Configure the Streamlit page and inject the app CSS.
    Keeps same public signature as before but adds optional params for
    easier customization in the future.
    """
    logo_base64 = ""
    page_icon = "🛡️"

    if logo_path and logo_path.exists():
        try:
            with open(logo_path, "rb") as f:
                logo_base64 = base64.b64encode(f.read()).decode()
            try:
                page_icon = Image.open(logo_path)
            except Exception:
                # Keep emoji if PIL can't open
                page_icon = "🛡️"
        except Exception:
            logo_base64 = ""
            page_icon = "🛡️"

    st.set_page_config(
        page_title=title,
        page_icon=page_icon,
        layout="centered",
        initial_sidebar_state=initial_sidebar_state,
        menu_items={'Get Help': None, 'Report a bug': None, 'About': None}
    )

    st.markdown(get_css(logo_base64), unsafe_allow_html=True)


def get_css(logo_base64: str) -> str:
    """
    Returns a professional, slightly toned-down CSS theme for the app.
    Uses CSS variables and keeps a transparent background for Plotly charts.
    """
    css = """
    <style>
    :root{
        --bg-1: #0f1724; /* page background */
        --card-bg: rgba(255,255,255,0.06);
        --card-surface: rgba(255,255,255,0.04);
        --accent-1: #5b7cff; /* primary accent */
        --accent-2: #7bd389; /* secondary accent */
        --muted: #9aa4b2;
        --glass-border: rgba(255,255,255,0.06);
        --radius: 14px;
        --max-width: 1000px;
    }

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    * { box-sizing: border-box; font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial; }

    /* Basic page adjustments */
    html, body, .stApp { background: linear-gradient(180deg, var(--bg-1) 0%, #071029 100%); }
    .main .block-container { padding-top: 2.25rem; padding-bottom: 2.25rem; max-width: var(--max-width); }

    /* Hide default Streamlit chrome that is unnecessary */
    #MainMenu, footer, header { visibility: hidden; height: 0; }

    /* Header */
    .main-header {
        background: linear-gradient(135deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
        border: 1px solid var(--glass-border);
        padding: 2rem 1.5rem;
        border-radius: 18px;
        margin-bottom: 1.8rem;
        color: white;
        text-align: center;
        box-shadow: 0 6px 30px rgba(2,6,23,0.6);
    }
    .main-header h1 { font-size: 2.2rem; margin: 0 0 0.35rem 0; font-weight: 700; letter-spacing: -0.4px; }
    .main-header p { margin: 0; color: var(--muted); font-weight: 400; }

    /* Input card */
    .input-card {
        background: var(--card-bg);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius);
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    .input-card h3 { margin: 0 0 0.35rem 0; color: #e6eefc; font-weight: 600; }
    .input-card p { margin: 0; color: var(--muted); }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, var(--accent-1), #9aa8ff);
        color: white;
        border: none;
        padding: 0.95rem 1rem;
        border-radius: 12px;
        font-weight: 700;
        letter-spacing: 0.6px;
        box-shadow: 0 6px 18px rgba(48,66,129,0.28);
    }
    .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 10px 30px rgba(48,66,129,0.34); }

    /* Info & result cards */
    .info-card, .result-card {
        background: linear-gradient(180deg, var(--card-surface), rgba(255,255,255,0.02));
        border: 1px solid var(--glass-border);
        border-radius: 14px;
        padding: 1.25rem;
        color: #eaf0ff;
        box-shadow: 0 8px 28px rgba(2,6,23,0.55);
    }
    .info-title { color: var(--accent-1); font-weight: 700; margin-bottom: 0.4rem; }
    .info-desc { color: var(--muted); font-size: 0.95rem; }

    /* Result variations */
    .result-spam { border-left: 4px solid #ff6b6b; }
    .result-safe { border-left: 4px solid var(--accent-2); }

    /* Result typography */
    .result-icon { font-size: 3.2rem; display: block; margin-bottom: 0.6rem; }
    .result-text { font-size: 1.6rem; font-weight: 800; margin: 0.6rem 0; }
    .result-message { color: var(--muted); font-size: 0.98rem; }

    /* Smaller text helpers */
    .confidence-score { background: rgba(255,255,255,0.03); padding: 0.6rem; border-radius: 10px; display: inline-block; color: #fff; }

    /* Responsive tweaks */
    @media (max-width: 640px) {
        .main-header h1 { font-size: 1.6rem; }
        .result-text { font-size: 1.2rem; }
        .main .block-container { padding-left: 1rem; padding-right: 1rem; }
    }

    /* Make Plotly figures blend in (Streamlit displays plotly inside an iframe; this helps) */
    .js-plotly-plot .plot-container .svg-container { background: transparent !important; }
    </style>
    """
    if logo_base64:
        css += f'<link rel="icon" type="image/png" href="data:image/png;base64,{logo_base64}">'
    return css


def render_header(title: str = "🛡️ Email / SMS Spam Classifier", subtitle: str = "Protect your inbox from unwanted messages with AI-powered detection"):
    """
    Render a compact header. Keeps the same HTML as before but uses the new CSS.
    """
    st.markdown(f"""
        <div class="main-header">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
    """, unsafe_allow_html=True)
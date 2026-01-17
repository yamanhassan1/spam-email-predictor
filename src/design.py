import streamlit as st
import base64
from pathlib import Path
from PIL import Image
from typing import Optional, Iterable, Dict


def setup_page(
    title: str = "Email Spam Detector",
    logo_path: Optional[Path] = Path("image/logo.png"),
    initial_sidebar_state: str = "collapsed",
    theme: str = "dark",
    compact: bool = False,
):
    """
    Configure the Streamlit page and inject the app CSS.

    Kept backward compatible with previous usage (no args). Added
    theme/compact options for more advanced control.
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

    st.markdown(get_css(logo_base64, theme=theme, compact=compact), unsafe_allow_html=True)


def get_css(logo_base64: str, theme: str = "dark", compact: bool = False) -> str:
    """
    Return a more advanced, professional CSS string.

    - theme: 'dark' (default) or 'light' (available for future use)
    - compact: if True, reduce paddings and font sizes for compact displays.
    """
    # Basic theme variables (dark focused)
    css = f"""
    <style>
    :root {{
        --accent-1: #5b7cff;
        --accent-2: #7bd389;
        --muted: #9aa4b2;
        --glass-border: rgba(255,255,255,0.06);
        --card-radius: 14px;
        --max-width: 1100px;
    }}
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    * {{ font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial; box-sizing: border-box; }}
    html, body, .stApp {{ background: linear-gradient(180deg, #071029 0%, #081427 100%); }}
    .main .block-container {{ max-width: var(--max-width); padding-top: { '1rem' if compact else '2.25rem' }; padding-bottom: { '1rem' if compact else '2.25rem' }; }}
    #MainMenu, footer, header {{ visibility: hidden; height: 0; }}

    /* Header */
    .main-header {{
        background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
        border: 1px solid var(--glass-border);
        padding: { '0.9rem 1rem' if compact else '2rem 1.5rem' };
        border-radius: 16px;
        margin-bottom: 1.2rem;
        color: #eaf0ff;
        text-align: center;
        box-shadow: 0 6px 30px rgba(2,6,23,0.6);
    }}
    .main-header h1 {{ font-size: { '1.25rem' if compact else '2.2rem' }; margin: 0 0 0.25rem 0; font-weight: 700; }}
    .main-header p {{ margin: 0; color: var(--muted); font-weight: 400; font-size: { '0.8rem' if compact else '1rem' }; }}

    /* Input card */
    .input-card {{
        background: rgba(255,255,255,0.03);
        border: 1px solid var(--glass-border);
        border-radius: var(--card-radius);
        padding: { '0.8rem' if compact else '1.5rem' };
        margin-bottom: 1rem;
    }}
    .input-card h3 {{ margin: 0 0 0.35rem 0; color: #e6eefc; font-weight: 600; font-size: { '0.95rem' if compact else '1.1rem' }; }}
    .input-card p {{ margin: 0; color: var(--muted); font-size: { '0.8rem' if compact else '0.95rem' }; }}

    /* Buttons - smoother hover & focus */
    .stButton > button {{
        background: linear-gradient(90deg, var(--accent-1), #9aa8ff);
        color: white;
        border: none;
        padding: { '0.6rem 0.9rem' if compact else '0.95rem 1rem' };
        border-radius: 12px;
        font-weight: 700;
        letter-spacing: 0.6px;
        box-shadow: 0 6px 18px rgba(48,66,129,0.24);
    }}
    .stButton > button:hover {{ transform: translateY(-2px); box-shadow: 0 10px 30px rgba(48,66,129,0.32); }}
    .stButton > button:focus {{ outline: 2px solid rgba(91,124,255,0.18); }}

    /* Cards */
    .info-card, .result-card {{
        background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
        border: 1px solid var(--glass-border);
        border-radius: 12px;
        padding: { '0.8rem' if compact else '1.25rem' };
        color: #eaf0ff;
        box-shadow: 0 8px 28px rgba(2,6,23,0.5);
    }}
    .info-title {{ color: var(--accent-1); font-weight: 700; margin-bottom: 0.4rem; }}
    .info-desc {{ color: var(--muted); font-size: 0.95rem; }}

    /* Result styles - subtle left accent to communicate severity */
    .result-spam {{ border-left: 4px solid #ff6b6b; }}
    .result-safe {{ border-left: 4px solid var(--accent-2); }}

    .result-icon {{ font-size: 2.6rem; display:block; margin-bottom:0.5rem; }}
    .result-text {{ font-size: { '1rem' if compact else '1.6rem' }; font-weight: 800; margin: 0.4rem 0; }}
    .result-message {{ color: var(--muted); font-size: 0.95rem; }}

    .confidence-score {{ background: rgba(255,255,255,0.03); padding: 0.5rem; border-radius: 10px; display: inline-block; color: #fff; font-weight:600; }}

    /* Small helpers */
    .small-muted {{ color: var(--muted); font-size: 0.9rem; }}

    /* Plotly blending */
    .js-plotly-plot .plot-container .svg-container {{ background: transparent !important; }}

    /* accessible focus states for interactive elements */
    button:focus, a:focus {{ outline: 3px solid rgba(91,124,255,0.12); outline-offset: 2px; }}

    </style>
    """
    if logo_base64:
        css += f'<link rel="icon" type="image/png" href="data:image/png;base64,{logo_base64}">'

    return css


def render_header(title: str = "🛡️ Email / SMS Spam Classifier", subtitle: str = "Protect your inbox from unwanted messages with AI-powered detection"):
    """
    Render a compact header. Backwards-compatible with previous render_header().
    """
    st.markdown(f"""
        <div class="main-header">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
    """, unsafe_allow_html=True)


def render_result_card(is_spam: bool, confidence_pct: float, short_message: Optional[str] = None) -> str:
    """
    Return an HTML fragment for a result card. Useful if app wants to render
    results consistently via a helper instead of inline HTML.
    """
    tone_class = "result-spam" if is_spam else "result-safe"
    icon = "🚨" if is_spam else "✅"
    short_message = short_message or ("This message has been classified as spam. Please be cautious." if is_spam
                                     else "This message appears to be legitimate and safe.")
    html = f"""
    <div class="result-card {tone_class}">
        <div class="result-icon">{icon}</div>
        <div class="result-text">{'SPAM DETECTED' if is_spam else 'SAFE MESSAGE'}</div>
        <div class="result-message">{short_message}</div>
        <div class="confidence-score"><strong>Confidence Level: {confidence_pct:.1f}%</strong></div>
    </div>
    """
    return html


def render_info_cards(cards: Iterable[Dict[str, str]]):
    """
    Render a row of small info cards. Each card is a dict with keys:
    - icon (str), title (str), desc (str)
    Example:
        [{'icon': '🔍', 'title': 'Text Analysis', 'desc': '...'}, ...]
    """
    # This function writes directly to Streamlit
    cols = st.columns(len(list(cards)))
    for c, col in zip(cards, cols):
        with col:
            st.markdown(f"""
            <div class="info-card" style="text-align: center;">
                <div style="font-size: 1.6rem;">{c.get('icon','')}</div>
                <div class="info-title">{c.get('title','')}</div>
                <div class="info-desc">{c.get('desc','')}</div>
            </div>
            """, unsafe_allow_html=True)
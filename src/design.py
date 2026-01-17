import streamlit as st
import base64
from pathlib import Path
from PIL import Image
from typing import Optional, Iterable, Dict


def setup_page(
    title: str = "Email Spam Detector",
    logo_path: Optional[Path] = Path("image/logo.png"),
    initial_sidebar_state: str = "collapsed",
    animations: bool = True,
    compact: bool = False,
):
    """
    Configure the Streamlit page and inject polished CSS with advanced animations.

    - animations: enable/disable animated effects (honored via CSS classes and prefers-reduced-motion).
    - compact: reduce paddings/typography for tight layouts (mobile/embedded).
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

    st.markdown(get_css(logo_base64, animations=animations, compact=compact), unsafe_allow_html=True)


def get_css(logo_base64: str, animations: bool = True, compact: bool = False) -> str:
    """
    Return a modern, professional CSS theme with optional animations and responsive adjustments.
    It uses CSS variables to make theme tweaks easy.
    """
    # when animations disabled, keep minimal keyframes but still provide polished look
    anim_toggle = "on" if animations else "off"
    css = f"""
    <style>
    :root {{
        --bg-top: #061021;
        --bg-bottom: #07111a;
        --card-bg: rgba(255,255,255,0.03);
        --card-surface: rgba(255,255,255,0.02);
        --accent-primary: #5b7cff;
        --accent-success: #7bd389;
        --accent-danger: #ff6b6b;
        --muted: #9aa4b2;
        --glass-border: rgba(255,255,255,0.06);
        --radius: 14px;
        --max-width: 1100px;
    }}

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

    html, body, .stApp {{
        background: linear-gradient(180deg, var(--bg-top) 0%, var(--bg-bottom) 100%);
        color: #eaf0ff;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }}

    .main .block-container {{
        max-width: var(--max-width);
        padding-top: { '1rem' if compact else '2rem' };
        padding-bottom: { '1rem' if compact else '2rem' };
        padding-left: clamp(0.75rem, 3vw, 1.25rem);
        padding-right: clamp(0.75rem, 3vw, 1.25rem);
    }}

    /* Hide default Streamlit chrome for a cleaner canvas */
    #MainMenu, footer, header {{ visibility: hidden; height: 0; }}

    /* === Animations & Motion preferences === */
    @media (prefers-reduced-motion: reduce) {{
        .animate, .float, .stButton > button::after {{ animation: none !important; transition: none !important; }}
    }}

    /* subtle animated background gradient */
    @keyframes gradientShift {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}

    .stApp {{
        background-image: linear-gradient(120deg, rgba(91,124,255,0.04), rgba(123,211,137,0.03), rgba(255,111,111,0.02));
        background-size: 400% 400%;
        animation: {"gradientShift 18s ease infinite" if animations else "none"};
    }}

    /* entrance and fade animations used by content */
    @keyframes fadeInUp {{
        0% {{ opacity: 0; transform: translateY(10px) scale(0.995); }}
        100% {{ opacity: 1; transform: translateY(0) scale(1); }}
    }}
    .animate {{ animation: {"fadeInUp 520ms cubic-bezier(.2,.9,.2,1) both" if animations else "none"}; }}

    /* floating icon animation for gentle motion */
    @keyframes floatY {{
        0% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-6px); }}
        100% {{ transform: translateY(0px); }}
    }}
    .float {{ animation: {"floatY 4.5s ease-in-out infinite" if animations else "none"}; }}

    /* button ripple / glow on hover */
    .stButton > button {{
        position: relative;
        background: linear-gradient(90deg, var(--accent-primary), #9aa8ff);
        color: white;
        border: none;
        padding: 0.9rem 1rem;
        border-radius: 12px;
        font-weight: 700;
        letter-spacing: 0.5px;
        box-shadow: 0 8px 30px rgba(11,22,60,0.35);
        transition: transform 220ms cubic-bezier(.2,.9,.2,1), box-shadow 220ms;
        overflow: hidden;
    }}
    .stButton > button:hover {{
        transform: translateY(-4px) scale(1.01);
        box-shadow: 0 18px 50px rgba(11,22,60,0.45);
    }}
    /* soft glow when focused for accessibility */
    .stButton > button:focus {{
        outline: 3px solid rgba(91,124,255,0.14);
        outline-offset: 2px;
    }}
    /* small ripple effect using pseudo element */
    .stButton > button::after {{
        content: "";
        position: absolute;
        left: 50%;
        top: 50%;
        width: 0;
        height: 0;
        background: radial-gradient(circle, rgba(255,255,255,0.12) 0%, transparent 60%);
        transform: translate(-50%, -50%);
        border-radius: 50%;
        transition: width 520ms ease, height 520ms ease, opacity 520ms;
        opacity: 0;
        pointer-events: none;
        {"animation: none;" if not animations else ""}
    }}
    .stButton > button:active::after {{
        width: 300px;
        height: 300px;
        opacity: 1;
        transition: none;
    }}

    /* Card styles */
    .card {{
        background: linear-gradient(180deg, var(--card-bg), var(--card-surface));
        border: 1px solid var(--glass-border);
        border-radius: var(--radius);
        padding: 1.15rem;
        box-shadow: 0 12px 30px rgba(3,8,20,0.55);
        color: #eaf0ff;
    }}
    .card.meta {{
        display: flex;
        align-items: center;
        gap: 0.8rem;
    }}
    .card .icon {{
        font-size: 1.6rem;
        width: 48px;
        height: 48px;
        border-radius: 10px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(90deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
        border: 1px solid rgba(255,255,255,0.02);
    }}

    /* Result card specific */
    .result-card {{
        padding: 1.1rem;
        border-radius: 14px;
        position: relative;
        overflow: hidden;
        transition: transform 260ms ease, box-shadow 260ms ease;
    }}
    .result-card:hover {{
        transform: translateY(-6px) scale(1.01);
        box-shadow: 0 22px 60px rgba(3,8,20,0.6);
    }}
    .result-spam {{
        border-left: 4px solid var(--accent-danger);
    }}
    .result-safe {{
        border-left: 4px solid var(--accent-success);
    }}
    .result-icon {{
        font-size: clamp(1.8rem, 4vw, 2.8rem);
        display: block;
    }}
    .result-title {{
        font-weight: 800;
        font-size: clamp(1rem, 2.6vw, 1.4rem);
        margin-top: 0.45rem;
    }}
    .result-sub {{
        color: var(--muted);
        margin-top: 0.45rem;
    }}

    /* Animated accent bar (subtle) */
    .accent-bar {{
        height: 6px;
        width: 100%;
        border-radius: 8px;
        background: linear-gradient(90deg, rgba(91,124,255,0.95), rgba(123,211,137,0.9));
        box-shadow: 0 6px 18px rgba(91,124,255,0.08);
        margin-bottom: 0.9rem;
        {"animation: gradientShift 6s linear infinite;" if animations else ""}
    }}

    /* small info card */
    .info-card {{
        border-radius: 12px;
        padding: 0.9rem;
        background: linear-gradient(180deg, rgba(255,255,255,0.015), rgba(255,255,255,0.01));
        border: 1px solid rgba(255,255,255,0.02);
    }}
    .info-title {{ color: var(--accent-primary); font-weight: 700; }}
    .info-desc {{ color: var(--muted); font-size: 0.95rem; }}

    /* annotated message style */
    .annotated {{
        background: rgba(255,255,255,0.01);
        border-radius: 10px;
        padding: 0.9rem;
        line-height: 1.7;
        color: #eaf0ff;
    }}
    .annotated .spam {{
        background: rgba(255,90,90,0.12);
        color: #ffdfe0;
        padding: 2px 8px;
        border-radius: 999px;
        margin: 0 2px;
        display: inline-block;
    }}
    .annotated .ham {{
        background: rgba(75,199,139,0.12);
        color: #eafff0;
        padding: 2px 8px;
        border-radius: 999px;
        margin: 0 2px;
        display: inline-block;
    }}

    /* Responsive & accessibility tweaks */
    @media (max-width: 900px) {{
        .main .block-container {{ padding-left: 1rem; padding-right: 1rem; }}
    }}
    @media (max-width: 640px) {{
        .result-title {{ font-size: 1.05rem; }}
        .card {{ padding: 0.8rem; }}
        .stButton > button {{ padding: 0.8rem; }}
    }}

    /* focus visibility */
    button:focus, a:focus {{ outline: 3px solid rgba(91,124,255,0.12); outline-offset: 2px; }}

    </style>
    """
    if logo_base64:
        css += f'<link rel="icon" type="image/png" href="data:image/png;base64,{logo_base64}">'
    return css


def render_header(title: str = "🛡️ Email / SMS Spam Classifier", subtitle: str = "Protect your inbox from unwanted messages with AI-powered detection"):
    """
    Render a compact header using the current CSS. Animation class applied.
    """
    st.markdown(f"""
        <div class="card animate" style="text-align:center; margin-bottom:1rem;">
            <div class="accent-bar" aria-hidden="true"></div>
            <div style="display:flex; align-items:center; gap:1rem; justify-content:center; flex-direction:column;">
                <div style="font-weight:800; font-size:1.5rem; line-height:1.1;">{title}</div>
                <div style="color:var(--muted); margin-top:0.25rem;">{subtitle}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_result_card(is_spam: bool, confidence_pct: float, short_message: Optional[str] = None) -> str:
    """
    Return an HTML fragment for a stylized result card.
    Keeps the same content/semantics as previous implementations but with richer styling + subtle animation.
    """
    tone_class = "result-spam" if is_spam else "result-safe"
    icon = "🚨" if is_spam else "✅"
    title = "SPAM DETECTED" if is_spam else "SAFE MESSAGE"
    short_message = short_message or ("This message has been classified as spam. Please be cautious." if is_spam
                                     else "This message appears to be legitimate and safe.")
    html = f"""
    <div class="result-card card {tone_class} animate" role="status" aria-live="polite">
        <div style="display:flex; gap:1rem; align-items:center;">
            <div class="icon result-icon float" style="width:64px; height:64px; border-radius:12px; font-size:2rem; display:flex; align-items:center; justify-content:center;">{icon}</div>
            <div style="flex:1;">
                <div class="result-title">{title}</div>
                <div class="result-sub">{short_message}</div>
            </div>
            <div style="text-align:right;">
                <div style="font-weight:800; font-size:1.05rem; color:#fff;">{confidence_pct:.1f}%</div>
                <div style="color:var(--muted); font-size:0.85rem;">confidence</div>
            </div>
        </div>
    </div>
    """
    return html


def render_info_cards(cards: Iterable[Dict[str, str]]):
    """
    Render a row of small info cards. Each card is a dict with keys:
    - icon (str), title (str), desc (str)
    Cards receive a gentle entrance animation and floating icon.
    """
    cards_list = list(cards)
    if not cards_list:
        return
    cols = st.columns(len(cards_list))
    for idx, (c, col) in enumerate(zip(cards_list, cols)):
        with col:
            st.markdown(f"""
            <div class="info-card card animate" style="text-align:center;">
                <div style="display:flex; align-items:center; gap:0.6rem; justify-content:center; flex-direction:column;">
                    <div class="icon float" style="font-size:1.4rem;">{c.get('icon','')}</div>
                    <div class="info-title" style="margin-top:0.25rem;">{c.get('title','')}</div>
                    <div class="info-desc" style="margin-top:0.4rem;">{c.get('desc','')}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
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
    Return a modern, professional CSS theme, focusing on refined animations and card shapes.
    Only animation and card-shape related rules are changed compared to previous file.
    """
    css = f"""
    <style>
    :root {{
        --bg-top: #061021;
        --bg-bottom: #07111a;
        --card-bg: rgba(255,255,255,0.025);
        --card-surface: rgba(255,255,255,0.02);
        --accent-primary: #5b7cff;
        --accent-success: #7bd389;
        --accent-danger: #ff6b6b;
        --muted: #9aa4b2;
        --glass-border: rgba(255,255,255,0.04);
        --radius: 18px;
        --sharp-radius: 10px;
        --max-width: 1100px;
        --card-elevation: 22px;
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

    /* Respect reduced motion preference */
    @media (prefers-reduced-motion: reduce) {{
        .animate, .float, .card-tilt, .stButton > button::after {{ animation: none !important; transition: none !important; transform: none !important; }}
    }}

    /* --- Animation definitions (refined, subtle) --- */
    @keyframes subtleFloat {{
        0% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-6px); }}
        100% {{ transform: translateY(0px); }}
    }}

    @keyframes slowPulse {{
        0% {{ transform: scale(1); opacity: 1; }}
        50% {{ transform: scale(1.02); opacity: 0.98; }}
        100% {{ transform: scale(1); opacity: 1; }}
    }}

    @keyframes entrance {{
        0% {{ opacity: 0; transform: translateY(10px) scale(0.995); }}
        100% {{ opacity: 1; transform: translateY(0) scale(1); }}
    }}

    /* Apply animations only if enabled */
    .animate {{ animation: {"entrance 420ms cubic-bezier(.2,.9,.2,1) both" if animations else "none"}; }}
    .float {{ animation: {"subtleFloat 4.6s ease-in-out infinite" if animations else "none"}; }}
    .pulse {{ animation: {"slowPulse 6s ease-in-out infinite" if animations else "none"}; }}

    /* --- Card shapes & 3D tilt micro-interactions --- */
    .card {{
        background: linear-gradient(180deg, var(--card-bg), var(--card-surface));
        border-radius: var(--radius);
        padding: 1.15rem;
        color: #eaf0ff;
        box-shadow: 0 calc(var(--card-elevation) / 4) calc(var(--card-elevation)) rgba(2,8,20,0.55), inset 0 1px 0 rgba(255,255,255,0.02);
        position: relative;
        overflow: visible;
        transition: transform 320ms cubic-bezier(.2,.9,.2,1), box-shadow 320ms ease;
        will-change: transform;
    }}

    /* beveled / layered edge: pseudo element creates a subtle layered edge */
    .card::after {{
        content: "";
        position: absolute;
        left: 8px;
        right: 8px;
        bottom: -10px;
        height: 10px;
        border-radius: 10px;
        background: linear-gradient(90deg, rgba(0,0,0,0.12), rgba(0,0,0,0.04));
        filter: blur(6px);
        z-index: -1;
        opacity: 0.9;
    }}

    /* "tilt" container: small 3D tilt on hover for pointer devices */
    .card-tilt {{
        transform-style: preserve-3d;
        perspective: 900px;
    }}
    .card-tilt:hover {{
        transform: translateY(-6px) rotateX(3deg) rotateY(-1.2deg) scale(1.008);
        box-shadow: 0 28px 70px rgba(3,8,20,0.68);
    }}

    /* For cards that should look more geometric (sharp corner) */
    .card.sharp {{
        border-radius: var(--sharp-radius);
        clip-path: polygon(0 0, calc(100% - 16px) 0, 100% 16px, 100% 100%, 0% 100%);
    }}

    /* result card visual tweaks */
    .result-card {{
        padding: 1.1rem;
        border-radius: 16px;
        position: relative;
        overflow: visible;
    }}
    /* glossy top accent */
    .result-card .gloss::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 36%;
        background: linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.01));
        border-top-left-radius: 16px;
        border-top-right-radius: 16px;
        pointer-events: none;
        mix-blend-mode: overlay;
        z-index: 0;
    }}
    .result-card .content {{ position: relative; z-index: 1; }}

    .result-spam {{ border-left: 5px solid var(--accent-danger); }}
    .result-safe {{ border-left: 5px solid var(--accent-success); }}

    /* icon badge shape: rounded square with soft inner bevel */
    .result-icon-badge {{
        width: 64px;
        height: 64px;
        border-radius: 14px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.02), 0 8px 24px rgba(2,6,20,0.45);
        margin-right: 14px;
        flex-shrink: 0;
    }}

    /* accent bar refined */
    .accent-bar {{
        height: 6px;
        width: 100%;
        border-radius: 10px;
        background: linear-gradient(90deg, rgba(91,124,255,0.98), rgba(123,211,137,0.9));
        box-shadow: 0 6px 18px rgba(91,124,255,0.06), inset 0 -6px 18px rgba(0,0,0,0.12);
        margin-bottom: 0.9rem;
        {"animation: gradientShift 8s linear infinite;" if animations else ""}
    }}

    /* info card: slightly pill-like with inner highlight */
    .info-card {{
        border-radius: 12px;
        padding: 0.9rem;
        background: linear-gradient(180deg, rgba(255,255,255,0.012), rgba(255,255,255,0.008));
        border: 1px solid rgba(255,255,255,0.02);
        box-shadow: 0 8px 20px rgba(3,8,20,0.45);
    }}
    .info-card .icon {{
        width: 46px;
        height: 46px;
        border-radius: 12px;
        display:inline-flex;
        align-items:center;
        justify-content:center;
        background: linear-gradient(90deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.02);
    }}

    /* annotated message styling kept but with slightly rounder chips */
    .annotated {{
        background: rgba(255,255,255,0.008);
        border-radius: 12px;
        padding: 0.9rem;
        line-height: 1.7;
        color: #eaf0ff;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.01);
    }}
    .annotated .spam {{
        background: linear-gradient(90deg, rgba(255,90,90,0.14), rgba(255,70,70,0.06));
        color: #ffdfe0;
        padding: 4px 10px;
        border-radius: 999px;
        margin: 0 4px;
        display: inline-block;
        box-shadow: 0 6px 18px rgba(255,80,80,0.06);
    }}
    .annotated .ham {{
        background: linear-gradient(90deg, rgba(75,199,139,0.12), rgba(60,180,115,0.04));
        color: #eafff0;
        padding: 4px 10px;
        border-radius: 999px;
        margin: 0 4px;
        display: inline-block;
        box-shadow: 0 6px 18px rgba(60,180,115,0.04);
    }}

    /* Accessible focus outlines */
    button:focus, a:focus {{ outline: 3px solid rgba(91,124,255,0.14); outline-offset: 2px; }}

    /* Responsive tweaks: reduce 3D tilt / hover effects on small screens */
    @media (max-width: 900px) {{
        .card-tilt:hover {{ transform: translateY(-4px) rotateX(0) rotateY(0) scale(1.005); box-shadow: 0 18px 48px rgba(3,8,20,0.58); }}
    }}
    @media (max-width: 640px) {{
        .result-icon-badge {{ width: 52px; height: 52px; border-radius: 12px; }}
        .card {{ padding: 0.9rem; border-radius: 12px; }}
        .accent-bar {{ height: 5px; }}
    }}
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
        <div class="card card-tilt animate" style="text-align:center; margin-bottom:1rem;">
            <div class="accent-bar" aria-hidden="true"></div>
            <div style="display:flex; align-items:center; gap:1rem; justify-content:center; flex-direction:column;">
                <div style="font-weight:800; font-size:1.4rem; line-height:1.1;">{title}</div>
                <div style="color:var(--muted); margin-top:0.25rem;">{subtitle}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_result_card(is_spam: bool, confidence_pct: float, short_message: Optional[str] = None) -> str:
    """
    Return an HTML fragment for a stylized result card.
    Keeps the same content/semantics but uses refined shapes and animations.
    """
    tone_class = "result-spam" if is_spam else "result-safe"
    icon = "🚨" if is_spam else "✅"
    title = "SPAM DETECTED" if is_spam else "SAFE MESSAGE"
    short_message = short_message or ("This message has been classified as spam. Please be cautious." if is_spam
                                     else "This message appears to be legitimate and safe.")
    html = f"""
    <div class="result-card card card-tilt {tone_class} animate">
        <div class="gloss"></div>
        <div class="content" style="display:flex; gap:1rem; align-items:center;">
            <div class="result-icon-badge float" aria-hidden="true">{icon}</div>
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
    Cards receive a gentle entrance animation and refined shapes.
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
                    <div class="icon" style="font-size:1.2rem;">{c.get('icon','')}</div>
                    <div class="info-title" style="margin-top:0.25rem;">{c.get('title','')}</div>
                    <div class="info-desc" style="margin-top:0.4rem;">{c.get('desc','')}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
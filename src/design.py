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
    Return an updated CSS theme with stronger, attractive animated gradients and refined card shapes.
    The animations argument toggles animated rules; prefers-reduced-motion is honored.
    """
    anim_enabled = animations
    css = f"""
    <style>
    :root {{
        --bg-top: #041021;
        --bg-bottom: #061226;
        --card-bg: rgba(255,255,255,0.02);
        --card-surface: rgba(255,255,255,0.01);
        --accent-primary-1: #4f7bff;
        --accent-primary-2: #7bd3ff;
        --accent-success: #6be19b;
        --accent-danger: #ff7b7b;
        --muted: #9aa4b2;
        --glass-border: rgba(255,255,255,0.04);
        --radius: 18px;
        --max-width: 1120px;
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

    /* hide default streamlit chrome for cleaner canvas */
    #MainMenu, footer, header {{ visibility: hidden; height: 0; }}

    /* Respect reduced motion preference */
    @media (prefers-reduced-motion: reduce) {{
        .glow, .soft-gradient, .float, .animate, .tilt-hover, .shimmer {{ animation: none !important; transition: none !important; transform: none !important; }}
    }}

    /* Animated gradient backgrounds for cards - subtle and professional */
    @keyframes gradientFlowPrimary {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}
    @keyframes gradientFlowAccent {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 75% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}

    /* entrance animation */
    @keyframes entrance {{
        0% {{ opacity: 0; transform: translateY(8px) scale(0.995); }}
        100% {{ opacity: 1; transform: translateY(0) scale(1); }}
    }}

    .animate {{ animation: {"entrance 420ms cubic-bezier(.2,.9,.2,1) both" if anim_enabled else "none"}; }}
    .float {{ animation: {"translateY 4.8s ease-in-out infinite" if anim_enabled else "none"}; }}

    /* Card base */
    .card {{
        border-radius: var(--radius);
        padding: 1.15rem;
        color: #eaf0ff;
        background: linear-gradient(180deg, var(--card-bg), var(--card-surface));
        border: 1px solid var(--glass-border);
        box-shadow: 0 18px 48px rgba(2,8,20,0.56), inset 0 1px 0 rgba(255,255,255,0.02);
        transition: transform 300ms cubic-bezier(.2,.9,.2,1), box-shadow 300ms ease;
        overflow: visible;
    }}

    /* tilt hover for pointer devices, disabled on small screens in responsive rules */
    .tilt-hover {{ will-change: transform; transform-style: preserve-3d; perspective: 800px; }}
    .tilt-hover:hover {{ transform: translateY(-6px) rotateX(2.2deg) rotateY(-0.8deg) scale(1.006); box-shadow: 0 32px 80px rgba(2,8,20,0.68); }}

    /* layered shadow (beveled) */
    .card::after {{
        content: "";
        position: absolute;
        left: 10px;
        right: 10px;
        bottom: -12px;
        height: 12px;
        border-radius: 12px;
        background: linear-gradient(90deg, rgba(0,0,0,0.20), rgba(0,0,0,0.06));
        filter: blur(6px);
        z-index: -1;
        opacity: 0.95;
    }}

    /* soft gradient border using background-clip technique */
    .card.gradient-border {{
        position: relative;
        padding: calc(1.15rem - 1px);
    }}
    .card.gradient-border::before {{
        content: "";
        position: absolute;
        inset: 0;
        border-radius: calc(var(--radius) + 2px);
        padding: 2px;
        background: linear-gradient(90deg, var(--accent-primary-1), var(--accent-primary-2), var(--accent-success));
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
        z-index: -2;
        opacity: 0.95;
        {"animation: gradientFlowPrimary 8s ease infinite;" if anim_enabled else ""}
    }}

    /* result card: apply attractive soft-gradient background and glossy top */
    .result-card {{
        border-radius: 16px;
        position: relative;
        overflow: visible;
        padding: 1.15rem;
        background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
    }}
    .result-card.soft-gradient {{
        background: linear-gradient(90deg, rgba(91,124,255,0.06), rgba(123,211,137,0.04));
        {"background-size: 300% 300%;" if anim_enabled else ""}
        {"animation: gradientFlowAccent 10s ease infinite;" if anim_enabled else ""}
        border: 1px solid rgba(255,255,255,0.02);
    }}
    .result-card .gloss::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 34%;
        background: linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.01));
        border-top-left-radius: 16px;
        border-top-right-radius: 16px;
        pointer-events: none;
        mix-blend-mode: overlay;
        z-index: 0;
    }}
    .result-spam {{ border-left: 5px solid var(--accent-danger); }}
    .result-safe {{ border-left: 5px solid var(--accent-success); }}

    /* icon badge with gradient glow */
    .result-icon-badge {{
        width: 68px;
        height: 68px;
        border-radius: 14px;
        display:inline-flex;
        align-items:center;
        justify-content:center;
        background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.02), 0 12px 34px rgba(2,8,20,0.45);
        margin-right: 14px;
        flex-shrink: 0;
        position: relative;
    }}
    .result-icon-badge::after {{
        content: "";
        position: absolute;
        inset: -6px;
        border-radius: 16px;
        background: radial-gradient(circle at 20% 20%, rgba(91,124,255,0.12), transparent 18%),
                    radial-gradient(circle at 80% 80%, rgba(123,211,137,0.08), transparent 18%);
        z-index: -1;
        filter: blur(8px);
        opacity: 0.95;
        {"animation: gradientFlowPrimary 10s linear infinite;" if anim_enabled else ""}
    }}

    /* info-card: pill-like with animated accent strip */
    .info-card {{
        border-radius: 14px;
        padding: 0.95rem;
        background: linear-gradient(180deg, rgba(255,255,255,0.01), rgba(255,255,255,0.008));
        border: 1px solid rgba(255,255,255,0.02);
        box-shadow: 0 10px 28px rgba(3,8,20,0.45);
        position: relative;
    }}
    .info-card .accent-strip {{
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 6px;
        border-top-left-radius: 14px;
        border-bottom-left-radius: 14px;
        background: linear-gradient(180deg, var(--accent-primary-1), var(--accent-primary-2));
        {"animation: gradientFlowPrimary 7s linear infinite;" if anim_enabled else ""}
    }}

    /* small shimmer for headings (very subtle) */
    @keyframes shimmer {{
        0% {{ background-position: -200% 0; }}
        100% {{ background-position: 200% 0; }}
    }}
    .shimmer {{
        background: linear-gradient(90deg, rgba(255,255,255,0.04) 0%, rgba(255,255,255,0.08) 50%, rgba(255,255,255,0.04) 100%);
        background-size: 200% 100%;
        {"animation: shimmer 2400ms linear infinite" if anim_enabled else ""}
        -webkit-background-clip: text;
        color: transparent;
    }}

    /* annotated chips (rounded with gradient hints) */
    .annotated .spam {{
        background: linear-gradient(90deg, rgba(255,90,90,0.16), rgba(255,70,70,0.06));
        color: #ffdfe0;
        padding: 6px 12px;
        border-radius: 999px;
        margin: 0 6px;
        display: inline-block;
        box-shadow: 0 8px 30px rgba(255,80,80,0.06);
    }}
    .annotated .ham {{
        background: linear-gradient(90deg, rgba(75,199,139,0.14), rgba(60,180,115,0.04));
        color: #eafff0;
        padding: 6px 12px;
        border-radius: 999px;
        margin: 0 6px;
        display: inline-block;
        box-shadow: 0 8px 30px rgba(60,180,115,0.04);
    }}

    /* Focus outlines for accessibility */
    button:focus, a:focus {{ outline: 3px solid rgba(91,124,255,0.12); outline-offset: 2px; }}

    /* Responsive reductions for hover/tilt on small screens */
    @media (max-width: 900px) {{
        .tilt-hover:hover {{ transform: translateY(-4px) rotateX(0) rotateY(0) scale(1.004); box-shadow: 0 20px 48px rgba(3,8,20,0.58); }}
    }}
    @media (max-width: 640px) {{
        .result-icon-badge {{ width: 56px; height: 56px; border-radius: 12px; }}
        .card {{ padding: 0.9rem; border-radius: 12px; }}
    }}
    </style>
    """
    if logo_base64:
        css += f'<link rel="icon" type="image/png" href="data:image/png;base64,{logo_base64}">'
    return css


def render_header(title: str = "🛡️ Email / SMS Spam Classifier", subtitle: str = "Protect your inbox from unwanted messages with AI-powered detection"):
    """
    Render the header using the improved card appearance and animations.
    """
    st.markdown(f"""
        <div class="card tilt-hover animate" style="text-align:center; margin-bottom:1rem;">
            <div class="accent-bar" style="height:8px; width:100%; border-radius:10px; margin-bottom:12px; background: linear-gradient(90deg, var(--accent-primary-1), var(--accent-primary-2));"></div>
            <div style="display:flex; align-items:center; gap:1rem; justify-content:center; flex-direction:column;">
                <div style="font-weight:800; font-size:1.35rem; line-height:1.05;" class="shimmer">{title}</div>
                <div style="color:var(--muted); margin-top:0.25rem;">{subtitle}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_result_card(is_spam: bool, confidence_pct: float, short_message: Optional[str] = None) -> str:
    """
    Return an HTML fragment for a stylized result card using animated gradients and refined shapes.
    """
    tone_class = "result-spam" if is_spam else "result-safe"
    icon = "🚨" if is_spam else "✅"
    title = "SPAM DETECTED" if is_spam else "SAFE MESSAGE"
    short_message = short_message or ("This message has been classified as spam. Please be cautious." if is_spam
                                     else "This message appears to be legitimate and safe.")
    html = f"""
    <div class="result-card soft-gradient card tilt-hover {tone_class} animate">
        <div class="gloss"></div>
        <div class="content" style="display:flex; gap:1rem; align-items:center;">
            <div class="result-icon-badge" aria-hidden="true">{icon}</div>
            <div style="flex:1;">
                <div style="font-weight:800; font-size:1.05rem;">{title}</div>
                <div style="color:var(--muted); margin-top:0.35rem;">{short_message}</div>
            </div>
            <div style="text-align:right;">
                <div style="font-weight:900; font-size:1.05rem; color:#fff;">{confidence_pct:.1f}%</div>
                <div style="color:var(--muted); font-size:0.85rem;">confidence</div>
            </div>
        </div>
    </div>
    """
    return html


def render_info_cards(cards: Iterable[Dict[str, str]]):
    """
    Render a row of animated gradient info cards. Each card has:
    - icon (str), title (str), desc (str)
    """
    cards_list = list(cards)
    if not cards_list:
        return
    cols = st.columns(len(cards_list))
    for idx, (c, col) in enumerate(zip(cards_list, cols)):
        with col:
            st.markdown(f"""
            <div class="info-card card tilt-hover animate" style="text-align:center; position:relative;">
                <div class="accent-strip" aria-hidden="true"></div>
                <div style="display:flex; align-items:center; gap:0.6rem; justify-content:center; flex-direction:column;">
                    <div class="icon" style="font-size:1.2rem;">{c.get('icon','')}</div>
                    <div style="font-weight:700; margin-top:0.25rem;">{c.get('title','')}</div>
                    <div style="color:var(--muted); margin-top:0.35rem; font-size:0.95rem;">{c.get('desc','')}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
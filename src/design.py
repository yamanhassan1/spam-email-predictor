import streamlit as st
import base64
from pathlib import Path
from typing import Optional, Iterable, Dict


def setup_page(
    title: str = "Email Spam Detector",
    logo_path: Optional[Path] = (
    Path(__file__).parent.parent / "image" / "logo.png"
    ),
    initial_sidebar_state: str = "collapsed",
    animations: bool = True,
    compact: bool = False,
):
    """
    Configure the Streamlit page with premium design and advanced animations.
    """
    logo_base64 = ""
    page_icon = "🛡️"

    if logo_path and logo_path.exists():
        try:
            with open(logo_path, "rb") as f:
                logo_base64 = base64.b64encode(f.read()).decode()
            try:
                from PIL import Image
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
    Premium CSS with modern glassmorphism, gradients, and sophisticated animations.
    """
    anim_enabled = animations
    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    :root {{
        --bg-primary: #0a0e27;
        --bg-secondary: #0f1433;
        --bg-tertiary: #161b42;
        
        --glass-bg: rgba(255, 255, 255, 0.04);
        --glass-border: rgba(255, 255, 255, 0.1);
        --glass-highlight: rgba(255, 255, 255, 0.15);
        
        --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --gradient-success: linear-gradient(135deg, #10b981 0%, #059669 100%);
        --gradient-danger: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        --gradient-info: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        
        --blue-500: #3b82f6;
        --blue-400: #60a5fa;
        --purple-500: #8b5cf6;
        --purple-400: #a78bfa;
        --cyan-500: #06b6d4;
        --green-500: #10b981;
        --green-400: #34d399;
        --red-500: #ef4444;
        --red-400: #f87171;
        
        --text-primary: #f8fafc;
        --text-secondary: #cbd5e1;
        --text-muted: #94a3b8;
        
        --shadow-glow: 0 0 40px rgba(59, 130, 246, 0.3);
        --shadow-xl: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    }}

    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}

    html, body, .stApp {{
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0a0e27 100%);
        background-attachment: fixed;
        color: var(--text-primary);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        overflow-x: hidden;
    }}

    /* Animated mesh gradient background */
    .stApp::before {{
        content: "";
        position: fixed;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: 
            radial-gradient(circle at 20% 50%, rgba(102, 126, 234, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(139, 92, 246, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 40% 20%, rgba(59, 130, 246, 0.12) 0%, transparent 50%),
            radial-gradient(circle at 70% 40%, rgba(16, 185, 129, 0.08) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
        {"animation: meshFloat 30s ease-in-out infinite;" if anim_enabled else ""}
    }}

    @keyframes meshFloat {{
        0%, 100% {{ transform: translate(0, 0) rotate(0deg); }}
        33% {{ transform: translate(30px, -30px) rotate(5deg); }}
        66% {{ transform: translate(-20px, 20px) rotate(-5deg); }}
    }}

    /* Floating particles effect */
    .stApp::after {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(2px 2px at 20% 30%, rgba(255, 255, 255, 0.15), transparent),
            radial-gradient(2px 2px at 60% 70%, rgba(255, 255, 255, 0.1), transparent),
            radial-gradient(1px 1px at 50% 50%, rgba(255, 255, 255, 0.1), transparent),
            radial-gradient(1px 1px at 80% 10%, rgba(255, 255, 255, 0.15), transparent),
            radial-gradient(2px 2px at 90% 60%, rgba(255, 255, 255, 0.1), transparent),
            radial-gradient(1px 1px at 33% 80%, rgba(255, 255, 255, 0.1), transparent);
        background-size: 200% 200%;
        background-position: 0% 0%;
        pointer-events: none;
        z-index: 1;
        opacity: 0.4;
        {"animation: particleShift 60s linear infinite;" if anim_enabled else ""}
    }}

    @keyframes particleShift {{
        0% {{ background-position: 0% 0%; }}
        100% {{ background-position: 100% 100%; }}
    }}

    .main .block-container {{
        max-width: 1400px;
        padding: {'2rem' if compact else '3.5rem'} clamp(1rem, 5vw, 3rem);
        position: relative;
        z-index: 2;
    }}

    #MainMenu, footer, header {{
        visibility: hidden;
        height: 0;
    }}

    /* Premium glass card with depth */
    .card {{
        background: linear-gradient(135deg, 
            rgba(255, 255, 255, 0.05) 0%, 
            rgba(255, 255, 255, 0.02) 100%);
        backdrop-filter: blur(30px) saturate(150%);
        -webkit-backdrop-filter: blur(30px) saturate(150%);
        border: 1px solid var(--glass-border);
        border-radius: 24px;
        padding: 2rem;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1),
            0 0 0 1px rgba(255, 255, 255, 0.05);
        position: relative;
        overflow: hidden;
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    }}

    /* Glossy overlay effect */
    .card::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 50%;
        background: linear-gradient(180deg, 
            rgba(255, 255, 255, 0.12) 0%, 
            transparent 100%);
        pointer-events: none;
        z-index: 1;
        border-radius: 24px 24px 0 0;
    }}

    /* Animated shimmer on hover */
    .card::after {{
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            110deg,
            transparent 25%,
            rgba(255, 255, 255, 0.15) 45%,
            rgba(255, 255, 255, 0.2) 50%,
            rgba(255, 255, 255, 0.15) 55%,
            transparent 75%
        );
        transform: translateX(-100%) translateY(-100%) rotate(30deg);
        pointer-events: none;
        z-index: 3;
        transition: transform 0.8s cubic-bezier(0.4, 0, 0.2, 1);
    }}

    .card:hover {{
        transform: translateY(-6px) scale(1.01);
        box-shadow: 
            0 20px 60px rgba(0, 0, 0, 0.4),
            0 0 60px rgba(59, 130, 246, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.15);
        border-color: var(--glass-highlight);
    }}

    .card:hover::after {{
        transform: translateX(100%) translateY(100%) rotate(30deg);
    }}

    /* Gradient border animation */
    .gradient-border {{
        position: relative;
        border: none;
    }}

    .gradient-border::before {{
        content: "";
        position: absolute;
        inset: -2px;
        border-radius: 24px;
        padding: 2px;
        background: linear-gradient(135deg, 
            var(--blue-400),
            var(--purple-400),
            var(--cyan-500),
            var(--blue-400)
        );
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
        {"background-size: 400% 400%;" if anim_enabled else ""}
        {"animation: gradientFlow 8s ease infinite;" if anim_enabled else ""}
        z-index: -1;
    }}

    @keyframes gradientFlow {{
        0%, 100% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
    }}

    /* Slide in animation */
    .animate {{
        {"animation: slideInUp 0.7s cubic-bezier(0.16, 1, 0.3, 1) backwards;" if anim_enabled else ""}
    }}

    @keyframes slideInUp {{
        from {{
            opacity: 0;
            transform: translateY(40px) scale(0.98);
        }}
        to {{
            opacity: 1;
            transform: translateY(0) scale(1);
        }}
    }}

    .animate:nth-child(1) {{ animation-delay: 0s; }}
    .animate:nth-child(2) {{ animation-delay: 0.1s; }}
    .animate:nth-child(3) {{ animation-delay: 0.2s; }}
    .animate:nth-child(4) {{ animation-delay: 0.3s; }}
    .animate:nth-child(5) {{ animation-delay: 0.4s; }}

    /* Premium result card with glow */
    .result-card {{
        border-radius: 28px;
        padding: 2.5rem;
        position: relative;
        background: linear-gradient(135deg, 
            rgba(255, 255, 255, 0.06),
            rgba(255, 255, 255, 0.02)
        );
        backdrop-filter: blur(40px) saturate(180%);
        border: 2px solid var(--glass-border);
        box-shadow: 
            0 30px 90px rgba(0, 0, 0, 0.5),
            inset 0 2px 0 rgba(255, 255, 255, 0.15);
    }}

    .result-card::after {{
        content: "";
        position: absolute;
        inset: -30px;
        border-radius: 28px;
        background: inherit;
        filter: blur(40px);
        opacity: 0;
        z-index: -1;
        transition: opacity 0.5s;
    }}

    .result-card:hover::after {{
        opacity: 0.7;
    }}

    .result-spam {{
        border-color: var(--red-500);
        background: linear-gradient(135deg, 
            rgba(239, 68, 68, 0.1),
            rgba(220, 38, 38, 0.05)
        );
    }}

    .result-spam::after {{
        background: radial-gradient(circle, 
            rgba(239, 68, 68, 0.4),
            transparent 70%
        );
    }}

    .result-safe {{
        border-color: var(--green-500);
        background: linear-gradient(135deg, 
            rgba(16, 185, 129, 0.1),
            rgba(5, 150, 105, 0.05)
        );
    }}

    .result-safe::after {{
        background: radial-gradient(circle, 
            rgba(16, 185, 129, 0.4),
            transparent 70%
        );
    }}

    /* 3D Icon Badge */
    .result-icon-badge {{
        width: 90px;
        height: 90px;
        border-radius: 20px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, 
            rgba(255, 255, 255, 0.15),
            rgba(255, 255, 255, 0.05)
        );
        backdrop-filter: blur(20px);
        box-shadow: 
            0 10px 40px rgba(0, 0, 0, 0.3),
            inset 0 2px 0 rgba(255, 255, 255, 0.3),
            inset 0 -2px 0 rgba(0, 0, 0, 0.2);
        font-size: 3rem;
        position: relative;
        flex-shrink: 0;
        {"animation: float 4s ease-in-out infinite;" if anim_enabled else ""}
        transform-style: preserve-3d;
    }}

    @keyframes float {{
        0%, 100% {{ transform: translateY(0px) rotateX(0deg) rotateY(0deg); }}
        25% {{ transform: translateY(-10px) rotateX(5deg) rotateY(-5deg); }}
        75% {{ transform: translateY(-5px) rotateX(-5deg) rotateY(5deg); }}
    }}

    .result-icon-badge::before {{
        content: "";
        position: absolute;
        inset: -3px;
        border-radius: 20px;
        background: linear-gradient(135deg,
            var(--blue-400),
            var(--purple-400)
        );
        z-index: -1;
        opacity: 0.6;
        filter: blur(20px);
        {"animation: pulse 3s ease-in-out infinite;" if anim_enabled else ""}
    }}

    @keyframes pulse {{
        0%, 100% {{ opacity: 0.6; transform: scale(1); }}
        50% {{ opacity: 0.9; transform: scale(1.1); }}
    }}

    /* Info card with accent strip */
    .info-card {{
        border-radius: 20px;
        padding: 1.75rem;
        background: linear-gradient(135deg,
            rgba(255, 255, 255, 0.05),
            rgba(255, 255, 255, 0.02)
        );
        backdrop-filter: blur(25px);
        border: 1px solid var(--glass-border);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
        position: relative;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        overflow: hidden;
    }}

    .info-card::before {{
        content: "";
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 4px;
        background: linear-gradient(180deg,
            var(--blue-400),
            var(--purple-400),
            var(--cyan-500)
        );
        {"background-size: 100% 400%;" if anim_enabled else ""}
        {"animation: gradientFlow 6s ease infinite;" if anim_enabled else ""}
    }}

    .info-card:hover {{
        transform: translateY(-6px) scale(1.02);
        box-shadow: 0 16px 48px rgba(0, 0, 0, 0.35);
        border-color: var(--glass-highlight);
    }}

    /* Enhanced chip badges */
    .annotated .spam {{
        background: linear-gradient(135deg,
            rgba(239, 68, 68, 0.25),
            rgba(220, 38, 38, 0.15)
        );
        color: #fecdd3;
        padding: 10px 18px;
        border-radius: 12px;
        margin: 0 6px 6px 0;
        display: inline-block;
        font-weight: 700;
        font-size: 0.95rem;
        border: 1px solid rgba(239, 68, 68, 0.4);
        box-shadow: 
            0 4px 12px rgba(239, 68, 68, 0.25),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }}

    .annotated .spam:hover {{
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 8px 20px rgba(239, 68, 68, 0.35);
    }}

    .annotated .ham {{
        background: linear-gradient(135deg,
            rgba(16, 185, 129, 0.25),
            rgba(5, 150, 105, 0.15)
        );
        color: #d1fae5;
        padding: 10px 18px;
        border-radius: 12px;
        margin: 0 6px 6px 0;
        display: inline-block;
        font-weight: 700;
        font-size: 0.95rem;
        border: 1px solid rgba(16, 185, 129, 0.4);
        box-shadow: 
            0 4px 12px rgba(16, 185, 129, 0.25),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }}

    .annotated .ham:hover {{
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 8px 20px rgba(16, 185, 129, 0.35);
    }}

    /* Streamlit component overrides */
    .stTextArea textarea {{
        background: rgba(255, 255, 255, 0.04) !important;
        border: 2px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        color: #f8fafc !important;
        font-size: 1rem !important;
        padding: 1.25rem !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(10px) !important;
    }}

    .stTextArea textarea:focus {{
        border-color: var(--blue-400) !important;
        box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.15) !important;
        background: rgba(255, 255, 255, 0.06) !important;
    }}

    .stButton > button {{
        background: linear-gradient(135deg, var(--blue-500), var(--purple-500)) !important;
        color: white !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 1rem 2.5rem !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        letter-spacing: 0.02em !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 
            0 10px 30px rgba(59, 130, 246, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
        position: relative !important;
        overflow: hidden !important;
    }}

    .stButton > button::before {{
        content: "";
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        transition: left 0.5s;
    }}

    .stButton > button:hover::before {{
        left: 100%;
    }}

    .stButton > button:hover {{
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 15px 45px rgba(59, 130, 246, 0.5) !important;
    }}

    .stButton > button:active {{
        transform: translateY(-1px) scale(0.98) !important;
    }}

    /* Typography improvements */
    h1, h2, h3, h4, h5, h6 {{
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1.2;
        background: linear-gradient(135deg, #f8fafc, #cbd5e1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}

    p {{
        line-height: 1.7;
        color: var(--text-secondary);
    }}

    /* Scrollbar styling */
    ::-webkit-scrollbar {{
        width: 10px;
        height: 10px;
    }}

    ::-webkit-scrollbar-track {{
        background: rgba(255, 255, 255, 0.02);
        border-radius: 10px;
    }}

    ::-webkit-scrollbar-thumb {{
        background: linear-gradient(135deg, var(--blue-500), var(--purple-500));
        border-radius: 10px;
        border: 2px solid transparent;
        background-clip: padding-box;
    }}

    ::-webkit-scrollbar-thumb:hover {{
        background: linear-gradient(135deg, var(--blue-400), var(--purple-400));
        background-clip: padding-box;
    }}

    /* Focus states */
    button:focus, 
    a:focus,
    input:focus,
    textarea:focus {{
        outline: 2px solid var(--blue-400) !important;
        outline-offset: 3px !important;
    }}

    /* Responsive design */
    @media (max-width: 768px) {{
        .result-icon-badge {{
            width: 70px;
            height: 70px;
            font-size: 2.25rem;
        }}
        
        .card {{
            padding: 1.5rem;
            border-radius: 20px;
        }}
        
        .result-card {{
            padding: 2rem;
        }}
    }}

    @media (max-width: 480px) {{
        .result-icon-badge {{
            width: 60px;
            height: 60px;
            font-size: 2rem;
        }}
        
        .card {{
            padding: 1.25rem;
            border-radius: 16px;
        }}
    }}

    /* Reduced motion for accessibility */
    @media (prefers-reduced-motion: reduce) {{
        *,
        *::before,
        *::after {{
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }}
    }}
    </style>
    """
    if logo_base64:
        css += f'<link rel="icon" type="image/png" href="data:image/png;base64,{logo_base64}">'
    return css


def render_header(title, subtitle):
    """
    Render premium header with gradient accents and modern styling.
    """
    st.markdown(f"""
        <div class="card gradient-border animate" style="text-align: center; padding: 3rem 2rem; margin-bottom: 3rem; position: relative; overflow: visible;">
            <!-- Decorative glow circles -->
            <div style="position: absolute; top: -100px; right: -100px; width: 300px; height: 300px; background: radial-gradient(circle, rgba(139, 92, 246, 0.2), transparent 70%); filter: blur(60px); pointer-events: none;"></div>
            <div style="position: absolute; bottom: -100px; left: -100px; width: 300px; height: 300px; background: radial-gradient(circle, rgba(59, 130, 246, 0.2), transparent 70%); filter: blur(60px); pointer-events: none;"></div>
            
            <div style="font-size: 5rem; margin-bottom: 1.5rem; filter: drop-shadow(0 10px 30px rgba(59, 130, 246, 0.4)); animation: float 4s ease-in-out infinite;">🛡️</div>
            <h1 style="font-size: 3.5rem; font-weight: 900; margin-bottom: 1rem; letter-spacing: -0.04em; background: linear-gradient(135deg, #667eea, #764ba2, #f093fb); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
                {title}
            </h1>
            <div style="height: 4px; width: 120px; margin: 0 auto 1.5rem; background: linear-gradient(90deg, var(--blue-400), var(--purple-400), var(--cyan-500)); border-radius: 999px; box-shadow: 0 4px 20px rgba(102, 126, 234, 0.5);"></div>
            <p style="color: #cbd5e1; font-size: 1.25rem; line-height: 1.8; max-width: 700px; margin: 0 auto;">
                {subtitle}
            </p>
        </div>
    """, unsafe_allow_html=True)


def render_result_card(is_spam: bool, confidence_pct: float, short_message: Optional[str] = None) -> str:
    """
    Generate premium result card with modern styling.
    """
    tone_class = "result-spam" if is_spam else "result-safe"
    icon = "🚨" if is_spam else "✅"
    title = "SPAM DETECTED" if is_spam else "SAFE MESSAGE"
    short_message = short_message or (
        "This message has been classified as spam. Exercise caution before proceeding." if is_spam
        else "This message appears to be legitimate and safe to read."
    )
    
    html = f"""
    <div class="result-card {tone_class} animate" style="margin: 2.5rem 0;">
        <div style="display: flex; gap: 2rem; align-items: center; flex-wrap: wrap;">
            <div class="result-icon-badge" aria-label="Status icon">
                {icon}
            </div>
            <div style="flex: 1; min-width: 220px;">
                <h2 style="font-weight: 900; font-size: 1.75rem; margin: 0 0 0.75rem 0; letter-spacing: -0.03em;">
                    {title}
                </h2>
                <p style="color: var(--text-secondary); margin: 0; line-height: 1.7; font-size: 1.05rem;">
                    {short_message}
                </p>
            </div>
            <div style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.04)); border-radius: 20px; backdrop-filter: blur(20px); min-width: 140px; box-shadow: inset 0 2px 0 rgba(255, 255, 255, 0.1);">
                <div style="font-weight: 900; font-size: 2.75rem; color: var(--text-primary); line-height: 1; background: linear-gradient(135deg, #f8fafc, #cbd5e1); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
                    {confidence_pct:.1f}%
                </div>
                <div style="color: var(--text-muted); font-size: 0.95rem; margin-top: 0.5rem; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 600;">
                Confidence
                </div>
            </div>
        </div>
    </div>
    """
    return html


def render_info_cards(cards: Iterable[Dict[str, str]]):
    """
    Render premium info cards with gradient accents and hover effects.
    """
    cards_list = list(cards)
    if not cards_list:
        return
    
    cols = st.columns(len(cards_list))
    for idx, (card_data, col) in enumerate(zip(cards_list, cols)):
        with col:
            st.markdown(f"""
            <div class="info-card card animate" style="text-align: center; height: 100%; animation-delay: {idx * 0.1}s;">
                <div style="display: flex; flex-direction: column; align-items: center; gap: 1.25rem; padding: 0.5rem;">
                    <div style="width: 70px; height: 70px; border-radius: 16px; background: linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(139, 92, 246, 0.1)); display: flex; align-items: center; justify-content: center; font-size: 2.5rem; box-shadow: 0 8px 24px rgba(59, 130, 246, 0.2), inset 0 2px 0 rgba(255, 255, 255, 0.1);">
                        {card_data.get('icon', '')}
                    </div>
                    <h3 style="font-weight: 800; font-size: 1.2rem; margin: 0; color: var(--text-primary); letter-spacing: -0.02em;">
                        {card_data.get('title', '')}
                    </h3>
                    <p style="color: var(--text-secondary); margin: 0; font-size: 1rem; line-height: 1.6;">
                        {card_data.get('desc', '')}
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
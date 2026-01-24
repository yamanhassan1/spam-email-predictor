import streamlit as st
import base64
from pathlib import Path
from typing import Optional, Iterable, Dict
import time


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
    Premium CSS with glassmorphism, advanced gradients, and sophisticated animations.
    """
    anim_enabled = animations
    css = f"""
    <style>
    :root {{
        --bg-dark: #0a0e27;
        --bg-mid: #0f1433;
        --bg-light: #161b42;
        --glass-bg: rgba(255, 255, 255, 0.03);
        --glass-border: rgba(255, 255, 255, 0.08);
        --glass-highlight: rgba(255, 255, 255, 0.12);
        
        --primary-blue: #3b82f6;
        --primary-cyan: #06b6d4;
        --primary-purple: #8b5cf6;
        --success-green: #10b981;
        --success-emerald: #34d399;
        --danger-red: #ef4444;
        --danger-rose: #fb7185;
        
        --text-primary: #f8fafc;
        --text-secondary: #cbd5e1;
        --text-muted: #94a3b8;
        
        --radius-sm: 12px;
        --radius-md: 16px;
        --radius-lg: 20px;
        --radius-xl: 24px;
        
        --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.1);
        --shadow-md: 0 8px 32px rgba(0, 0, 0, 0.2);
        --shadow-lg: 0 16px 48px rgba(0, 0, 0, 0.3);
        --shadow-xl: 0 24px 64px rgba(0, 0, 0, 0.4);
        
        --max-width: 1200px;
    }}

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}

    html, body, .stApp {{
        background: radial-gradient(ellipse at top, var(--bg-mid), var(--bg-dark)),
                    radial-gradient(ellipse at bottom, var(--bg-light), var(--bg-dark));
        background-attachment: fixed;
        color: var(--text-primary);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        overflow-x: hidden;
    }}

    /* Animated background particles */
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 20% 30%, rgba(59, 130, 246, 0.08) 0%, transparent 50%),
            radial-gradient(circle at 80% 70%, rgba(139, 92, 246, 0.06) 0%, transparent 50%),
            radial-gradient(circle at 40% 80%, rgba(16, 185, 129, 0.05) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
        {"animation: particleFloat 20s ease-in-out infinite;" if anim_enabled else ""}
    }}

    @keyframes particleFloat {{
        0%, 100% {{ transform: translate(0, 0) scale(1); }}
        33% {{ transform: translate(30px, -30px) scale(1.1); }}
        66% {{ transform: translate(-20px, 20px) scale(0.9); }}
    }}

    .main .block-container {{
        max-width: var(--max-width);
        padding-top: {'2rem' if compact else '3rem'};
        padding-bottom: {'2rem' if compact else '3rem'};
        padding-left: clamp(1rem, 4vw, 2rem);
        padding-right: clamp(1rem, 4vw, 2rem);
        position: relative;
        z-index: 1;
    }}

    #MainMenu, footer, header {{
        visibility: hidden;
        height: 0;
    }}

    @media (prefers-reduced-motion: reduce) {{
        * {{
            animation: none !important;
            transition: none !important;
        }}
    }}

    /* Advanced gradient animations */
    @keyframes gradientShift {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}

    @keyframes glowPulse {{
        0%, 100% {{ opacity: 0.5; filter: blur(20px); }}
        50% {{ opacity: 0.8; filter: blur(25px); }}
    }}

    @keyframes slideInUp {{
        from {{
            opacity: 0;
            transform: translateY(30px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    @keyframes shimmerSlide {{
        0% {{ transform: translateX(-100%); }}
        100% {{ transform: translateX(100%); }}
    }}

    @keyframes float {{
        0%, 100% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-10px); }}
    }}

    /* Glass card base */
    .card {{
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        box-shadow: var(--shadow-lg),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }}

    /* Glossy overlay */
    .card::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 40%;
        background: linear-gradient(180deg, 
            rgba(255, 255, 255, 0.1) 0%, 
            rgba(255, 255, 255, 0.05) 50%,
            transparent 100%);
        pointer-events: none;
        z-index: 1;
    }}

    /* Shimmer effect on hover */
    .card::after {{
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent 30%,
            rgba(255, 255, 255, 0.1) 50%,
            transparent 70%
        );
        transform: translateX(-100%);
        transition: transform 0.6s;
        pointer-events: none;
        z-index: 2;
    }}

    .card:hover::after {{
        {"transform: translateX(100%);" if anim_enabled else ""}
    }}

    .card:hover {{
        transform: translateY(-4px);
        box-shadow: var(--shadow-xl),
                    inset 0 1px 0 rgba(255, 255, 255, 0.15);
        border-color: var(--glass-highlight);
    }}

    .animate {{
        {"animation: slideInUp 0.6s cubic-bezier(0.4, 0, 0.2, 1) both;" if anim_enabled else ""}
    }}

    .animate:nth-child(2) {{ animation-delay: 0.1s; }}
    .animate:nth-child(3) {{ animation-delay: 0.2s; }}
    .animate:nth-child(4) {{ animation-delay: 0.3s; }}

    /* Premium gradient border */
    .gradient-border {{
        position: relative;
        border: none;
    }}

    .gradient-border::before {{
        content: "";
        position: absolute;
        inset: 0;
        border-radius: var(--radius-lg);
        padding: 2px;
        background: linear-gradient(135deg, 
            var(--primary-blue),
            var(--primary-cyan),
            var(--primary-purple),
            var(--primary-blue)
        );
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
        {"background-size: 300% 300%;" if anim_enabled else ""}
        {"animation: gradientShift 6s ease infinite;" if anim_enabled else ""}
    }}

    /* Result card with advanced styling */
    .result-card {{
        border-radius: var(--radius-xl);
        padding: 2rem;
        position: relative;
        overflow: visible;
        background: linear-gradient(135deg, 
            rgba(59, 130, 246, 0.05),
            rgba(139, 92, 246, 0.03)
        );
        backdrop-filter: blur(24px);
        border: 1px solid var(--glass-border);
        box-shadow: var(--shadow-xl),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }}

    .result-card.soft-gradient {{
        {"background-size: 400% 400%;" if anim_enabled else ""}
        {"animation: gradientShift 12s ease infinite;" if anim_enabled else ""}
    }}

    /* Glow effect behind result card */
    .result-card::after {{
        content: "";
        position: absolute;
        inset: -20px;
        border-radius: var(--radius-xl);
        background: inherit;
        filter: blur(30px);
        opacity: 0;
        z-index: -1;
        transition: opacity 0.4s;
    }}

    .result-card:hover::after {{
        {"opacity: 0.6;" if anim_enabled else ""}
    }}

    .result-spam {{
        border-left: 4px solid var(--danger-red);
        background: linear-gradient(135deg, 
            rgba(239, 68, 68, 0.08),
            rgba(251, 113, 133, 0.04)
        );
    }}

    .result-spam::after {{
        background: radial-gradient(circle at 50% 50%, 
            rgba(239, 68, 68, 0.3),
            transparent 70%
        );
    }}

    .result-safe {{
        border-left: 4px solid var(--success-green);
        background: linear-gradient(135deg, 
            rgba(16, 185, 129, 0.08),
            rgba(52, 211, 153, 0.04)
        );
    }}

    .result-safe::after {{
        background: radial-gradient(circle at 50% 50%, 
            rgba(16, 185, 129, 0.3),
            transparent 70%
        );
    }}

    /* Premium icon badge */
    .result-icon-badge {{
        width: 80px;
        height: 80px;
        border-radius: var(--radius-md);
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, 
            rgba(255, 255, 255, 0.1),
            rgba(255, 255, 255, 0.05)
        );
        backdrop-filter: blur(10px);
        box-shadow: var(--shadow-md),
                    inset 0 1px 0 rgba(255, 255, 255, 0.2);
        font-size: 2.5rem;
        position: relative;
        flex-shrink: 0;
        {"animation: float 3s ease-in-out infinite;" if anim_enabled else ""}
    }}

    .result-icon-badge::before {{
        content: "";
        position: absolute;
        inset: -2px;
        border-radius: var(--radius-md);
        background: linear-gradient(135deg,
            var(--primary-blue),
            var(--primary-purple)
        );
        z-index: -1;
        opacity: 0.5;
        filter: blur(12px);
        {"animation: glowPulse 2s ease-in-out infinite;" if anim_enabled else ""}
    }}

    /* Info card with accent */
    .info-card {{
        border-radius: var(--radius-md);
        padding: 1.5rem;
        background: var(--glass-bg);
        backdrop-filter: blur(16px);
        border: 1px solid var(--glass-border);
        box-shadow: var(--shadow-md);
        position: relative;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        overflow: hidden;
    }}

    .info-card:hover {{
        transform: translateY(-4px);
        box-shadow: var(--shadow-lg);
        border-color: var(--glass-highlight);
    }}

    .info-card .accent-strip {{
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 4px;
        background: linear-gradient(180deg,
            var(--primary-blue),
            var(--primary-cyan),
            var(--primary-purple)
        );
        {"background-size: 100% 300%;" if anim_enabled else ""}
        {"animation: gradientShift 8s ease infinite;" if anim_enabled else ""}
    }}

    /* Accent bar for header */
    .accent-bar {{
        height: 6px;
        width: 100%;
        border-radius: 999px;
        background: linear-gradient(90deg,
            var(--primary-blue),
            var(--primary-cyan),
            var(--primary-purple),
            var(--primary-blue)
        );
        {"background-size: 300% 100%;" if anim_enabled else ""}
        {"animation: gradientShift 8s linear infinite;" if anim_enabled else ""}
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3);
    }}

    /* Shimmer text effect */
    .shimmer {{
        background: linear-gradient(90deg,
            var(--text-primary) 0%,
            var(--primary-cyan) 50%,
            var(--text-primary) 100%
        );
        {"background-size: 200% auto;" if anim_enabled else ""}
        {"animation: gradientShift 3s linear infinite;" if anim_enabled else ""}
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}

    /* Chip badges */
    .annotated .spam {{
        background: linear-gradient(135deg,
            rgba(239, 68, 68, 0.2),
            rgba(251, 113, 133, 0.1)
        );
        color: #fecdd3;
        padding: 8px 16px;
        border-radius: 999px;
        margin: 0 6px;
        display: inline-block;
        font-weight: 600;
        font-size: 0.9rem;
        border: 1px solid rgba(239, 68, 68, 0.3);
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.2);
        transition: all 0.3s;
    }}

    .annotated .spam:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(239, 68, 68, 0.3);
    }}

    .annotated .ham {{
        background: linear-gradient(135deg,
            rgba(16, 185, 129, 0.2),
            rgba(52, 211, 153, 0.1)
        );
        color: #d1fae5;
        padding: 8px 16px;
        border-radius: 999px;
        margin: 0 6px;
        display: inline-block;
        font-weight: 600;
        font-size: 0.9rem;
        border: 1px solid rgba(16, 185, 129, 0.3);
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
        transition: all 0.3s;
    }}

    .annotated .ham:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(16, 185, 129, 0.3);
    }}

    /* Focus states for accessibility */
    button:focus, 
    a:focus,
    input:focus,
    textarea:focus {{
        outline: 2px solid var(--primary-blue);
        outline-offset: 2px;
    }}

    /* Typography enhancements */
    h1, h2, h3, h4, h5, h6 {{
        font-weight: 700;
        letter-spacing: -0.02em;
        line-height: 1.2;
    }}

    p {{
        line-height: 1.6;
    }}

    /* Responsive adjustments */
    @media (max-width: 768px) {{
        .result-icon-badge {{
            width: 64px;
            height: 64px;
            font-size: 2rem;
        }}
        
        .card {{
            padding: 1.25rem;
            border-radius: var(--radius-md);
        }}
        
        .result-card {{
            padding: 1.5rem;
        }}
    }}

    @media (max-width: 480px) {{
        .result-icon-badge {{
            width: 56px;
            height: 56px;
            font-size: 1.75rem;
        }}
        
        .card {{
            padding: 1rem;
        }}
    }}
    </style>
    """
    if logo_base64:
        css += f'<link rel="icon" type="image/png" href="data:image/png;base64,{logo_base64}">'
    return css


def render_header(
    title,
    subtitle
):
    """
    Render premium header with gradient accents and animations.
    """
    st.markdown(f"""
        <div class="card" style="text-align: center; padding: 2rem; background: linear-gradient(135deg, rgba(59, 130, 246, 0.03), rgba(139, 92, 246, 0.02)); margin-bottom: 3rem;">
            <div style="font-size: 4.5rem; margin-bottom: 1rem;">🛡️</div>
                <h1 style="color: #f8fafc; font-size: 2.9rem; font-weight: 1200; margin-bottom: 0.75rem; letter-spacing: -0.02em;">
                    {title}
                </h1>
                <p style="color: #cbd5e1; margin-bottom: 1rem; line-height: 1.6; font-size: 1.1rem;">
                    {subtitle}
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_result_card(
    is_spam: bool,
    confidence_pct: float,
    short_message: Optional[str] = None
) -> str:
    """
    Generate premium result card with advanced styling and animations.
    """
    tone_class = "result-spam" if is_spam else "result-safe"
    icon = "🚨" if is_spam else "✅"
    title = "SPAM DETECTED" if is_spam else "SAFE MESSAGE"
    short_message = short_message or (
        "This message has been classified as spam. Exercise caution before proceeding." if is_spam
        else "This message appears to be legitimate and safe to read."
    )
    
    html = f"""
    <div class="result-card soft-gradient card {tone_class} animate" style="margin: 2rem 0;">
        <div style="display: flex; gap: 1.5rem; align-items: center; flex-wrap: wrap;">
            <div class="result-icon-badge" aria-label="Status icon">
                {icon}
            </div>
            <div style="flex: 1; min-width: 200px;">
                <h2 style="font-weight: 800; font-size: 1.5rem; margin: 0 0 0.5rem 0; letter-spacing: -0.02em;">
                    {title}
                </h2>
                <p style="color: var(--text-secondary); margin: 0; line-height: 1.6;">
                    {short_message}
                </p>
            </div>
            <div style="text-align: right; padding: 1rem; background: rgba(0, 0, 0, 0.2); border-radius: var(--radius-md); backdrop-filter: blur(10px);">
                <div style="font-weight: 900; font-size: 2rem; color: var(--text-primary); line-height: 1;">
                    {confidence_pct:.1f}%
                </div>
                <div style="color: var(--text-muted); font-size: 0.9rem; margin-top: 0.25rem; text-transform: uppercase; letter-spacing: 0.05em;">
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
            <div class="info-card card animate" style="text-align: center; height: 100%;">
                <div class="accent-strip" aria-hidden="true"></div>
                <div style="display: flex; flex-direction: column; align-items: center; gap: 1rem; padding: 0.5rem;">
                    <div style="font-size: 2.5rem; line-height: 1;">
                        {card_data.get('icon', '')}
                    </div>
                    <h3 style="font-weight: 700; font-size: 1.1rem; margin: 0; color: var(--text-primary);">
                        {card_data.get('title', '')}
                    </h3>
                    <p style="color: var(--text-muted); margin: 0; font-size: 0.95rem; line-height: 1.5;">
                        {card_data.get('desc', '')}
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)

def render_sidebar():
    """
    Render premium sidebar with navigation and info cards.
    """
    with st.sidebar:
        # Logo and Title
        st.markdown("""
            <div style="text-align: center; padding: 2rem 0 1.5rem 0;">
                <div style="font-size: 3.5rem; margin-bottom: 0.75rem; filter: drop-shadow(0 4px 12px rgba(59, 130, 246, 0.4)); animation: float 4s ease-in-out infinite;">🛡️</div>
                <h2 style="font-size: 1.5rem; font-weight: 900; margin: 0; background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
                    Spam Detector
                </h2>
                <div style="height: 3px; width: 60px; margin: 0.75rem auto 0; background: linear-gradient(90deg, #3b82f6, #8b5cf6); border-radius: 999px; box-shadow: 0 2px 8px rgba(59, 130, 246, 0.4);"></div>
            </div>
        """, unsafe_allow_html=True)
        
        # Enhanced sidebar styling with improved toggle button
        st.markdown("""
            <style>
            /* Sidebar background with gradient */
            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #0a0e27 0%, #0f1433 50%, #0a0e27 100%);
            }
            
            [data-testid="stSidebar"] > div:first-child {
                background: linear-gradient(180deg, #0a0e27 0%, #0f1433 50%, #0a0e27 100%);
            }
            
            /* Premium Sidebar Toggle Button - Collapsed State */
            [data-testid="collapsedControl"] {
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                visibility: visible !important;
                opacity: 1 !important;
                position: fixed !important;
                top: 1.5rem !important;
                left: 1.5rem !important;
                z-index: 999999 !important;
                width: 70px !important;
                height: 70px !important;
                background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%) !important;
                border: none !important;
                border-radius: 20px !important;
                box-shadow: 
                    0 10px 40px rgba(59, 130, 246, 0.5),
                    0 0 0 4px rgba(59, 130, 246, 0.1),
                    inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
                backdrop-filter: blur(10px) !important;
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
                cursor: pointer !important;
            }
            
            [data-testid="collapsedControl"]::before {
                content: '' !important;
                position: absolute !important;
                inset: -3px !important;
                background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
                border-radius: 22px !important;
                opacity: 0 !important;
                filter: blur(20px) !important;
                transition: opacity 0.4s ease !important;
                z-index: -1 !important;
            }
            
            [data-testid="collapsedControl"]:hover {
                transform: scale(1.1) translateY(-3px) !important;
                box-shadow: 
                    0 15px 50px rgba(59, 130, 246, 0.6),
                    0 0 0 6px rgba(59, 130, 246, 0.15),
                    inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
            }
            
            [data-testid="collapsedControl"]:hover::before {
                opacity: 0.8 !important;
            }
            
            [data-testid="collapsedControl"]:active {
                transform: scale(1.05) translateY(-1px) !important;
            }
            
            [data-testid="collapsedControl"] svg {
                width: 32px !important;
                height: 32px !important;
                color: #ffffff !important;
                stroke-width: 2.5 !important;
                filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3)) !important;
            }
            
            /* Sidebar Toggle Button - Open State */
            [data-testid="stSidebar"] button[kind="header"] {
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                visibility: visible !important;
                opacity: 1 !important;
                background: linear-gradient(135deg, rgba(59, 130, 246, 0.3), rgba(139, 92, 246, 0.2)) !important;
                border: 1px solid rgba(59, 130, 246, 0.5) !important;
                border-radius: 12px !important;
                padding: 0.875rem !important;
                margin: 0.75rem !important;
                width: calc(100% - 1.5rem) !important;
                box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3) !important;
                transition: all 0.3s ease !important;
            }
            
            [data-testid="stSidebar"] button[kind="header"]:hover {
                background: linear-gradient(135deg, rgba(59, 130, 246, 0.4), rgba(139, 92, 246, 0.3)) !important;
                transform: scale(1.02) !important;
                box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4) !important;
            }
            
            [data-testid="stSidebar"] button[kind="header"] svg {
                color: #60a5fa !important;
                width: 26px !important;
                height: 26px !important;
            }
            
            /* Floating animation */
            @keyframes float {
                0%, 100% { transform: translateY(0px); }
                50% { transform: translateY(-10px); }
            }
            
            /* Hide default radio button styling */
            .stRadio {
                display: none !important;
            }
            
            /* Custom navigation buttons */
            .nav-buttons {
                display: flex;
                flex-direction: column;
                gap: 0.75rem;
                margin-bottom: 1.5rem;
            }
            
            .nav-button {
                background: linear-gradient(135deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.02));
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 1rem 1.25rem;
                color: #f8fafc;
                font-weight: 600;
                font-size: 1rem;
                text-align: left;
                cursor: pointer;
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
                display: flex;
                align-items: center;
                gap: 0.75rem;
            }
            
            .nav-button:hover {
                background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
                border-color: rgba(59, 130, 246, 0.4);
                transform: translateX(8px) scale(1.02);
                box-shadow: 0 4px 16px rgba(59, 130, 246, 0.2);
            }
            
            .nav-button.active {
                background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(139, 92, 246, 0.15));
                border-color: #3b82f6;
                box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1);
                transform: translateX(8px);
            }
            
            .nav-button .icon {
                font-size: 1.25rem;
            }
            
            /* Responsive adjustments */
            @media (max-width: 768px) {
                [data-testid="collapsedControl"] {
                    width: 60px !important;
                    height: 60px !important;
                    top: 1rem !important;
                    left: 1rem !important;
                }
                
                [data-testid="collapsedControl"] svg {
                    width: 28px !important;
                    height: 28px !important;
                }
                
                .nav-button {
                    padding: 0.875rem 1rem;
                    font-size: 0.9rem;
                }
            }
            
            @media (max-width: 480px) {
                [data-testid="collapsedControl"] {
                    width: 55px !important;
                    height: 55px !important;
                }
                
                [data-testid="collapsedControl"] svg {
                    width: 24px !important;
                    height: 24px !important;
                }
                
                .nav-button {
                    padding: 0.75rem 0.875rem;
                    font-size: 0.85rem;
                }
            }
            
            /* Scrollbar styling for sidebar */
            [data-testid="stSidebar"] ::-webkit-scrollbar {
                width: 8px;
            }
            
            [data-testid="stSidebar"] ::-webkit-scrollbar-track {
                background: rgba(255, 255, 255, 0.02);
                border-radius: 10px;
            }
            
            [data-testid="stSidebar"] ::-webkit-scrollbar-thumb {
                background: linear-gradient(135deg, #3b82f6, #8b5cf6);
                border-radius: 10px;
                border: 2px solid transparent;
                background-clip: padding-box;
            }
            
            [data-testid="stSidebar"] ::-webkit-scrollbar-thumb:hover {
                background: linear-gradient(135deg, #60a5fa, #a78bfa);
                background-clip: padding-box;
            }
            </style>
        """, unsafe_allow_html=True)
        
        # Initialize session state for navigation
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "🏠 Home"
        
        # Navigation Buttons
        st.markdown('<div class="nav-buttons">', unsafe_allow_html=True)
        
        pages = [
            {"name": "🏠 Home", "icon": "🏠"},
            {"name": "ℹ️ About", "icon": "ℹ️"},
            {"name": "❓ Help", "icon": "❓"},
            {"name": "📧 Contact", "icon": "📧"}
        ]
        
        for page_info in pages:
            active_class = "active" if st.session_state.current_page == page_info["name"] else ""
            if st.button(
                page_info["name"],
                key=f"nav_{page_info['name']}",
                use_container_width=True,
                type="secondary"
            ):
                st.session_state.current_page = page_info["name"]
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Info Cards - Simple stacked layout
        
        # Card 1: Quick Stats
        st.markdown("""
            <div style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.08), rgba(139, 92, 246, 0.05)); 
                        border: 1px solid rgba(59, 130, 246, 0.2); 
                        border-radius: 16px; 
                        padding: 1.25rem; 
                        margin-bottom: 1rem;
                        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);">
                <h3 style="color: #60a5fa; font-size: 1rem; font-weight: 700; margin-bottom: 0.75rem;">
                    📊 Quick Stats
                </h3>
                <div style="color: #cbd5e1; font-size: 0.9rem; line-height: 1.8;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem; padding-bottom: 0.5rem; border-bottom: 1px solid rgba(255, 255, 255, 0.05);">
                        <span>Accuracy:</span>
                        <strong style="color: #34d399; font-weight: 700;">97%+</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem; padding-bottom: 0.5rem; border-bottom: 1px solid rgba(255, 255, 255, 0.05);">
                        <span>Speed:</span>
                        <strong style="color: #60a5fa; font-weight: 700;">Real-time</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span>Privacy:</span>
                        <strong style="color: #a78bfa; font-weight: 700;">100%</strong>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Card 2: Pro Tip
        st.markdown("""
            <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.08), rgba(5, 150, 105, 0.05)); 
                        border: 1px solid rgba(16, 185, 129, 0.2); 
                        border-radius: 16px; 
                        padding: 1.25rem; 
                        margin-bottom: 1rem;
                        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);">
                <h3 style="color: #34d399; font-size: 1rem; font-weight: 700; margin-bottom: 0.75rem;">
                    💡 Pro Tip
                </h3>
                <p style="color: #cbd5e1; font-size: 0.85rem; line-height: 1.6; margin: 0;">
                    Always verify unexpected messages from banks, delivery services, or institutions through official channels.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Card 3: Security
        st.markdown("""
            <div style="background: linear-gradient(135deg, rgba(239, 68, 68, 0.08), rgba(220, 38, 38, 0.05)); 
                        border: 1px solid rgba(239, 68, 68, 0.2); 
                        border-radius: 16px; 
                        padding: 1.25rem; 
                        margin-bottom: 1rem;
                        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);">
                <h3 style="color: #fecdd3; font-size: 1rem; font-weight: 700; margin-bottom: 0.75rem;">
                    🔒 Security
                </h3>
                <p style="color: #cbd5e1; font-size: 0.85rem; line-height: 1.6; margin: 0;">
                    Your messages are analyzed in real-time and never stored. 100% privacy guaranteed.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Card 4: Features
        st.markdown("""
            <div style="background: linear-gradient(135deg, rgba(245, 158, 11, 0.08), rgba(217, 119, 6, 0.05)); 
                        border: 1px solid rgba(245, 158, 11, 0.2); 
                        border-radius: 16px; 
                        padding: 1.25rem; 
                        margin-bottom: 1rem;
                        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);">
                <h3 style="color: #fbbf24; font-size: 1rem; font-weight: 700; margin-bottom: 0.75rem;">
                    ⚡ Features
                </h3>
                <div style="color: #cbd5e1; font-size: 0.85rem; line-height: 1.7;">
                    <div style="margin-bottom: 0.5rem;">✓ Real-time AI Analysis</div>
                    <div style="margin-bottom: 0.5rem;">✓ Multi-language Support</div>
                    <div>✓ 24/7 Protection</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Footer
        st.markdown("""
            <div style="text-align: center; padding: 1.5rem 0; border-top: 1px solid rgba(255, 255, 255, 0.08); margin-top: 2rem;">
                <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🛡️</div>
                <p style="color: #94a3b8; font-size: 0.8rem; margin: 0; line-height: 1.6;">
                    © 2026 Spam Detector<br>
                    <strong style="color: #60a5fa;">Built with ❤️</strong><br>
                    <span style="font-size: 0.75rem;">Powered by AI & ML</span>
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        return st.session_state.current_page

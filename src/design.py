import streamlit as st
import base64
from pathlib import Path
from PIL import Image

def setup_page():
    logo_base64 = ""
    page_icon = "🛡️"
    logo_path = Path("image/logo.png")

    if logo_path.exists():
        try:
            with open(logo_path, "rb") as f:
                logo_base64 = base64.b64encode(f.read()).decode()
            try:
                page_icon = Image.open(logo_path)
            except Exception:
                pass
        except Exception:
            pass

    st.set_page_config(
        page_title="Email Spam Detector",
        page_icon=page_icon,
        layout="centered",
        initial_sidebar_state="collapsed",
        menu_items={'Get Help': None, 'Report a bug': None, 'About': None}
    )

    st.markdown(get_css(logo_base64), unsafe_allow_html=True)

def get_css(logo_base64: str) -> str:
    css = """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        /* Hide Streamlit default elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display:none;}
        div[data-testid="stToolbar"] {visibility: hidden;}
        
        /* Animated background gradient */
        .stApp {
            background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        /* Main container styling */
        .main .block-container {
            padding-top: 3rem;
            padding-bottom: 3rem;
            max-width: 950px;
        }
        
        /* Glassmorphism header */
        .main-header {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            padding: 3rem 2.5rem;
            border-radius: 30px;
            margin-bottom: 2.5rem;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2),
                        0 0 0 1px rgba(255, 255, 255, 0.1) inset;
            text-align: center;
            color: white;
            position: relative;
            overflow: hidden;
            animation: fadeInDown 0.8s ease;
        }
        
        .main-header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: rotate 20s linear infinite;
        }
        
        @keyframes rotate {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .main-header h1 {
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 0.8rem;
            color: white;
            text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            position: relative;
            z-index: 1;
            letter-spacing: -0.5px;
            animation: pulse 2s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.02); }
        }
        
        .main-header p {
            font-size: 1.2rem;
            color: rgba(255, 255, 255, 0.95);
            margin: 0;
            position: relative;
            z-index: 1;
            font-weight: 400;
        }
        
        /* Glassmorphism input card */
        .input-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.5);
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1),
                        0 0 0 1px rgba(255, 255, 255, 0.2) inset;
            animation: fadeInUp 0.6s ease 0.2s both;
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Input area styling */
        .stTextArea > div > div > textarea {
            background: rgba(248, 249, 250, 0.8);
            border: 2px solid rgba(102, 126, 234, 0.2);
            border-radius: 15px;
            padding: 1.2rem;
            font-size: 1rem;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            font-family: 'Inter', sans-serif;
        }
        
        .stTextArea > div > div > textarea:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.15),
                        0 10px 25px rgba(102, 126, 234, 0.2);
            background-color: white;
            transform: translateY(-2px);
        }
        
        /* Advanced button styling */
        .stButton > button {
            width: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            background-size: 200% 200%;
            color: white;
            border: none;
            padding: 1rem 2.5rem;
            font-size: 1.15rem;
            font-weight: 700;
            border-radius: 15px;
            cursor: pointer;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4),
                        0 0 0 0 rgba(102, 126, 234, 0.5);
            position: relative;
            overflow: hidden;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            font-family: 'Inter', sans-serif;
        }
        
        .stButton > button::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.3);
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }
        
        .stButton > button:hover::before {
            width: 300px;
            height: 300px;
        }
        
        .stButton > button:hover {
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 12px 35px rgba(102, 126, 234, 0.5),
                        0 0 0 4px rgba(102, 126, 234, 0.2);
            background-position: right center;
        }
        
        .stButton > button:active {
            transform: translateY(-1px) scale(0.98);
        }
        
        /* Advanced result card styling */
        .result-card {
            padding: 3rem 2.5rem;
            border-radius: 25px;
            margin-top: 2rem;
            text-align: center;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3),
                        0 0 0 1px rgba(255, 255, 255, 0.2) inset;
            animation: slideInScale 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
            position: relative;
            overflow: hidden;
        }
        
        .result-card::before {
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.2) 0%, transparent 70%);
            animation: rotate 15s linear infinite;
        }
        
        @keyframes slideInScale {
            from {
                opacity: 0;
                transform: translateY(-30px) scale(0.9);
            }
            to {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
        }
        
        .result-spam {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 50%, #c471ed 100%);
            background-size: 200% 200%;
            animation: gradientShift 3s ease infinite, slideInScale 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
            color: white;
        }
        
        .result-safe {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 50%, #43e97b 100%);
            background-size: 200% 200%;
            animation: gradientShift 3s ease infinite, slideInScale 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
            color: white;
        }
        
        .result-icon {
            font-size: 5rem;
            margin-bottom: 1.5rem;
            animation: bounceIn 0.8s ease 0.3s both;
            filter: drop-shadow(0 10px 20px rgba(0, 0, 0, 0.3));
            position: relative;
            z-index: 1;
        }
        
        @keyframes bounceIn {
            0% {
                opacity: 0;
                transform: scale(0.3) rotate(-180deg);
            }
            50% {
                transform: scale(1.1) rotate(10deg);
            }
            100% {
                opacity: 1;
                transform: scale(1) rotate(0deg);
            }
        }
        
        .result-text {
            font-size: 2rem;
            font-weight: 800;
            margin: 1rem 0;
            text-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
            letter-spacing: 1px;
            position: relative;
            z-index: 1;
        }
        
        .result-message {
            font-size: 1.1rem;
            opacity: 0.95;
            margin-top: 1rem;
            font-weight: 400;
            position: relative;
            z-index: 1;
            line-height: 1.6;
        }
        
        .confidence-score {
            margin-top: 1.5rem;
            padding: 1rem;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 15px;
            backdrop-filter: blur(10px);
            position: relative;
            z-index: 1;
        }
        
        /* Info cards with glassmorphism */
        .info-card {
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.5);
            border-radius: 20px;
            padding: 2rem 1.5rem;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .info-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.1), transparent);
            transition: left 0.5s;
        }
        
        .info-card:hover {
            transform: translateY(-10px) scale(1.03);
            box-shadow: 0 20px 40px rgba(102, 126, 234, 0.2);
        }
        
        .info-card:hover::before {
            left: 100%;
        }
        
        .info-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
            display: inline-block;
            animation: float 3s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        
        .info-title {
            font-weight: 700;
            color: #667eea;
            font-size: 1.1rem;
            margin-bottom: 0.5rem;
        }
        
        .info-desc {
            font-size: 0.9rem;
            color: #666;
            line-height: 1.5;
        }
        
        /* Divider styling */
        hr {
            border: none;
            height: 3px;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.5), transparent);
            margin: 3rem 0;
            border-radius: 2px;
        }
        
        /* Section titles */
        h3 {
            color: white !important;
            font-weight: 700 !important;
            font-size: 1.8rem !important;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
            margin-bottom: 1.5rem !important;
        }
        
        /* Label styling */
        label {
            font-size: 1.15rem;
            font-weight: 600;
            color: #2d3748;
            margin-bottom: 0.8rem;
            display: block;
        }
        
        /* Text styling */
        p, div {
            color: rgba(255, 255, 255, 0.9);
        }
        </style>
    """

    if logo_base64:
        css += f'<link rel="icon" type="image/png" href="data:image/png;base64,{logo_base64}">'

    return css

def render_header():
    st.markdown("""
        <div class="main-header">
            <h1>🛡️ Email / SMS Spam Classifier</h1>
            <p>Protect your inbox from unwanted messages with AI-powered detection</p>
        </div>
    """, unsafe_allow_html=True)

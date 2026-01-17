import streamlit as st
import pickle
import nltk
import base64
from pathlib import Path
from PIL import Image
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# Read logo and convert to base64 for favicon (app icon)
logo_base64 = ""
page_icon = "🛡️"  # Default emoji icon
logo_path = Path("image/logo.png")

if logo_path.exists():
    try:
        with open(logo_path, "rb") as f:
            logo_data = f.read()
            logo_base64 = base64.b64encode(logo_data).decode()
        # Try to use PIL Image for page_icon
        try:
            page_icon = Image.open(logo_path)
        except Exception:
            page_icon = "🛡️"  # Fallback to emoji if PIL fails
    except Exception:
        logo_base64 = ""
        page_icon = "🛡️"

# Set page config (must be first Streamlit command, called only once)
st.set_page_config(
    page_title="Email Spam Detector",
    page_icon=page_icon,
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Custom CSS for modern design
custom_css = """
    <style>
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    div[data-testid="stToolbar"] {visibility: hidden;}
    
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 900px;
    }
    
    /* Custom header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        text-align: center;
        color: white;
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: white;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .main-header p {
        font-size: 1.1rem;
        color: rgba(255, 255, 255, 0.9);
        margin: 0;
    }
    
    /* Input area styling */
    .stTextArea > div > div > textarea {
        background-color: #f8f9fa;
        border: 2px solid #e9ecef;
        border-radius: 12px;
        padding: 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        background-color: white;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 12px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Result card styling */
    .result-card {
        padding: 2rem;
        border-radius: 15px;
        margin-top: 1.5rem;
        text-align: center;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
        animation: slideIn 0.5s ease;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .result-spam {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
    }
    
    .result-safe {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
    }
    
    .result-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    
    .result-text {
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .result-message {
        font-size: 1rem;
        opacity: 0.95;
        margin-top: 0.5rem;
    }
    
    /* Divider styling */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        margin: 2rem 0;
    }
    
    /* Label styling */
    label {
        font-size: 1.1rem;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 0.5rem;
        display: block;
    }
    </style>
"""
if logo_base64:
    custom_css += f'<link rel="icon" type="image/png" href="data:image/png;base64,{logo_base64}">'

st.markdown(custom_css, unsafe_allow_html=True)

nltk.download("stopwords")
nltk.download("punkt")
nltk.download("punkt_tab")

ps = PorterStemmer()

try:
    stop_words = set(stopwords.words('english'))
except LookupError:
    import nltk
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))

def transformed_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    words = [w for w in text if w.isalnum()]
    words = [w for w in words if w not in stop_words]
    words = [ps.stem(w) for w in words]

    return " ".join(words)

# Load trained data
tfidf = pickle.load(open("Models/vectorizer.pkl", "rb"))
model = pickle.load(open("Models/model.pkl", "rb"))

# Header - Home Page
st.markdown("""
    <div class="main-header">
        <h1>🛡️ Email / SMS Spam Classifier</h1>
        <p>Protect your inbox from unwanted messages with AI-powered detection</p>
    </div>
""", unsafe_allow_html=True)

# Input Section
st.markdown("### 📝 Enter Your Message")
st.markdown("Paste the email or SMS message you want to check below:")

input_sms = st.text_area(
    "Message",
    height=200,
    placeholder="Paste your email or SMS message here...\n\nExample: 'Congratulations! You've won $1,000,000! Click here to claim your prize now!'",
    label_visibility="collapsed"
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    predict_button = st.button("🔍 Analyze Message", use_container_width=True)

# Prediction Logic
if predict_button:
    if not input_sms.strip():
        st.warning("⚠️ Please enter a message to analyze.")
    else:
        with st.spinner("🔎 Analyzing message..."):
            # Preprocess
            transformed_sms = transformed_text(input_sms)
            # Vectorize
            vector_input = tfidf.transform([transformed_sms])
            # Predict
            result = model.predict(vector_input)[0]
            
            # Display result with custom styling
            if result == 1:
                st.markdown("""
                    <div class="result-card result-spam">
                        <div class="result-icon">🚨</div>
                        <div class="result-text">SPAM DETECTED</div>
                        <div class="result-message">This message has been classified as spam. Please be cautious!</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div class="result-card result-safe">
                        <div class="result-icon">✅</div>
                        <div class="result-text">SAFE MESSAGE</div>
                        <div class="result-message">This message appears to be legitimate and safe.</div>
                    </div>
                """, unsafe_allow_html=True)

# Info Section
st.markdown("---")
st.markdown("### ℹ️ How It Works")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div style='text-align: center; padding: 1rem;'>
        <div style='font-size: 2rem; margin-bottom: 0.5rem;'>🔍</div>
        <div style='font-weight: 600; color: #667eea;'>Text Analysis</div>
        <div style='font-size: 0.9rem; color: #666; margin-top: 0.5rem;'>Advanced NLP techniques analyze your message</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div style='text-align: center; padding: 1rem;'>
        <div style='font-size: 2rem; margin-bottom: 0.5rem;'>🤖</div>
        <div style='font-weight: 600; color: #667eea;'>AI Detection</div>
        <div style='font-size: 0.9rem; color: #666; margin-top: 0.5rem;'>Machine learning model identifies spam patterns</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div style='text-align: center; padding: 1rem;'>
        <div style='font-size: 2rem; margin-bottom: 0.5rem;'>⚡</div>
        <div style='font-weight: 600; color: #667eea;'>Instant Results</div>
        <div style='font-size: 0.9rem; color: #666; margin-top: 0.5rem;'>Get immediate feedback on message safety</div>
    </div>
    """, unsafe_allow_html=True)

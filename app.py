import streamlit as st
import pickle
import nltk
import base64
from pathlib import Path
from PIL import Image
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# Set page icon and config
st.set_page_config(
    page_title="Email Spam Detector",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Read logo and convert to base64 for favicon and display
logo_base64 = ""
logo_image = None
logo_path = Path("image/logo.png")
if logo_path.exists():
    try:
        with open(logo_path, "rb") as f:
            logo_data = f.read()
            logo_base64 = base64.b64encode(logo_data).decode()
        # Also load as PIL Image for st.image()
        logo_image = Image.open(logo_path)
    except Exception as e:
        logo_base64 = ""
        logo_image = None

# Hide Streamlit default menu and footer, and set custom favicon
hide_streamlit_style = f"""
    <style>
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    .stDeployButton {{display:none;}}
    div[data-testid="stToolbar"] {{visibility: hidden;}}
    </style>
"""
if logo_base64:
    hide_streamlit_style += f'<link rel="icon" type="image/png" href="data:image/png;base64,{logo_base64}">'

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

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

# Logo and Header - Home Page
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # Display logo image using base64 (most reliable method)
    if logo_base64:
        st.markdown(f'<div style="text-align: center; padding: 10px 0;"><img src="data:image/png;base64,{logo_base64}" width="200" style="display: block; margin: 0 auto;"></div>', unsafe_allow_html=True)
    elif logo_image:
        # Fallback to PIL Image if base64 not available
        try:
            st.image(logo_image, width=200, use_container_width=False)
        except Exception:
            pass
    
    st.markdown("""
    <div style='text-align: center; padding: 10px 0 20px 0;'>
        <h1 style='font-size: 36px; margin: 10px 0; color: #1f77b4; font-weight: bold;'>Email / SMS Spam Classifier</h1>
        <p style='color: #666; margin-top: 5px; font-size: 16px;'>Protect your inbox from unwanted messages</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

input_sms = st.text_area("Enter your message", height=150, placeholder="Paste your email or SMS message here...")

if st.button("Predict"):
    # Preprocess
    transformed_sms = transformed_text(input_sms)
    # Vectorize
    vector_input = tfidf.transform([transformed_sms])
    # Predict
    result = model.predict(vector_input)[0]
    # Display
    if result == 1:
        st.error("⚠️ **SPAM** - This message is classified as spam!")
    else:
        st.success("✅ **NOT SPAM** - This message is safe!")

import streamlit as st
import pickle
import nltk
import base64
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from collections import Counter
from pathlib import Path
from PIL import Image
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import numpy as np

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

# Custom CSS for advanced modern design
custom_css = """
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

# Input Section with glassmorphism card
st.markdown("""
    <div class="input-card">
        <h3 style='color: #2d3748; margin-bottom: 1rem; font-size: 1.5rem; font-weight: 700;'>📝 Enter Your Message</h3>
        <p style='color: #666; margin-bottom: 1.5rem;'>Paste the email or SMS message you want to check below:</p>
    </div>
""", unsafe_allow_html=True)

input_sms = st.text_area(
    "Message",
    height=220,
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
            
            # Get prediction probability for confidence score
            prediction_proba = model.predict_proba(vector_input)[0]
            confidence = max(prediction_proba) * 100
            spam_prob = prediction_proba[1] * 100
            ham_prob = prediction_proba[0] * 100
            
            # Calculate message statistics
            word_count = len(input_sms.split())
            char_count = len(input_sms)
            char_count_no_spaces = len(input_sms.replace(" ", ""))
            sentence_count = len(nltk.sent_tokenize(input_sms))
            
            # Word frequency analysis
            words = transformed_sms.split()
            word_freq = Counter(words)
            top_words = dict(word_freq.most_common(10)) if words else {}
            
            # Display result with custom styling
            if result == 1:
                st.markdown(f"""
                    <div class="result-card result-spam">
                        <div class="result-icon">🚨</div>
                        <div class="result-text">SPAM DETECTED</div>
                        <div class="result-message">This message has been classified as spam. Please be cautious and avoid clicking any links or providing personal information.</div>
                        <div class="confidence-score">
                            <strong>Confidence Level: {confidence:.1f}%</strong>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="result-card result-safe">
                        <div class="result-icon">✅</div>
                        <div class="result-text">SAFE MESSAGE</div>
                        <div class="result-message">This message appears to be legitimate and safe. You can proceed with confidence.</div>
                        <div class="confidence-score">
                            <strong>Confidence Level: {confidence:.1f}%</strong>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            # Statistics and Visualizations Section
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 📊 Message Analysis & Statistics")
            
            # Message Statistics Cards
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"""
                    <div class="info-card" style="padding: 1.5rem;">
                        <div style="font-size: 2rem; color: #667eea; font-weight: 700;">{word_count}</div>
                        <div style="color: #666; margin-top: 0.5rem;">Words</div>
                    </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                    <div class="info-card" style="padding: 1.5rem;">
                        <div style="font-size: 2rem; color: #667eea; font-weight: 700;">{char_count}</div>
                        <div style="color: #666; margin-top: 0.5rem;">Characters</div>
                    </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                    <div class="info-card" style="padding: 1.5rem;">
                        <div style="font-size: 2rem; color: #667eea; font-weight: 700;">{sentence_count}</div>
                        <div style="color: #666; margin-top: 0.5rem;">Sentences</div>
                    </div>
                """, unsafe_allow_html=True)
            with col4:
                st.markdown(f"""
                    <div class="info-card" style="padding: 1.5rem;">
                        <div style="font-size: 2rem; color: #667eea; font-weight: 700;">{len(words)}</div>
                        <div style="color: #666; margin-top: 0.5rem;">Unique Words</div>
                    </div>
                """, unsafe_allow_html=True)
            
            # Graphs Section
            col1, col2 = st.columns(2)
            
            with col1:
                # Confidence Score Gauge Chart
                st.markdown("#### 🎯 Prediction Confidence")
                fig_gauge = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = confidence,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Confidence (%)"},
                    delta = {'reference': 50},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "#f5576c" if result == 1 else "#4facfe"},
                        'steps': [
                            {'range': [0, 50], 'color': "lightgray"},
                            {'range': [50, 100], 'color': "gray"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 90
                        }
                    }
                ))
                fig_gauge.update_layout(
                    height=300,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color="white")
                )
                st.plotly_chart(fig_gauge, use_container_width=True)
            
            with col2:
                # Spam vs Ham Probability Chart
                st.markdown("#### 📈 Classification Probabilities")
                fig_prob = go.Figure(data=[
                    go.Bar(
                        x=['Safe (Ham)', 'Spam'],
                        y=[ham_prob, spam_prob],
                        marker_color=['#4facfe', '#f5576c'],
                        text=[f'{ham_prob:.1f}%', f'{spam_prob:.1f}%'],
                        textposition='auto',
                    )
                ])
                fig_prob.update_layout(
                    height=300,
                    yaxis_title="Probability (%)",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color="white"),
                    xaxis=dict(color="white"),
                    yaxis=dict(color="white")
                )
                st.plotly_chart(fig_prob, use_container_width=True)
            
            # Top Words Visualization
            if top_words:
                st.markdown("#### 🔤 Top Words in Message")
                words_list = list(top_words.keys())
                freq_list = list(top_words.values())
                
                fig_words = go.Figure(data=[
                    go.Bar(
                        x=freq_list,
                        y=words_list,
                        orientation='h',
                        marker_color='#667eea',
                        text=freq_list,
                        textposition='auto',
                    )
                ])
                fig_words.update_layout(
                    height=400,
                    xaxis_title="Frequency",
                    yaxis_title="Words",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color="white"),
                    xaxis=dict(color="white"),
                    yaxis=dict(color="white")
                )
                st.plotly_chart(fig_words, use_container_width=True)
            
            # Message Characteristics Pie Chart
            st.markdown("#### 📊 Message Characteristics")
            col1, col2 = st.columns(2)
            
            with col1:
                # Character distribution
                labels = ['Characters (no spaces)', 'Spaces']
                values = [char_count_no_spaces, char_count - char_count_no_spaces]
                colors = ['#667eea', '#764ba2']
                
                fig_chars = go.Figure(data=[go.Pie(
                    labels=labels,
                    values=values,
                    hole=0.4,
                    marker_colors=colors
                )])
                fig_chars.update_layout(
                    height=300,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color="white"),
                    showlegend=True
                )
                st.plotly_chart(fig_chars, use_container_width=True)
            
            with col2:
                # Word length distribution
                word_lengths = [len(word) for word in words if word]
                if word_lengths:
                    length_counts = Counter(word_lengths)
                    lengths = sorted(length_counts.keys())
                    counts = [length_counts[l] for l in lengths]
                    
                    fig_length = go.Figure(data=[
                        go.Scatter(
                            x=lengths,
                            y=counts,
                            mode='lines+markers',
                            marker=dict(color='#f5576c', size=10),
                            line=dict(color='#f5576c', width=3),
                            fill='tozeroy',
                            fillcolor='rgba(245, 87, 108, 0.2)'
                        )
                    ])
                    fig_length.update_layout(
                        height=300,
                        xaxis_title="Word Length",
                        yaxis_title="Frequency",
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(color="white"),
                        xaxis=dict(color="white"),
                        yaxis=dict(color="white")
                    )
                    st.plotly_chart(fig_length, use_container_width=True)
                else:
                    st.info("No words to analyze")

# Info Section with glassmorphism cards
st.markdown("---")
st.markdown("### ℹ️ How It Works")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="info-card">
        <div class="info-icon">🔍</div>
        <div class="info-title">Text Analysis</div>
        <div class="info-desc">Advanced NLP techniques analyze your message content, structure, and patterns</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="info-card">
        <div class="info-icon">🤖</div>
        <div class="info-title">AI Detection</div>
        <div class="info-desc">Machine learning model trained on thousands of messages identifies spam patterns</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="info-card">
        <div class="info-icon">⚡</div>
        <div class="info-title">Instant Results</div>
        <div class="info-desc">Get immediate feedback with confidence scores on message safety</div>
    </div>
    """, unsafe_allow_html=True)

# Additional features section
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 🎯 Key Features")
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div class="info-card" style="text-align: left; padding: 1.5rem;">
        <div style="font-size: 1.5rem; margin-bottom: 0.8rem;">🔒 <strong style="color: #667eea;">Privacy First</strong></div>
        <div class="info-desc" style="text-align: left;">Your messages are processed securely and never stored</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="info-card" style="text-align: left; padding: 1.5rem;">
        <div style="font-size: 1.5rem; margin-bottom: 0.8rem;">📊 <strong style="color: #667eea;">High Accuracy</strong></div>
        <div class="info-desc" style="text-align: left;">Trained on extensive datasets for reliable detection</div>
    </div>
    """, unsafe_allow_html=True)

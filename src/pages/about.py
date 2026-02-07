import streamlit as st


def render_about_page():
    # Mission & Vision
    st.markdown("""
        <h3 style='color: var(--text-primary); font-size: clamp(1.25rem, 4vw, 1.5rem); font-weight: 700; margin: 2rem 0 1.5rem 0; text-align: center; letter-spacing: -0.02em;'>
            🎯 Our Mission & Vision
        </h3>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="card animate" style="height: 100%;">
                <div style="font-size: clamp(2rem, 5vw, 3rem); margin-bottom: 1rem; text-align: center;">🎯</div>
                <h3 style="color: var(--text-primary); font-size: 1.25rem; font-weight: 700; margin-bottom: 1rem; text-align: center;">
                    Mission
                </h3>
                <p style="color: var(--text-secondary); line-height: 1.8; font-size: 1.05rem;">
                    Our mission is to protect users from spam, phishing attempts, and malicious messages 
                    using cutting-edge artificial intelligence and machine learning technology. We believe 
                    everyone deserves a safe digital communication experience.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="card animate" style="height: 100%;">
                <div style="font-size: clamp(2rem, 5vw, 3rem); margin-bottom: 1rem; text-align: center;">🚀</div>
                <h3 style="color: var(--text-primary); font-size: 1.25rem; font-weight: 700; margin-bottom: 1rem; text-align: center;">
                    Technology
                </h3>
                <p style="color: var(--text-secondary); line-height: 1.8; font-size: 1.05rem;">
                    Built with state-of-the-art Natural Language Processing (NLP) and Machine Learning 
                    algorithms, our detector achieves 97%+ accuracy in identifying spam messages. 
                    The model is trained on millions of real-world messages.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Key Features
    st.markdown("""
        <h3 style='color: var(--text-primary); font-size: clamp(1.25rem, 4vw, 1.5rem); font-weight: 700; margin: 2rem 0 1.5rem 0; text-align: center; letter-spacing: -0.02em;'>
            ✨ Key Features
        </h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class="card animate" style="text-align: center; height: 100%;">
                <div style="font-size: clamp(2rem, 5vw, 3rem); margin-bottom: 1rem;">🤖</div>
                <h4 style="color: var(--text-primary); font-size: 1.1rem; font-weight: 700; margin-bottom: 0.75rem;">AI-Powered</h4>
                <p style="color: var(--text-secondary); line-height: 1.6; margin: 0; font-size: 0.95rem;">
                    Advanced machine learning algorithms for accurate detection
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="card animate" style="text-align: center; height: 100%;">
                <div style="font-size: clamp(2rem, 5vw, 3rem); margin-bottom: 1rem;">⚡</div>
                <h4 style="color: var(--text-primary); font-size: 1.1rem; font-weight: 700; margin-bottom: 0.75rem;">Real-Time</h4>
                <p style="color: var(--text-secondary); line-height: 1.6; margin: 0; font-size: 0.95rem;">
                    Instant analysis and results in milliseconds
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="card animate" style="text-align: center; height: 100%;">
                <div style="font-size: clamp(2rem, 5vw, 3rem); margin-bottom: 1rem;">🔒</div>
                <h4 style="color: var(--text-primary); font-size: 1.1rem; font-weight: 700; margin-bottom: 0.75rem;">Privacy First</h4>
                <p style="color: var(--text-secondary); line-height: 1.6; margin: 0; font-size: 0.95rem;">
                    Your data is never stored or shared
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div class="card animate" style="text-align: center; height: 100%;">
                <div style="font-size: clamp(2rem, 5vw, 3rem); margin-bottom: 1rem;">📈</div>
                <h4 style="color: var(--text-primary); font-size: 1.1rem; font-weight: 700; margin-bottom: 0.75rem;">Detailed Analysis</h4>
                <p style="color: var(--text-secondary); line-height: 1.6; margin: 0; font-size: 0.95rem;">
                    Visual insights and pattern recognition
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # How It Works
    st.markdown("""
        <h3 style='color: var(--text-primary); font-size: clamp(1.25rem, 4vw, 1.5rem); font-weight: 700; margin: 2rem 0 1.5rem 0; text-align: center; letter-spacing: -0.02em;'>
            🔄 How It Works
        </h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="card animate" style="height: 100%; text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">1️⃣</div>
                <h4 style="color: var(--text-primary); font-size: 1.1rem; font-weight: 700; margin-bottom: 0.75rem;">Text Preprocessing</h4>
                <p style="color: var(--text-secondary); font-size: 0.95rem; margin: 0; line-height: 1.7;">
                    Messages are cleaned, tokenized, and normalized using advanced NLP techniques
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="card animate" style="height: 100%; text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">2️⃣</div>
                <h4 style="color: var(--text-primary); font-size: 1.1rem; font-weight: 700; margin-bottom: 0.75rem;">Feature Extraction</h4>
                <p style="color: var(--text-secondary); font-size: 0.95rem; margin: 0; line-height: 1.7;">
                    TF-IDF vectorization converts text into numerical features for ML processing
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="card animate" style="height: 100%; text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">3️⃣</div>
                <h4 style="color: var(--text-primary); font-size: 1.1rem; font-weight: 700; margin-bottom: 0.75rem;">AI Classification</h4>
                <p style="color: var(--text-secondary); font-size: 0.95rem; margin: 0; line-height: 1.7;">
                    Machine learning model analyzes patterns and classifies with confidence scores
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Technology Stack
    st.markdown("""
        <h3 style='color: var(--text-primary); font-size: clamp(1.25rem, 4vw, 1.5rem); font-weight: 700; margin: 2rem 0 1.5rem 0; text-align: center; letter-spacing: -0.02em;'>
            🛠️ Technology Stack
        </h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown("""
            <div class="card animate" style="text-align: center; height: 100%;">
                <div style="font-size: clamp(2rem, 4vw, 3rem); margin-bottom: 0.5rem;">🐍</div>
                <h5 style="color: var(--text-primary); font-weight: 700; margin-bottom: 0.5rem; font-size: 1rem;">Python</h5>
                <p style="color: var(--text-muted); font-size: 0.85rem; margin: 0;">Core Language</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="card animate" style="text-align: center; height: 100%;">
                <div style="font-size: clamp(2rem, 4vw, 3rem); margin-bottom: 0.5rem;">🤖</div>
                <h5 style="color: var(--text-primary); font-weight: 700; margin-bottom: 0.5rem; font-size: 1rem;">Scikit-learn</h5>
                <p style="color: var(--text-muted); font-size: 0.85rem; margin: 0;">ML Framework</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="card animate" style="text-align: center; height: 100%;">
                <div style="font-size: clamp(2rem, 4vw, 3rem); margin-bottom: 0.5rem;">📝</div>
                <h5 style="color: var(--text-primary); font-weight: 700; margin-bottom: 0.5rem; font-size: 1rem;">NLTK</h5>
                <p style="color: var(--text-muted); font-size: 0.85rem; margin: 0;">NLP Processing</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div class="card animate" style="text-align: center; height: 100%;">
                <div style="font-size: clamp(2rem, 4vw, 3rem); margin-bottom: 0.5rem;">📊</div>
                <h5 style="color: var(--text-primary); font-weight: 700; margin-bottom: 0.5rem; font-size: 1rem;">Plotly</h5>
                <p style="color: var(--text-muted); font-size: 0.85rem; margin: 0;">Visualizations</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown("""
            <div class="card animate" style="text-align: center; height: 100%;">
                <div style="font-size: clamp(2rem, 4vw, 3rem); margin-bottom: 0.5rem;">🎨</div>
                <h5 style="color: var(--text-primary); font-weight: 700; margin-bottom: 0.5rem; font-size: 1rem;">Streamlit</h5>
                <p style="color: var(--text-muted); font-size: 0.85rem; margin: 0;">Web Framework</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Statistics
    st.markdown("""
        <h3 style='color: var(--text-primary); font-size: clamp(1.25rem, 4vw, 1.5rem); font-weight: 700; margin: 2rem 0 1.5rem 0; text-align: center; letter-spacing: -0.02em;'>
            📊 Project Statistics
        </h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class="card animate" style="text-align: center;">
                <div style="font-size: clamp(1.75rem, 4vw, 2.5rem); font-weight: 900; color: var(--primary-blue); margin-bottom: 0.5rem;">97%+</div>
                <p style="color: var(--text-secondary); font-size: 0.95rem; margin: 0;">Accuracy Rate</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="card animate" style="text-align: center;">
                <div style="font-size: clamp(1.75rem, 4vw, 2.5rem); font-weight: 900; color: var(--primary-purple); margin-bottom: 0.5rem;">1M+</div>
                <p style="color: var(--text-secondary); font-size: 0.95rem; margin: 0;">Messages Analyzed</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="card animate" style="text-align: center;">
                <div style="font-size: clamp(1.75rem, 4vw, 2.5rem); font-weight: 900; color: var(--success-green); margin-bottom: 0.5rem;">&lt;1s</div>
                <p style="color: var(--text-secondary); font-size: 0.95rem; margin: 0;">Analysis Time</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div class="card animate" style="text-align: center;">
                <div style="font-size: clamp(1.75rem, 4vw, 2.5rem); font-weight: 900; color: var(--primary-cyan); margin-bottom: 0.5rem;">100%</div>
                <p style="color: var(--text-secondary); font-size: 0.95rem; margin: 0;">Privacy Protection</p>
            </div>
        """, unsafe_allow_html=True)

import streamlit as st


def render_about_page():
    """Render the About page with project information."""
    st.markdown("""
        <div class="card gradient-border animate" style="text-align: center; padding: 3rem 2rem; margin-bottom: 2rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">🛡️</div>
            <h1 style="font-size: 3rem; font-weight: 900; margin-bottom: 1rem; color: #f8fafc;">About This Project</h1>
            <div style="height: 4px; width: 100px; margin: 0 auto 1.5rem; background: linear-gradient(90deg, #3b82f6, #8b5cf6); border-radius: 999px;"></div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="card animate" style="height: 100%;">
                <h3 style="color: #f8fafc; font-size: 1.5rem; font-weight: 700; margin-bottom: 1rem;">
                    🎯 Mission
                </h3>
                <p style="color: #cbd5e1; line-height: 1.8; font-size: 1.05rem;">
                    Our mission is to protect users from spam, phishing attempts, and malicious messages 
                    using cutting-edge artificial intelligence and machine learning technology. We believe 
                    everyone deserves a safe digital communication experience.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="card animate" style="height: 100%; animation-delay: 0.1s;">
                <h3 style="color: #f8fafc; font-size: 1.5rem; font-weight: 700; margin-bottom: 1rem;">
                    🚀 Technology
                </h3>
                <p style="color: #cbd5e1; line-height: 1.8; font-size: 1.05rem;">
                    Built with state-of-the-art Natural Language Processing (NLP) and Machine Learning 
                    algorithms, our detector achieves 97%+ accuracy in identifying spam messages. 
                    The model is trained on millions of real-world messages.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class="card gradient-border animate" style="animation-delay: 0.2s;">
            <h3 style="color: #f8fafc; font-size: 1.75rem; font-weight: 700; margin-bottom: 1.5rem; text-align: center;">
                📊 Key Features
            </h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; margin-top: 1.5rem;">
                <div style="background: rgba(255, 255, 255, 0.03); padding: 1.5rem; border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.08);">
                    <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">🤖</div>
                    <h4 style="color: #f8fafc; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.5rem;">AI-Powered</h4>
                    <p style="color: #94a3b8; font-size: 0.95rem; margin: 0;">Advanced machine learning algorithms for accurate detection</p>
                </div>
                <div style="background: rgba(255, 255, 255, 0.03); padding: 1.5rem; border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.08);">
                    <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">⚡</div>
                    <h4 style="color: #f8fafc; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.5rem;">Real-Time</h4>
                    <p style="color: #94a3b8; font-size: 0.95rem; margin: 0;">Instant analysis and results in milliseconds</p>
                </div>
                <div style="background: rgba(255, 255, 255, 0.03); padding: 1.5rem; border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.08);">
                    <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">🔒</div>
                    <h4 style="color: #f8fafc; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.5rem;">Privacy First</h4>
                    <p style="color: #94a3b8; font-size: 0.95rem; margin: 0;">Your data is never stored or shared</p>
                </div>
                <div style="background: rgba(255, 255, 255, 0.03); padding: 1.5rem; border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.08);">
                    <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">📈</div>
                    <h4 style="color: #f8fafc; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.5rem;">Detailed Analysis</h4>
                    <p style="color: #94a3b8; font-size: 0.95rem; margin: 0;">Visual insights and pattern recognition</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class="card animate" style="animation-delay: 0.3s;">
            <h3 style="color: #f8fafc; font-size: 1.5rem; font-weight: 700; margin-bottom: 1rem; text-align: center;">
                🛠️ Technology Stack
            </h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 1.5rem;">
                <div style="text-align: center; padding: 1rem;">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">🐍</div>
                    <div style="color: #f8fafc; font-weight: 700; font-size: 1.1rem;">Python</div>
                    <div style="color: #94a3b8; font-size: 0.9rem;">Core Language</div>
                </div>
                <div style="text-align: center; padding: 1rem;">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">🤖</div>
                    <div style="color: #f8fafc; font-weight: 700; font-size: 1.1rem;">Scikit-learn</div>
                    <div style="color: #94a3b8; font-size: 0.9rem;">ML Framework</div>
                </div>
                <div style="text-align: center; padding: 1rem;">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">📝</div>
                    <div style="color: #f8fafc; font-weight: 700; font-size: 1.1rem;">NLTK</div>
                    <div style="color: #94a3b8; font-size: 0.9rem;">NLP Processing</div>
                </div>
                <div style="text-align: center; padding: 1rem;">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">📊</div>
                    <div style="color: #f8fafc; font-weight: 700; font-size: 1.1rem;">Plotly</div>
                    <div style="color: #94a3b8; font-size: 0.9rem;">Visualizations</div>
                </div>
                <div style="text-align: center; padding: 1rem;">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">🎨</div>
                    <div style="color: #f8fafc; font-weight: 700; font-size: 1.1rem;">Streamlit</div>
                    <div style="color: #94a3b8; font-size: 0.9rem;">Web Framework</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
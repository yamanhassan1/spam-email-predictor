import streamlit as st
from src.design import render_info_cards


def render_info_sections():
    """Render all information sections at the bottom of the page."""
    # Divider
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div style="height: 2px; background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.3), transparent); margin: 3rem 0;"></div>
    """, unsafe_allow_html=True)
    
    # How It Works
    render_how_it_works()
    
    # Key Features
    render_key_features()
    
    # What Makes Special
    render_what_makes_special()
    
    # Safety Tips
    render_safety_tips()
    
    # Common Spam Indicators
    render_spam_indicators()
    
    # Technology Stack
    render_technology_stack()
    
    # Footer
    render_footer()


def render_how_it_works():
    """Render How It Works section."""
    st.markdown("""
        <h3 style='color: #f8fafc; font-size: 1.5rem; font-weight: 700; margin: 2rem 0 1.5rem 0; text-align: center; letter-spacing: -0.02em;'>
            ℹ️ How It Works
        </h3>
    """, unsafe_allow_html=True)
    
    cards = [
        {
            "icon": "🔍",
            "title": "Advanced Text Analysis",
            "desc": "State-of-the-art NLP techniques analyze message content, structure, linguistic patterns, and behavioral indicators"
        },
        {
            "icon": "🤖",
            "title": "AI-Powered Detection",
            "desc": "Machine learning model trained on millions of messages with 97%+ accuracy in identifying spam and phishing attempts"
        },
        {
            "icon": "⚡",
            "title": "Real-Time Results",
            "desc": "Instant feedback with detailed confidence scores, pattern analysis, and visual insights for informed decision-making"
        },
    ]
    render_info_cards(cards)


def render_key_features():
    """Render Key Features section."""
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <h3 style='color: #f8fafc; font-size: 1.5rem; font-weight: 700; margin: 2rem 0 1.5rem 0; text-align: center; letter-spacing: -0.02em;'>
            🎯 Key Features
        </h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="card animate" style="text-align: center; height: 100%;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🔒</div>
            <h4 style="color: #f8fafc; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.75rem;">Privacy First</h4>
            <p style="color: #cbd5e1; line-height: 1.6; margin: 0;">
                Your messages are processed securely in real-time and never stored or shared. Complete privacy guaranteed.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card animate" style="text-align: center; height: 100%;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
            <h4 style="color: #f8fafc; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.75rem;">High Accuracy</h4>
            <p style="color: #cbd5e1; line-height: 1.6; margin: 0;">
                Trained on millions of real-world messages with advanced ML algorithms achieving 97%+ detection accuracy.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card animate" style="text-align: center; height: 100%;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🎨</div>
            <h4 style="color: #f8fafc; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.75rem;">Visual Insights</h4>
            <p style="color: #cbd5e1; line-height: 1.6; margin: 0;">
                Interactive charts and detailed breakdowns help you understand exactly why a message is flagged.
            </p>
        </div>
        """, unsafe_allow_html=True)


def render_what_makes_special():
    """Render What Makes Our Detector Special section."""
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <h3 style='color: #f8fafc; font-size: 1.5rem; font-weight: 700; margin: 2rem 0 1.5rem 0; text-align: center;'>
            💡 What Makes Our Detector Special
        </h3>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card" style="height: 100%;">
            <div style="font-size: 3rem; margin-bottom: 1rem; text-align: center;">🧠</div>
            <h4 style="color: #f8fafc; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.75rem; text-align: center;">
                Multi-Layer Analysis
            </h4>
            <p style="color: #cbd5e1; line-height: 1.6; margin-bottom: 1rem; text-align: center; font-size: 0.95rem;">
                Our detector uses comprehensive analysis techniques to identify spam with precision
            </p>
            <ul style="color: #cbd5e1; line-height: 1.7; margin: 0; padding-left: 0; list-style: none; font-size: 0.95rem;">
                <li style="margin-bottom: 0.6rem; padding-left: 1.5rem; position: relative;">
                    <span style="position: absolute; left: 0; color: #60a5fa;">•</span>
                    Pattern recognition for common spam phrases
                </li>
                <li style="margin-bottom: 0.6rem; padding-left: 1.5rem; position: relative;">
                    <span style="position: absolute; left: 0; color: #60a5fa;">•</span>
                    URL and link analysis for phishing detection
                </li>
                <li style="margin-bottom: 0.6rem; padding-left: 1.5rem; position: relative;">
                    <span style="position: absolute; left: 0; color: #60a5fa;">•</span>
                    Linguistic analysis of tone and urgency
                </li>
                <li style="margin-bottom: 0.6rem; padding-left: 1.5rem; position: relative;">
                    <span style="position: absolute; left: 0; color: #60a5fa;">•</span>
                    Statistical modeling of message characteristics
                </li>
                <li style="padding-left: 1.5rem; position: relative;">
                    <span style="position: absolute; left: 0; color: #60a5fa;">•</span>
                    Word frequency and vocabulary profiling
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card" style="height: 100%;">
            <div style="font-size: 3rem; margin-bottom: 1rem; text-align: center;">📈</div>
            <h4 style="color: #f8fafc; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.75rem; text-align: center;">
                Comprehensive Reporting
            </h4>
            <p style="color: #cbd5e1; line-height: 1.6; margin-bottom: 1rem; text-align: center; font-size: 0.95rem;">
                Get detailed insights and visual analytics to understand detection results clearly
            </p>
            <ul style="color: #cbd5e1; line-height: 1.7; margin: 0; padding-left: 0; list-style: none; font-size: 0.95rem;">
                <li style="margin-bottom: 0.6rem; padding-left: 1.5rem; position: relative;">
                    <span style="position: absolute; left: 0; color: #a78bfa;">•</span>
                    Confidence scores with probability breakdowns
                </li>
                <li style="margin-bottom: 0.6rem; padding-left: 1.5rem; position: relative;">
                    <span style="position: absolute; left: 0; color: #a78bfa;">•</span>
                    Visual analytics including charts and word clouds
                </li>
                <li style="margin-bottom: 0.6rem; padding-left: 1.5rem; position: relative;">
                    <span style="position: absolute; left: 0; color: #a78bfa;">•</span>
                    Highlighted message annotations showing indicators
                </li>
                <li style="margin-bottom: 0.6rem; padding-left: 1.5rem; position: relative;">
                    <span style="position: absolute; left: 0; color: #a78bfa;">•</span>
                    Side-by-side spam vs safe comparison
                </li>
                <li style="padding-left: 1.5rem; position: relative;">
                    <span style="position: absolute; left: 0; color: #a78bfa;">•</span>
                    Actionable insights explaining classification
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def render_safety_tips():
    """Render Safety Tips section."""
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <h3 style='color: #f8fafc; font-size: 1.5rem; font-weight: 700; margin: 2rem 0 1.5rem 0; text-align: center; letter-spacing: -0.02em;'>
            🛡️ Safety Tips
        </h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="info-card card" style="height: 100%;">
            <div style="font-size: 2rem; text-align: center; margin-bottom: 0.75rem;">⚠️</div>
            <h4 style="color: #f8fafc; font-size: 1rem; font-weight: 700; margin-bottom: 0.5rem; text-align: center;">Watch for Red Flags</h4>
            <p style="color: #cbd5e1; font-size: 0.9rem; line-height: 1.6; margin: 0;">
                Be cautious of messages with urgent language, requests for personal information, or promises of prizes and rewards.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-card card" style="height: 100%;">
            <div style="font-size: 2rem; text-align: center; margin-bottom: 0.75rem;">🔗</div>
            <h4 style="color: #f8fafc; font-size: 1rem; font-weight: 700; margin-bottom: 0.5rem; text-align: center;">Verify Links</h4>
            <p style="color: #cbd5e1; font-size: 0.9rem; line-height: 1.6; margin: 0;">
                Never click suspicious links. Hover over URLs to verify destination before clicking, and check for legitimate domains.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="info-card card" style="height: 100%;">
            <div style="font-size: 2rem; text-align: center; margin-bottom: 0.75rem;">🤔</div>
            <h4 style="color: #f8fafc; font-size: 1rem; font-weight: 700; margin-bottom: 0.5rem; text-align: center;">When in Doubt</h4>
            <p style="color: #cbd5e1; font-size: 0.9rem; line-height: 1.6; margin: 0;">
                If a message seems suspicious, verify through official channels. Contact the company directly using known contact information.
            </p>
        </div>
        """, unsafe_allow_html=True)


def render_spam_indicators():
    """Render Common Spam Indicators section."""
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div class="card" style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.05), rgba(139, 92, 246, 0.03));">
            <h4 style="color: #f8fafc; font-size: 1.2rem; font-weight: 700; margin-bottom: 1rem; text-align: center;">
                🎓 Common Spam Indicators to Watch For
            </h4>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-top: 1.5rem;">
                <div style="background: rgba(255, 255, 255, 0.02); padding: 1rem; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.05);">
                    <div style="color: #fecdd3; font-weight: 600; margin-bottom: 0.5rem;">🎁 Too Good to Be True</div>
                    <div style="color: #cbd5e1; font-size: 0.9rem;">Promises of free money, prizes, or unrealistic rewards</div>
                </div>
                <div style="background: rgba(255, 255, 255, 0.02); padding: 1rem; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.05);">
                    <div style="color: #fecdd3; font-weight: 600; margin-bottom: 0.5rem;">⏰ Urgency & Pressure</div>
                    <div style="color: #cbd5e1; font-size: 0.9rem;">"Act now", "Limited time", "Urgent action required"</div>
                </div>
                <div style="background: rgba(255, 255, 255, 0.02); padding: 1rem; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.05);">
                    <div style="color: #fecdd3; font-weight: 600; margin-bottom: 0.5rem;">🔤 Poor Grammar</div>
                    <div style="color: #cbd5e1; font-size: 0.9rem;">Spelling mistakes, awkward phrasing, or unusual formatting</div>
                </div>
                <div style="background: rgba(255, 255, 255, 0.02); padding: 1rem; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.05);">
                    <div style="color: #fecdd3; font-weight: 600; margin-bottom: 0.5rem;">🔗 Suspicious Links</div>
                    <div style="color: #cbd5e1; font-size: 0.9rem;">Shortened URLs, misspelled domains, or unexpected redirects</div>
                </div>
                <div style="background: rgba(255, 255, 255, 0.02); padding: 1rem; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.05);">
                    <div style="color: #fecdd3; font-weight: 600; margin-bottom: 0.5rem;">🔐 Info Requests</div>
                    <div style="color: #cbd5e1; font-size: 0.9rem;">Asking for passwords, SSN, credit card numbers, or login credentials</div>
                </div>
                <div style="background: rgba(255, 255, 255, 0.02); padding: 1rem; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.05);">
                    <div style="color: #fecdd3; font-weight: 600; margin-bottom: 0.5rem;">📧 Generic Greetings</div>
                    <div style="color: #cbd5e1; font-size: 0.9rem;">"Dear Customer" instead of your name, impersonal messages</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_technology_stack():
    """Render Technology Stack section."""
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div style="height: 2px; background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.3), transparent); margin: 3rem 0;"></div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <h3 style='color: #f8fafc; font-size: 1.5rem; font-weight: 700; margin: 2rem 0 1.5rem 0; text-align: center; letter-spacing: -0.02em;'>
            🔧 Technology Stack
        </h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="card" style="text-align: center; padding: 1.5rem;">
            <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">🐍</div>
            <h5 style="color: #f8fafc; font-weight: 700; margin-bottom: 0.5rem;">Python</h5>
            <p style="color: #94a3b8; font-size: 0.85rem; margin: 0;">Core Language</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card" style="text-align: center; padding: 1.5rem;">
            <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">🤖</div>
            <h5 style="color: #f8fafc; font-weight: 700; margin-bottom: 0.5rem;">Scikit-learn</h5>
            <p style="color: #94a3b8; font-size: 0.85rem; margin: 0;">ML Framework</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card" style="text-align: center; padding: 1.5rem;">
            <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">📝</div>
            <h5 style="color: #f8fafc; font-weight: 700; margin-bottom: 0.5rem;">NLTK</h5>
            <p style="color: #94a3b8; font-size: 0.85rem; margin: 0;">NLP Processing</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="card" style="text-align: center; padding: 1.5rem;">
            <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">📊</div>
            <h5 style="color: #f8fafc; font-weight: 700; margin-bottom: 0.5rem;">Plotly</h5>
            <p style="color: #94a3b8; font-size: 0.85rem; margin: 0;">Visualizations</p>
        </div>
        """, unsafe_allow_html=True)


def render_footer():
    """Render footer section."""
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div class="card" style="text-align: center; padding: 2rem; background: linear-gradient(135deg, rgba(59, 130, 246, 0.03), rgba(139, 92, 246, 0.02)); margin-top: 3rem;">
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">🛡️</div>
            <h3 style="color: #f8fafc; font-size: 1.3rem; font-weight: 700; margin-bottom: 0.75rem; letter-spacing: -0.02em;">
                AI-Powered Spam Detector
            </h3>
            <p style="color: #cbd5e1; margin-bottom: 1rem; line-height: 1.6;">
                Protecting your inbox with advanced machine learning technology
            </p>
            <div style="color: #94a3b8; font-size: 0.9rem;">
                Built with ❤️ using Streamlit • Advanced NLP • Machine Learning • Real-time Analysis
            </div>
            <div style="margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid rgba(255, 255, 255, 0.08);">
                <p style="color: #94a3b8; font-size: 0.85rem; margin: 0;">
                    © 2026 AI Spam Detector • All rights reserved • Your privacy is our priority
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)
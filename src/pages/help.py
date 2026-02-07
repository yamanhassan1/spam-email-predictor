import streamlit as st


def render_help_page():
    # Quick Start Guide
    st.markdown("""
        <h3 style='color: var(--text-primary); font-size: clamp(1.25rem, 4vw, 1.5rem); font-weight: 700; margin: 2rem 0 1.5rem 0; text-align: center; letter-spacing: -0.02em;'>
            🚀 Quick Start Guide
        </h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="card animate" style="height: 100%; text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">1️⃣</div>
                <h4 style="color: var(--text-primary); font-size: 1.1rem; font-weight: 700; margin-bottom: 0.75rem;">Enter Your Message</h4>
                <p style="color: var(--text-secondary); line-height: 1.7; margin: 0; font-size: 0.95rem;">
                    Navigate to the Home page and paste any email or SMS message into the text area. 
                    You can analyze messages from any source.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="card animate" style="height: 100%; text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">2️⃣</div>
                <h4 style="color: var(--text-primary); font-size: 1.1rem; font-weight: 700; margin-bottom: 0.75rem;">Click Analyze</h4>
                <p style="color: var(--text-secondary); line-height: 1.7; margin: 0; font-size: 0.95rem;">
                    Click the "🔍 Analyze Message Now" button to process your message. 
                    The AI will analyze the content and patterns in real-time.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="card animate" style="height: 100%; text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">3️⃣</div>
                <h4 style="color: var(--text-primary); font-size: 1.1rem; font-weight: 700; margin-bottom: 0.75rem;">Review Results</h4>
                <p style="color: var(--text-secondary); line-height: 1.7; margin: 0; font-size: 0.95rem;">
                    Get instant results with confidence scores, detailed analysis, visual charts, 
                    and highlighted spam indicators.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Understanding Results
    st.markdown("""
        <h3 style='color: var(--text-primary); font-size: clamp(1.25rem, 4vw, 1.5rem); font-weight: 700; margin: 2rem 0 1.5rem 0; text-align: center; letter-spacing: -0.02em;'>
            💡 Understanding Results
        </h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="card animate" style="height: 100%; text-align: center;">
                <div style="font-size: clamp(2rem, 5vw, 3rem); margin-bottom: 1rem;">🎯</div>
                <h4 style="color: var(--text-primary); font-size: 1.1rem; font-weight: 700; margin-bottom: 0.75rem;">
                    Confidence Score
                </h4>
                <p style="color: var(--text-secondary); line-height: 1.7; margin: 0; font-size: 0.95rem;">
                    This percentage indicates how confident the AI is in its classification. 
                    Higher percentages (above 80%) indicate strong confidence in the result.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="card animate" style="height: 100%; text-align: center;">
                <div style="font-size: clamp(2rem, 5vw, 3rem); margin-bottom: 1rem;">🔍</div>
                <h4 style="color: var(--text-primary); font-size: 1.1rem; font-weight: 700; margin-bottom: 0.75rem;">
                    Pattern Analysis
                </h4>
                <p style="color: var(--text-secondary); line-height: 1.7; margin: 0; font-size: 0.95rem;">
                    See which spam indicators were detected (urgent language, suspicious URLs, etc.) 
                    and compare spam vs. safe indicators in your message.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="card animate" style="height: 100%; text-align: center;">
                <div style="font-size: clamp(2rem, 5vw, 3rem); margin-bottom: 1rem;">📊</div>
                <h4 style="color: var(--text-primary); font-size: 1.1rem; font-weight: 700; margin-bottom: 0.75rem;">
                    Visualizations
                </h4>
                <p style="color: var(--text-secondary); line-height: 1.7; margin: 0; font-size: 0.95rem;">
                    Interactive charts show word frequency, character distribution, and message complexity. 
                    Highlighted words in red indicate spam patterns, green indicates safe patterns.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Safety Tips
    st.markdown("""
        <h3 style='color: var(--text-primary); font-size: clamp(1.25rem, 4vw, 1.5rem); font-weight: 700; margin: 2rem 0 1.5rem 0; text-align: center; letter-spacing: -0.02em;'>
            🛡️ Safety Tips
        </h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="card animate" style="height: 100%; text-align: center;">
                <div style="font-size: clamp(2rem, 5vw, 3rem); margin-bottom: 1rem;">⚠️</div>
                <h4 style="color: var(--text-primary); font-weight: 700; margin-bottom: 0.75rem; font-size: clamp(0.95rem, 2.5vw, 1.05rem);">Never Click Suspicious Links</h4>
                <p style="color: var(--text-secondary); font-size: 0.95rem; margin: 0; line-height: 1.7;">
                    Hover over links to check their destination before clicking. Be wary of shortened URLs and unexpected domains.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="card animate" style="height: 100%; text-align: center;">
                <div style="font-size: clamp(2rem, 5vw, 3rem); margin-bottom: 1rem;">🔒</div>
                <h4 style="color: var(--text-primary); font-weight: 700; margin-bottom: 0.75rem; font-size: clamp(0.95rem, 2.5vw, 1.05rem);">Protect Personal Info</h4>
                <p style="color: var(--text-secondary); font-size: 0.95rem; margin: 0; line-height: 1.7;">
                    Never share passwords, SSN, credit card details, or banking information via email or SMS messages.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="card animate" style="height: 100%; text-align: center;">
                <div style="font-size: clamp(2rem, 5vw, 3rem); margin-bottom: 1rem;">✅</div>
                <h4 style="color: var(--text-primary); font-weight: 700; margin-bottom: 0.75rem; font-size: clamp(0.95rem, 2.5vw, 1.05rem);">Verify the Source</h4>
                <p style="color: var(--text-secondary); font-size: 0.95rem; margin: 0; line-height: 1.7;">
                    If unsure about a message, contact the company directly using official contact information from their website.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Common Spam Indicators
    st.markdown("""
        <h3 style='color: var(--text-primary); font-size: clamp(1.25rem, 4vw, 1.5rem); font-weight: 700; margin: 2rem 0 1.5rem 0; text-align: center; letter-spacing: -0.02em;'>
            🚨 Common Spam Indicators
        </h3>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="card animate">
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(280px, 100%), 1fr)); gap: 1.25rem;">
                <div style="background: var(--glass-bg); padding: 1.25rem; border-radius: var(--radius-sm); border: 1px solid var(--glass-border); text-align: center;">
                    <div style="font-size: clamp(1.5rem, 4vw, 2rem); margin-bottom: 0.5rem;">🎁</div>
                    <h4 style="color: var(--text-primary); font-weight: 700; margin-bottom: 0.5rem; font-size: 1rem;">Too Good to Be True</h4>
                    <p style="color: var(--text-secondary); font-size: 0.9rem; margin: 0;">Promises of free money, prizes, or unrealistic rewards</p>
                </div>
                <div style="background: var(--glass-bg); padding: 1.25rem; border-radius: var(--radius-sm); border: 1px solid var(--glass-border); text-align: center;">
                    <div style="font-size: clamp(1.5rem, 4vw, 2rem); margin-bottom: 0.5rem;">⏰</div>
                    <h4 style="color: var(--text-primary); font-weight: 700; margin-bottom: 0.5rem; font-size: 1rem;">Urgency &amp; Pressure</h4>
                    <p style="color: var(--text-secondary); font-size: 0.9rem; margin: 0;">"Act now", "Limited time", "Urgent action required"</p>
                </div>
                <div style="background: var(--glass-bg); padding: 1.25rem; border-radius: var(--radius-sm); border: 1px solid var(--glass-border); text-align: center;">
                    <div style="font-size: clamp(1.5rem, 4vw, 2rem); margin-bottom: 0.5rem;">📝</div>
                    <h4 style="color: var(--text-primary); font-weight: 700; margin-bottom: 0.5rem; font-size: 1rem;">Poor Grammar</h4>
                    <p style="color: var(--text-secondary); font-size: 0.9rem; margin: 0;">Spelling mistakes, awkward phrasing, or unusual formatting</p>
                </div>
                <div style="background: var(--glass-bg); padding: 1.25rem; border-radius: var(--radius-sm); border: 1px solid var(--glass-border); text-align: center;">
                    <div style="font-size: clamp(1.5rem, 4vw, 2rem); margin-bottom: 0.5rem;">🔗</div>
                    <h4 style="color: var(--text-primary); font-weight: 700; margin-bottom: 0.5rem; font-size: 1rem;">Suspicious Links</h4>
                    <p style="color: var(--text-secondary); font-size: 0.9rem; margin: 0;">Shortened URLs, misspelled domains, or unexpected redirects</p>
                </div>
                <div style="background: var(--glass-bg); padding: 1.25rem; border-radius: var(--radius-sm); border: 1px solid var(--glass-border); text-align: center;">
                    <div style="font-size: clamp(1.5rem, 4vw, 2rem); margin-bottom: 0.5rem;">🔐</div>
                    <h4 style="color: var(--text-primary); font-weight: 700; margin-bottom: 0.5rem; font-size: 1rem;">Info Requests</h4>
                    <p style="color: var(--text-secondary); font-size: 0.9rem; margin: 0;">Asking for passwords, SSN, credit card numbers, or login credentials</p>
                </div>
                <div style="background: var(--glass-bg); padding: 1.25rem; border-radius: var(--radius-sm); border: 1px solid var(--glass-border); text-align: center;">
                    <div style="font-size: clamp(1.5rem, 4vw, 2rem); margin-bottom: 0.5rem;">👤</div>
                    <h4 style="color: var(--text-primary); font-weight: 700; margin-bottom: 0.5rem; font-size: 1rem;">Generic Greetings</h4>
                    <p style="color: var(--text-secondary); font-size: 0.9rem; margin: 0;">"Dear Customer" instead of your name, impersonal messages</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # FAQs using expanders instead of HTML details
    st.markdown("""
        <h3 style='color: var(--text-primary); font-size: clamp(1.25rem, 4vw, 1.5rem); font-weight: 700; margin: 2rem 0 1.5rem 0; text-align: center; letter-spacing: -0.02em;'>
            ❓ Frequently Asked Questions
        </h3>
    """, unsafe_allow_html=True)
    
    with st.expander("How accurate is the spam detector?", expanded=False):
        st.markdown("""
            <p style="color: var(--text-secondary); line-height: 1.7; margin: 0;">
                Our AI model achieves over 97% accuracy on test data, trained on millions of real-world messages. 
                However, no system is perfect - always use your judgment alongside the AI's analysis.
            </p>
        """, unsafe_allow_html=True)
    
    with st.expander("Is my data stored or shared?", expanded=False):
        st.markdown("""
            <p style="color: var(--text-secondary); line-height: 1.7; margin: 0;">
                No! Your privacy is our priority. All messages are analyzed in real-time and immediately discarded. 
                We never store, log, or share your data with anyone.
            </p>
        """, unsafe_allow_html=True)
    
    with st.expander("Can I use this for any language?", expanded=False):
        st.markdown("""
            <p style="color: var(--text-secondary); line-height: 1.7; margin: 0;">
                Currently, the model is optimized for English language messages. Support for additional 
                languages may be added in future updates.
            </p>
        """, unsafe_allow_html=True)
    
    with st.expander("What should I do if I find a false positive?", expanded=False):
        st.markdown("""
            <p style="color: var(--text-secondary); line-height: 1.7; margin: 0;">
                While rare, false positives can occur. Always review the detailed analysis to understand 
                why a message was flagged. If you believe it's legitimate, verify through official channels.
            </p>
        """, unsafe_allow_html=True)
    
    with st.expander("How do I report spam that wasn't detected?", expanded=False):
        st.markdown("""
            <p style="color: var(--text-secondary); line-height: 1.7; margin: 0;">
                If you encounter spam that our system didn't detect, please use the contact form to report it. 
                This helps us continuously improve our detection algorithms.
            </p>
        """, unsafe_allow_html=True)
    
    with st.expander("Is this tool free to use?", expanded=False):
        st.markdown("""
            <p style="color: var(--text-secondary); line-height: 1.7; margin: 0;">
                Yes! The AI Spam Detector is completely free to use. We believe everyone deserves 
                access to tools that protect them from malicious messages.
            </p>
        """, unsafe_allow_html=True)

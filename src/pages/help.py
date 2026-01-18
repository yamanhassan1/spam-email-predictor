import streamlit as st


def render_help_page():
    """Render the Help page with usage instructions."""
    st.markdown("""
        <div class="card gradient-border animate" style="text-align: center; padding: 3rem 2rem; margin-bottom: 2rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">❓</div>
            <h1 style="font-size: 3rem; font-weight: 900; margin-bottom: 1rem; color: #f8fafc;">Help & Documentation</h1>
            <div style="height: 4px; width: 100px; margin: 0 auto 1.5rem; background: linear-gradient(90deg, #3b82f6, #8b5cf6); border-radius: 999px;"></div>
            <p style="color: #cbd5e1; font-size: 1.1rem;">Everything you need to know to use the AI Spam Detector</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Quick Start Guide
    st.markdown("### 🚀 Quick Start Guide")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="card animate" style="background: rgba(59, 130, 246, 0.08); border-left: 4px solid #3b82f6; height: 100%;">
                <div style="font-size: 2.5rem; text-align: center; margin-bottom: 1rem;">1️⃣</div>
                <h4 style="color: #60a5fa; font-size: 1.2rem; font-weight: 700; margin-bottom: 1rem; text-align: center;">Enter Your Message</h4>
                <p style="color: #cbd5e1; line-height: 1.8; margin: 0; text-align: center;">
                    Paste any email or SMS message into the text area on the Home page.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="card animate" style="background: rgba(139, 92, 246, 0.08); border-left: 4px solid #8b5cf6; height: 100%; animation-delay: 0.1s;">
                <div style="font-size: 2.5rem; text-align: center; margin-bottom: 1rem;">2️⃣</div>
                <h4 style="color: #a78bfa; font-size: 1.2rem; font-weight: 700; margin-bottom: 1rem; text-align: center;">Click Analyze</h4>
                <p style="color: #cbd5e1; line-height: 1.8; margin: 0; text-align: center;">
                    Click the "🔍 Analyze Message Now" button to process your message with AI.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="card animate" style="background: rgba(16, 185, 129, 0.08); border-left: 4px solid #10b981; height: 100%; animation-delay: 0.2s;">
                <div style="font-size: 2.5rem; text-align: center; margin-bottom: 1rem;">3️⃣</div>
                <h4 style="color: #34d399; font-size: 1.2rem; font-weight: 700; margin-bottom: 1rem; text-align: center;">Review Results</h4>
                <p style="color: #cbd5e1; line-height: 1.8; margin: 0; text-align: center;">
                    Get instant results with confidence scores and detailed analysis.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Understanding Results
    st.markdown("### 💡 Understanding Results")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="card animate" style="height: 100%;">
                <div style="font-size: 2rem; margin-bottom: 0.75rem; text-align: center;">🎯</div>
                <h4 style="color: #f8fafc; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.75rem; text-align: center;">
                    Confidence Score
                </h4>
                <p style="color: #cbd5e1; line-height: 1.7; margin: 0;">
                    This percentage indicates how confident the AI is in its classification. 
                    Higher percentages (above 80%) indicate strong confidence.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="card animate" style="height: 100%; animation-delay: 0.1s;">
                <div style="font-size: 2rem; margin-bottom: 0.75rem; text-align: center;">🔍</div>
                <h4 style="color: #f8fafc; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.75rem; text-align: center;">
                    Pattern Analysis
                </h4>
                <p style="color: #cbd5e1; line-height: 1.7; margin: 0;">
                    See which spam indicators were detected and compare spam vs. safe indicators in your message.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="card animate" style="height: 100%; animation-delay: 0.2s;">
                <div style="font-size: 2rem; margin-bottom: 0.75rem; text-align: center;">📊</div>
                <h4 style="color: #f8fafc; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.75rem; text-align: center;">
                    Visualizations
                </h4>
                <p style="color: #cbd5e1; line-height: 1.7; margin: 0;">
                    Interactive charts show word frequency and message complexity with color-coded indicators.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Safety Tips
    st.markdown("### 🛡️ Safety Tips")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="card animate" style="background: linear-gradient(135deg, rgba(239, 68, 68, 0.08), rgba(220, 38, 38, 0.04)); border-left: 4px solid #ef4444; height: 100%;">
                <div style="font-size: 2rem; margin-bottom: 0.75rem; text-align: center;">⚠️</div>
                <h4 style="color: #fecdd3; font-weight: 700; margin-bottom: 0.5rem; text-align: center;">Never Click Suspicious Links</h4>
                <p style="color: #fde2e4; font-size: 0.95rem; margin: 0;">
                    Hover over links to check their destination before clicking. Be wary of shortened URLs.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="card animate" style="background: linear-gradient(135deg, rgba(251, 191, 36, 0.08), rgba(245, 158, 11, 0.04)); border-left: 4px solid #fbbf24; height: 100%; animation-delay: 0.1s;">
                <div style="font-size: 2rem; margin-bottom: 0.75rem; text-align: center;">🔒</div>
                <h4 style="color: #fef3c7; font-weight: 700; margin-bottom: 0.5rem; text-align: center;">Protect Personal Info</h4>
                <p style="color: #fef9e7; font-size: 0.95rem; margin: 0;">
                    Never share passwords, SSN, or credit card details via email or SMS messages.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="card animate" style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.08), rgba(37, 99, 235, 0.04)); border-left: 4px solid #3b82f6; height: 100%; animation-delay: 0.2s;">
                <div style="font-size: 2rem; margin-bottom: 0.75rem; text-align: center;">✅</div>
                <h4 style="color: #dbeafe; font-weight: 700; margin-bottom: 0.5rem; text-align: center;">Verify the Source</h4>
                <p style="color: #eff6ff; font-size: 0.95rem; margin: 0;">
                    If unsure, contact the company directly using official contact information.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # FAQ Section
    st.markdown("### ❓ Frequently Asked Questions")
    
    with st.expander("How accurate is the spam detector?"):
        st.markdown("""
            <p style="color: #cbd5e1; line-height: 1.7;">
                Our AI model achieves over 97% accuracy on test data, trained on millions of real-world messages. 
                However, no system is perfect - always use your judgment alongside the AI's analysis.
            </p>
        """, unsafe_allow_html=True)
    
    with st.expander("Is my data stored or shared?"):
        st.markdown("""
            <p style="color: #cbd5e1; line-height: 1.7;">
                No! Your privacy is our priority. All messages are analyzed in real-time and immediately discarded. 
                We never store, log, or share your data with anyone.
            </p>
        """, unsafe_allow_html=True)
    
    with st.expander("Can I use this for any language?"):
        st.markdown("""
            <p style="color: #cbd5e1; line-height: 1.7;">
                Currently, the model is optimized for English language messages. Support for additional 
                languages may be added in future updates.
            </p>
        """, unsafe_allow_html=True)
    
    with st.expander("What should I do if I find a false positive?"):
        st.markdown("""
            <p style="color: #cbd5e1; line-height: 1.7;">
                While rare, false positives can occur. Always review the detailed analysis to understand 
                why a message was flagged. If you believe it's legitimate, verify through official channels.
            </p>
        """, unsafe_allow_html=True)
        # INSERT_YOUR_CODE
    with st.expander("How can I improve spam detection accuracy?"):
        st.markdown("""
            <p style="color: #cbd5e1; line-height: 1.7;">
                For best results, ensure your messages are clearly written and avoid excessive use of emojis or special characters. 
                You can also update the model with new examples or provide user feedback to help us improve future versions.
            </p>
        """, unsafe_allow_html=True)

    with st.expander("Who do I contact for support or to suggest a feature?"):
        st.markdown("""
            <p style="color: #cbd5e1; line-height: 1.7;">
                If you need assistance, encounter issues, or have ideas for new features, visit the <a href="/📧 Contact" style="color: #60a5fa; text-decoration: underline;">Contact</a> page. 
                Our team is happy to help and looks forward to hearing your feedback!
            </p>
        """, unsafe_allow_html=True)
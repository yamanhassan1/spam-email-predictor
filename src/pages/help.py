import streamlit as st


def render_help_page():
    """Render the Help page with usage instructions."""
    st.markdown("""
        <div class="card gradient-border animate" style="text-align: center; padding: 3rem 2rem; margin-bottom: 2rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">❓</div>
            <h1 style="font-size: 3rem; font-weight: 900; margin-bottom: 1rem;">Help & Documentation</h1>
            <div style="height: 4px; width: 100px; margin: 0 auto 1.5rem; background: linear-gradient(90deg, var(--blue-400), var(--purple-400)); border-radius: 999px;"></div>
            <p style="color: #cbd5e1; font-size: 1.1rem;">Everything you need to know to use the AI Spam Detector</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Quick Start Guide
    st.markdown("""
        <h3 style='color: #f8fafc; font-size: 1.5rem; font-weight: 700; margin: 2rem 0 1.5rem 0; letter-spacing: -0.02em;'>
            🚀 Quick Start Guide
        </h3>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="card animate">
            <div style="display: grid; gap: 1.5rem;">
                <div style="background: rgba(59, 130, 246, 0.05); padding: 1.5rem; border-radius: 16px; border-left: 4px solid var(--blue-400);">
                    <h4 style="color: #60a5fa; font-size: 1.2rem; font-weight: 700; margin-bottom: 1rem;">Step 1: Enter Your Message</h4>
                    <p style="color: #cbd5e1; line-height: 1.8; margin: 0;">
                        Navigate to the Home page and paste any email or SMS message into the text area. 
                        You can analyze messages from any source - emails, text messages, or any text content.
                    </p>
                </div>
                
                <div style="background: rgba(139, 92, 246, 0.05); padding: 1.5rem; border-radius: 16px; border-left: 4px solid var(--purple-400);">
                    <h4 style="color: #a78bfa; font-size: 1.2rem; font-weight: 700; margin-bottom: 1rem;">Step 2: Click Analyze</h4>
                    <p style="color: #cbd5e1; line-height: 1.8; margin: 0;">
                        Click the "🔍 Analyze Message Now" button to process your message. 
                        The AI will analyze the content, patterns, and characteristics in real-time.
                    </p>
                </div>
                
                <div style="background: rgba(16, 185, 129, 0.05); padding: 1.5rem; border-radius: 16px; border-left: 4px solid var(--green-400);">
                    <h4 style="color: #34d399; font-size: 1.2rem; font-weight: 700; margin-bottom: 1rem;">Step 3: Review Results</h4>
                    <p style="color: #cbd5e1; line-height: 1.8; margin: 0;">
                        Get instant results with confidence scores, detailed pattern analysis, visual charts, 
                        and highlighted spam indicators to help you make informed decisions.
                    </p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Understanding Results
    st.markdown("""
        <h3 style='color: #f8fafc; font-size: 1.5rem; font-weight: 700; margin: 2rem 0 1.5rem 0; letter-spacing: -0.02em;'>
            💡 Understanding Results
        </h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="card animate" style="height: 100%;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🎯</div>
                <h4 style="color: #f8fafc; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.75rem;">
                    Confidence Score
                </h4>
                <p style="color: #cbd5e1; line-height: 1.7; margin: 0; font-size: 0.95rem;">
                    This percentage indicates how confident the AI is in its classification. 
                    Higher percentages (above 80%) indicate strong confidence in the result.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="card animate" style="height: 100%;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🔍</div>
                <h4 style="color: #f8fafc; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.75rem;">
                    Pattern Analysis
                </h4>
                <p style="color: #cbd5e1; line-height: 1.7; margin: 0; font-size: 0.95rem;">
                    See which spam indicators were detected (urgent language, suspicious URLs, etc.) 
                    and compare spam vs. safe indicators in your message.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="card animate" style="height: 100%;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
                <h4 style="color: #f8fafc; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.75rem;">
                    Visualizations
                </h4>
                <p style="color: #cbd5e1; line-height: 1.7; margin: 0; font-size: 0.95rem;">
                    Interactive charts show word frequency, character distribution, and message complexity. 
                    Highlighted words in red indicate spam patterns, green indicates safe patterns.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Safety Tips
    st.markdown("""
        <h3 style='color: #f8fafc; font-size: 1.5rem; font-weight: 700; margin: 2rem 0 1.5rem 0; letter-spacing: -0.02em;'>
            🛡️ Safety Tips
        </h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="card animate" style="height: 100%;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">⚠️</div>
                <h4 style="color: #fecdd3; font-weight: 700; margin-bottom: 0.75rem; font-size: 1.05rem;">Never Click Suspicious Links</h4>
                <p style="color: #cbd5e1; font-size: 0.95rem; margin: 0; line-height: 1.7;">
                    Hover over links to check their destination before clicking. Be wary of shortened URLs and unexpected domains.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="card animate" style="height: 100%;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🔒</div>
                <h4 style="color: #fef3c7; font-weight: 700; margin-bottom: 0.75rem; font-size: 1.05rem;">Protect Personal Info</h4>
                <p style="color: #cbd5e1; font-size: 0.95rem; margin: 0; line-height: 1.7;">
                    Never share passwords, SSN, credit card details, or banking information via email or SMS messages.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="card animate" style="height: 100%;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">✅</div>
                <h4 style="color: #dbeafe; font-weight: 700; margin-bottom: 0.75rem; font-size: 1.05rem;">Verify the Source</h4>
                <p style="color: #cbd5e1; font-size: 0.95rem; margin: 0; line-height: 1.7;">
                    If unsure about a message, contact the company directly using official contact information from their website.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Common Spam Indicators
    st.markdown("""
        <h3 style='color: #f8fafc; font-size: 1.5rem; font-weight: 700; margin: 2rem 0 1.5rem 0; letter-spacing: -0.02em;'>
            🚨 Common Spam Indicators
        </h3>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="card gradient-border animate">
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.25rem;">
                <div style="background: rgba(255, 255, 255, 0.03); padding: 1.25rem; border-radius: 12px;">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">🎁</div>
                    <h4 style="color: #fecdd3; font-weight: 700; margin-bottom: 0.5rem; font-size: 1rem;">Too Good to Be True</h4>
                    <p style="color: #cbd5e1; font-size: 0.9rem; margin: 0;">Promises of free money, prizes, or unrealistic rewards</p>
                </div>
                <div style="background: rgba(255, 255, 255, 0.03); padding: 1.25rem; border-radius: 12px;">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">⏰</div>
                    <h4 style="color: #fecdd3; font-weight: 700; margin-bottom: 0.5rem; font-size: 1rem;">Urgency & Pressure</h4>
                    <p style="color: #cbd5e1; font-size: 0.9rem; margin: 0;">"Act now", "Limited time", "Urgent action required"</p>
                </div>
                <div style="background: rgba(255, 255, 255, 0.03); padding: 1.25rem; border-radius: 12px;">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">📝</div>
                    <h4 style="color: #fecdd3; font-weight: 700; margin-bottom: 0.5rem; font-size: 1rem;">Poor Grammar</h4>
                    <p style="color: #cbd5e1; font-size: 0.9rem; margin: 0;">Spelling mistakes, awkward phrasing, or unusual formatting</p>
                </div>
                <div style="background: rgba(255, 255, 255, 0.03); padding: 1.25rem; border-radius: 12px;">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔗</div>
                    <h4 style="color: #fecdd3; font-weight: 700; margin-bottom: 0.5rem; font-size: 1rem;">Suspicious Links</h4>
                    <p style="color: #cbd5e1; font-size: 0.9rem; margin: 0;">Shortened URLs, misspelled domains, or unexpected redirects</p>
                </div>
                <div style="background: rgba(255, 255, 255, 0.03); padding: 1.25rem; border-radius: 12px;">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔐</div>
                    <h4 style="color: #fecdd3; font-weight: 700; margin-bottom: 0.5rem; font-size: 1rem;">Info Requests</h4>
                    <p style="color: #cbd5e1; font-size: 0.9rem; margin: 0;">Asking for passwords, SSN, credit card numbers, or login credentials</p>
                </div>
                <div style="background: rgba(255, 255, 255, 0.03); padding: 1.25rem; border-radius: 12px;">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">👤</div>
                    <h4 style="color: #fecdd3; font-weight: 700; margin-bottom: 0.5rem; font-size: 1rem;">Generic Greetings</h4>
                    <p style="color: #cbd5e1; font-size: 0.9rem; margin: 0;">"Dear Customer" instead of your name, impersonal messages</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # FAQs
    st.markdown("""
        <h3 style='color: #f8fafc; font-size: 1.5rem; font-weight: 700; margin: 2rem 0 1.5rem 0; letter-spacing: -0.02em;'>
            ❓ Frequently Asked Questions
        </h3>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="card gradient-border animate">
            <div style="display: grid; gap: 1.25rem;">
                <details style="background: rgba(255, 255, 255, 0.03); padding: 1.25rem; border-radius: 12px; cursor: pointer;">
                    <summary style="color: #60a5fa; font-weight: 700; font-size: 1.1rem; margin-bottom: 0.75rem; cursor: pointer;">
                        How accurate is the spam detector?
                    </summary>
                    <p style="color: #cbd5e1; line-height: 1.7; margin-top: 0.75rem;">
                        Our AI model achieves over 97% accuracy on test data, trained on millions of real-world messages. 
                        However, no system is perfect - always use your judgment alongside the AI's analysis.
                    </p>
                </details>
                
                <details style="background: rgba(255, 255, 255, 0.03); padding: 1.25rem; border-radius: 12px; cursor: pointer;">
                    <summary style="color: #60a5fa; font-weight: 700; font-size: 1.1rem; margin-bottom: 0.75rem; cursor: pointer;">
                        Is my data stored or shared?
                    </summary>
                    <p style="color: #cbd5e1; line-height: 1.7; margin-top: 0.75rem;">
                        No! Your privacy is our priority. All messages are analyzed in real-time and immediately discarded. 
                        We never store, log, or share your data with anyone.
                    </p>
                </details>
                
                <details style="background: rgba(255, 255, 255, 0.03); padding: 1.25rem; border-radius: 12px; cursor: pointer;">
                    <summary style="color: #60a5fa; font-weight: 700; font-size: 1.1rem; margin-bottom: 0.75rem; cursor: pointer;">
                        Can I use this for any language?
                    </summary>
                    <p style="color: #cbd5e1; line-height: 1.7; margin-top: 0.75rem;">
                        Currently, the model is optimized for English language messages. Support for additional 
                        languages may be added in future updates.
                    </p>
                </details>
                
                <details style="background: rgba(255, 255, 255, 0.03); padding: 1.25rem; border-radius: 12px; cursor: pointer;">
                    <summary style="color: #60a5fa; font-weight: 700; font-size: 1.1rem; margin-bottom: 0.75rem; cursor: pointer;">
                        What should I do if I find a false positive?
                    </summary>
                    <p style="color: #cbd5e1; line-height: 1.7; margin-top: 0.75rem;">
                        While rare, false positives can occur. Always review the detailed analysis to understand 
                        why a message was flagged. If you believe it's legitimate, verify through official channels.
                    </p>
                </details>
                
                <details style="background: rgba(255, 255, 255, 0.03); padding: 1.25rem; border-radius: 12px; cursor: pointer;">
                    <summary style="color: #60a5fa; font-weight: 700; font-size: 1.1rem; margin-bottom: 0.75rem; cursor: pointer;">
                        How do I report spam that wasn't detected?
                    </summary>
                    <p style="color: #cbd5e1; line-height: 1.7; margin-top: 0.75rem;">
                        If you encounter spam that our system didn't detect, please use the contact form to report it. 
                        This helps us continuously improve our detection algorithms.
                    </p>
                </details>
                
                <details style="background: rgba(255, 255, 255, 0.03); padding: 1.25rem; border-radius: 12px; cursor: pointer;">
                    <summary style="color: #60a5fa; font-weight: 700; font-size: 1.1rem; margin-bottom: 0.75rem; cursor: pointer;">
                        Is this tool free to use?
                    </summary>
                    <p style="color: #cbd5e1; line-height: 1.7; margin-top: 0.75rem;">
                        Yes! The AI Spam Detector is completely free to use. We believe everyone deserves 
                        access to tools that protect them from malicious messages.
                    </p>
                </details>
            </div>
        </div>
    """, unsafe_allow_html=True)
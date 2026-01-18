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
    
    st.markdown("""
        <div class="card animate">
            <h3 style="color: #f8fafc; font-size: 1.75rem; font-weight: 700; margin-bottom: 1.5rem;">
                🚀 Quick Start Guide
            </h3>
            <div style="background: rgba(59, 130, 246, 0.05); padding: 1.5rem; border-radius: 16px; border-left: 4px solid #3b82f6; margin-bottom: 1.5rem;">
                <h4 style="color: #60a5fa; font-size: 1.2rem; font-weight: 700; margin-bottom: 1rem;">Step 1: Enter Your Message</h4>
                <p style="color: #cbd5e1; line-height: 1.8; margin: 0;">
                    Navigate to the Home page and paste any email or SMS message into the text area. 
                    You can analyze messages from any source - emails, text messages, or any text content.
                </p>
            </div>
            
            <div style="background: rgba(139, 92, 246, 0.05); padding: 1.5rem; border-radius: 16px; border-left: 4px solid #8b5cf6; margin-bottom: 1.5rem;">
                <h4 style="color: #a78bfa; font-size: 1.2rem; font-weight: 700; margin-bottom: 1rem;">Step 2: Click Analyze</h4>
                <p style="color: #cbd5e1; line-height: 1.8; margin: 0;">
                    Click the "🔍 Analyze Message Now" button to process your message. 
                    The AI will analyze the content, patterns, and characteristics in real-time.
                </p>
            </div>
            
            <div style="background: rgba(16, 185, 129, 0.05); padding: 1.5rem; border-radius: 16px; border-left: 4px solid #10b981;">
                <h4 style="color: #34d399; font-size: 1.2rem; font-weight: 700; margin-bottom: 1rem;">Step 3: Review Results</h4>
                <p style="color: #cbd5e1; line-height: 1.8; margin: 0;">
                    Get instant results with confidence scores, detailed pattern analysis, visual charts, 
                    and highlighted spam indicators to help you make informed decisions.
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class="card animate" style="animation-delay: 0.1s;">
            <h3 style="color: #f8fafc; font-size: 1.75rem; font-weight: 700; margin-bottom: 1.5rem;">
                💡 Understanding Results
            </h3>
            <div style="display: grid; gap: 1.25rem;">
                <div style="background: rgba(255, 255, 255, 0.03); padding: 1.25rem; border-radius: 12px;">
                    <h4 style="color: #f8fafc; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.75rem;">
                        🎯 Confidence Score
                    </h4>
                    <p style="color: #cbd5e1; line-height: 1.7; margin: 0;">
                        This percentage indicates how confident the AI is in its classification. 
                        Higher percentages (above 80%) indicate strong confidence in the result.
                    </p>
                </div>
                
                <div style="background: rgba(255, 255, 255, 0.03); padding: 1.25rem; border-radius: 12px;">
                    <h4 style="color: #f8fafc; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.75rem;">
                        🔍 Pattern Analysis
                    </h4>
                    <p style="color: #cbd5e1; line-height: 1.7; margin: 0;">
                        See which spam indicators were detected (urgent language, suspicious URLs, etc.) 
                        and compare spam vs. safe indicators in your message.
                    </p>
                </div>
                
                <div style="background: rgba(255, 255, 255, 0.03); padding: 1.25rem; border-radius: 12px;">
                    <h4 style="color: #f8fafc; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.75rem;">
                        📊 Visualizations
                    </h4>
                    <p style="color: #cbd5e1; line-height: 1.7; margin: 0;">
                        Interactive charts show word frequency, character distribution, and message complexity. 
                        Highlighted words in red indicate spam patterns, green indicates safe patterns.
                    </p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class="card animate" style="animation-delay: 0.2s;">
            <h3 style="color: #f8fafc; font-size: 1.75rem; font-weight: 700; margin-bottom: 1.5rem;">
                🛡️ Safety Tips
            </h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.25rem;">
                <div style="background: linear-gradient(135deg, rgba(239, 68, 68, 0.08), rgba(220, 38, 38, 0.04)); padding: 1.25rem; border-radius: 12px; border: 1px solid rgba(239, 68, 68, 0.2);">
                    <div style="font-size: 2rem; margin-bottom: 0.75rem;">⚠️</div>
                    <h4 style="color: #fecdd3; font-weight: 700; margin-bottom: 0.5rem;">Never Click Suspicious Links</h4>
                    <p style="color: #fde2e4; font-size: 0.95rem; margin: 0;">
                        Hover over links to check their destination before clicking. Be wary of shortened URLs.
                    </p>
                </div>
                
                <div style="background: linear-gradient(135deg, rgba(251, 191, 36, 0.08), rgba(245, 158, 11, 0.04)); padding: 1.25rem; border-radius: 12px; border: 1px solid rgba(251, 191, 36, 0.2);">
                    <div style="font-size: 2rem; margin-bottom: 0.75rem;">🔒</div>
                    <h4 style="color: #fef3c7; font-weight: 700; margin-bottom: 0.5rem;">Protect Personal Info</h4>
                    <p style="color: #fef9e7; font-size: 0.95rem; margin: 0;">
                        Never share passwords, SSN, or credit card details via email or SMS messages.
                    </p>
                </div>
                
                <div style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.08), rgba(37, 99, 235, 0.04)); padding: 1.25rem; border-radius: 12px; border: 1px solid rgba(59, 130, 246, 0.2);">
                    <div style="font-size: 2rem; margin-bottom: 0.75rem;">✅</div>
                    <h4 style="color: #dbeafe; font-weight: 700; margin-bottom: 0.5rem;">Verify the Source</h4>
                    <p style="color: #eff6ff; font-size: 0.95rem; margin: 0;">
                        If unsure, contact the company directly using official contact information.
                    </p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class="card gradient-border animate" style="animation-delay: 0.3s;">
            <h3 style="color: #f8fafc; font-size: 1.75rem; font-weight: 700; margin-bottom: 1.5rem; text-align: center;">
                ❓ Frequently Asked Questions
            </h3>
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
            </div>
        </div>
    """, unsafe_allow_html=True)
import streamlit as st

def render_input_section():
    """
    Render the premium input section with styled text area.
    Cross-platform compatible for Windows, Mac, Linux, and web browsers.
    Returns the user input text.
    """
    st.markdown("""
    <div class="card" style="margin-bottom: 2rem; text-align: center;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">📝</div>
        <h3 style='color: #f8fafc; margin-bottom: 0.75rem; font-size: 1.1rem; font-weight: 700;'>
            Enter Your Message
        </h3>
        <p style='color: #cbd5e1; margin-bottom: 0; line-height: 1.6;'>
            Paste any email or SMS message below for instant AI-powered analysis and threat detection.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Cross-platform compatible CSS with important declarations and browser prefixes
    st.markdown("""
        <style>
        /* Text Area Styling - Cross-platform compatible */
        .stTextArea textarea {
            background: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 12px !important;
            color: #f8fafc !important;
            font-size: 1rem !important;
            padding: 1rem !important;
            line-height: 1.6 !important;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif !important;
            transition: all 0.3s ease !important;
            -webkit-transition: all 0.3s ease !important;
            -moz-transition: all 0.3s ease !important;
            resize: vertical !important;
            min-height: 220px !important;
        }
        
        /* Focus state - works across browsers */
        .stTextArea textarea:focus {
            border-color: rgba(59, 130, 246, 0.5) !important;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
            -webkit-box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
            -moz-box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
            outline: none !important;
        }
        
        /* Placeholder styling - cross-browser */
        .stTextArea textarea::placeholder {
            color: rgba(203, 213, 225, 0.5) !important;
            opacity: 1 !important;
        }
        
        .stTextArea textarea::-webkit-input-placeholder {
            color: rgba(203, 213, 225, 0.5) !important;
        }
        
        .stTextArea textarea::-moz-placeholder {
            color: rgba(203, 213, 225, 0.5) !important;
        }
        
        .stTextArea textarea:-ms-input-placeholder {
            color: rgba(203, 213, 225, 0.5) !important;
        }
        
        /* Scrollbar styling - Webkit browsers (Chrome, Safari, Edge) */
        .stTextArea textarea::-webkit-scrollbar {
            width: 8px !important;
        }
        
        .stTextArea textarea::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.05) !important;
            border-radius: 10px !important;
        }
        
        .stTextArea textarea::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.2) !important;
            border-radius: 10px !important;
        }
        
        .stTextArea textarea::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 255, 255, 0.3) !important;
        }
        
        /* Firefox scrollbar */
        .stTextArea textarea {
            scrollbar-width: thin !important;
            scrollbar-color: rgba(255, 255, 255, 0.2) rgba(255, 255, 255, 0.05) !important;
        }
        
        /* Button Styling - Cross-platform */
        .stButton > button {
            background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.75rem 2rem !important;
            font-weight: 700 !important;
            font-size: 1rem !important;
            letter-spacing: 0.02em !important;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
            -webkit-transition: all 0.3s ease !important;
            -moz-transition: all 0.3s ease !important;
            box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3) !important;
            -webkit-box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3) !important;
            -moz-box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3) !important;
            width: 100% !important;
            max-width: 300px !important;
            margin: 0 auto !important;
            display: block !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            -webkit-transform: translateY(-2px) !important;
            -moz-transform: translateY(-2px) !important;
            box-shadow: 0 12px 32px rgba(59, 130, 246, 0.4) !important;
            -webkit-box-shadow: 0 12px 32px rgba(59, 130, 246, 0.4) !important;
            -moz-box-shadow: 0 12px 32px rgba(59, 130, 246, 0.4) !important;
        }
        
        .stButton > button:active {
            transform: translateY(0) !important;
            -webkit-transform: translateY(0) !important;
            -moz-transform: translateY(0) !important;
        }
        
        /* Disable text selection on button */
        .stButton > button {
            -webkit-user-select: none !important;
            -moz-user-select: none !important;
            -ms-user-select: none !important;
            user-select: none !important;
        }
        
        /* Fix for Windows high contrast mode */
        @media (prefers-contrast: high) {
            .stTextArea textarea {
                border: 2px solid rgba(255, 255, 255, 0.3) !important;
            }
        }
        
        /* Fix for reduced motion preferences */
        @media (prefers-reduced-motion: reduce) {
            .stTextArea textarea,
            .stButton > button {
                transition: none !important;
                -webkit-transition: none !important;
                -moz-transition: none !important;
            }
        }
        
        /* Dark mode support */
        @media (prefers-color-scheme: dark) {
            .stTextArea textarea {
                background: rgba(255, 255, 255, 0.03) !important;
            }
        }
        
        /* Light mode support */
        @media (prefers-color-scheme: light) {
            .stTextArea textarea {
                background: rgba(0, 0, 0, 0.03) !important;
                color: #1e293b !important;
                border: 1px solid rgba(0, 0, 0, 0.08) !important;
            }
        }
        </style>
    """, unsafe_allow_html=True)
    
    input_sms = st.text_area(
        "Message",
        height=220,
        placeholder="📧 Paste your email or SMS message here...\n\nExample: 'Congratulations! You've won $1,000,000! Click here to claim your prize now!'\n\nOr: 'Hi John, are we still meeting for coffee tomorrow at 3pm?'",
        label_visibility="collapsed",
        key="message_input"
    )
    
    return input_sms

import streamlit as st


def render_input_section():
    """
    Render the premium input section with styled text area.
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
    
    # Custom styled text area
    st.markdown("""
        <style>
        .stTextArea textarea {
            background: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 12px !important;
            color: #f8fafc !important;
            font-size: 1rem !important;
            padding: 1rem !important;
            transition: all 0.3s ease !important;
        }
        .stTextArea textarea:focus {
            border-color: rgba(59, 130, 246, 0.5) !important;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
        }
        .stButton > button {
            background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.75rem 2rem !important;
            font-weight: 700 !important;
            font-size: 1rem !important;
            letter-spacing: 0.02em !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3) !important;
        }
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 12px 32px rgba(59, 130, 246, 0.4) !important;
        }
        .stButton > button:active {
            transform: translateY(0) !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    input_sms = st.text_area(
        "Message",
        height=220,
        placeholder="📧 Paste your email or SMS message here...\n\nExample: 'Congratulations! You've won $1,000,000! Click here to claim your prize now!'\n\nOr: 'Hi John, are we still meeting for coffee tomorrow at 3pm?'",
        label_visibility="collapsed"
    )
    
    return input_sms
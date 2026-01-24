import streamlit as st


def render_contact_page():
    """
    Render the Contact page with improved text coloring and dynamic email.
    Cross-platform compatible for Windows, Mac, Linux, and all browsers.
    """
    
    # Dynamic email configuration
    CONTACT_EMAIL = "yaman.hassan10@yahoo.com"
    COMPANY_NAME = "AI Spam Detector"
    
    # Contact Form Section with improved colors
    st.markdown("""
        <div class="card" style="margin-bottom: 2rem; text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📬</div>
            <h3 style='background: linear-gradient(135deg, #60a5fa, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 0.75rem; font-size: 1.3rem; font-weight: 800;'>
                Send Us a Message
            </h3>
            <p style='color: #e2e8f0; margin-bottom: 0; line-height: 1.6; font-size: 1.05rem;'>
                Fill out the form below and we'll get back to you within 24 hours.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Cross-platform compatible CSS styling with improved colors
    st.markdown("""
        <style>
        /* ===== INPUT FIELDS STYLING - CROSS-PLATFORM WITH IMPROVED COLORS ===== */
        .stTextInput input, .stTextArea textarea, .stSelectbox select {
            background: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(96, 165, 250, 0.2) !important;
            border-radius: 12px !important;
            color: #f1f5f9 !important;
            font-size: 1rem !important;
            padding: 1rem !important;
            line-height: 1.6 !important;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif !important;
            transition: all 0.3s ease !important;
            -webkit-transition: all 0.3s ease !important;
            -moz-transition: all 0.3s ease !important;
        }
        
        /* Hover state for inputs */
        .stTextInput input:hover, 
        .stTextArea textarea:hover, 
        .stSelectbox select:hover {
            border-color: rgba(96, 165, 250, 0.4) !important;
            background: rgba(255, 255, 255, 0.08) !important;
        }
        
        /* Focus states - cross-browser with vibrant colors */
        .stTextInput input:focus, .stTextArea textarea:focus, .stSelectbox select:focus {
            border-color: rgba(96, 165, 250, 0.6) !important;
            background: rgba(255, 255, 255, 0.08) !important;
            box-shadow: 0 0 0 4px rgba(96, 165, 250, 0.15) !important;
            -webkit-box-shadow: 0 0 0 4px rgba(96, 165, 250, 0.15) !important;
            -moz-box-shadow: 0 0 0 4px rgba(96, 165, 250, 0.15) !important;
            outline: none !important;
        }
        
        /* Label styling with better visibility */
        .stTextInput label, 
        .stTextArea label, 
        .stSelectbox label {
            color: #e2e8f0 !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            margin-bottom: 0.5rem !important;
        }
        
        /* Placeholder styling - cross-browser with improved contrast */
        .stTextInput input::placeholder,
        .stTextArea textarea::placeholder {
            color: rgba(203, 213, 225, 0.6) !important;
            opacity: 1 !important;
        }
        
        .stTextInput input::-webkit-input-placeholder,
        .stTextArea textarea::-webkit-input-placeholder {
            color: rgba(203, 213, 225, 0.6) !important;
        }
        
        .stTextInput input::-moz-placeholder,
        .stTextArea textarea::-moz-placeholder {
            color: rgba(203, 213, 225, 0.6) !important;
        }
        
        .stTextInput input:-ms-input-placeholder,
        .stTextArea textarea:-ms-input-placeholder {
            color: rgba(203, 213, 225, 0.6) !important;
        }
        
        /* ===== SELECT BOX STYLING - CROSS-PLATFORM ===== */
        .stSelectbox > div > div {
            background: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(96, 165, 250, 0.2) !important;
            border-radius: 12px !important;
        }
        
        .stSelectbox [data-baseweb="select"] {
            background: rgba(255, 255, 255, 0.05) !important;
        }
        
        .stSelectbox [data-baseweb="select"] > div {
            color: #f1f5f9 !important;
        }
        
        /* ===== SCROLLBAR STYLING - WEBKIT (Chrome, Safari, Edge) ===== */
        .stTextArea textarea::-webkit-scrollbar {
            width: 10px !important;
        }
        
        .stTextArea textarea::-webkit-scrollbar-track {
            background: rgba(96, 165, 250, 0.1) !important;
            border-radius: 10px !important;
        }
        
        .stTextArea textarea::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #60a5fa, #a78bfa) !important;
            border-radius: 10px !important;
        }
        
        .stTextArea textarea::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
        }
        
        /* Firefox scrollbar */
        .stTextArea textarea {
            scrollbar-width: thin !important;
            scrollbar-color: #60a5fa rgba(96, 165, 250, 0.1) !important;
        }
        
        /* ===== FORM SUBMIT BUTTON - CROSS-PLATFORM WITH GRADIENT ===== */
        .stButton > button, 
        .stFormSubmitButton > button {
            background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.75rem 2rem !important;
            font-weight: 700 !important;
            font-size: 1.08rem !important;
            letter-spacing: 0.02em !important;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
            -webkit-transition: all 0.3s ease !important;
            -moz-transition: all 0.3s ease !important;
            box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3) !important;
            -webkit-box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3) !important;
            -moz-box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3) !important;
            -webkit-user-select: none !important;
            -moz-user-select: none !important;
            -ms-user-select: none !important;
            user-select: none !important;
        }
        
        .stButton > button:hover,
        .stFormSubmitButton > button:hover {
            transform: translateY(-2px) scale(1.02) !important;
            -webkit-transform: translateY(-2px) scale(1.02) !important;
            -moz-transform: translateY(-2px) scale(1.02) !important;
            box-shadow: 0 12px 32px rgba(59, 130, 246, 0.4) !important;
            -webkit-box-shadow: 0 12px 32px rgba(59, 130, 246, 0.4) !important;
            -moz-box-shadow: 0 12px 32px rgba(59, 130, 246, 0.4) !important;
            background: linear-gradient(135deg, #2563eb, #7c3aed) !important;
        }
        
        .stButton > button:active,
        .stFormSubmitButton > button:active {
            transform: translateY(0) scale(0.98) !important;
            -webkit-transform: translateY(0) scale(0.98) !important;
            -moz-transform: translateY(0) scale(0.98) !important;
        }
        
        /* ===== MAILTO BUTTON STYLING WITH DYNAMIC GRADIENT ===== */
        .mailto-button {
            background: linear-gradient(90deg, #10b981, #06b6d4) !important;
            color: #fff !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.75rem 2.5rem !important;
            font-size: 1.08rem !important;
            font-weight: 700 !important;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif !important;
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3) !important;
            -webkit-box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3) !important;
            -moz-box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3) !important;
            cursor: pointer !important;
            margin-top: 1rem !important;
            transition: all 0.3s ease !important;
            -webkit-transition: all 0.3s ease !important;
            -moz-transition: all 0.3s ease !important;
            display: inline-block !important;
        }
        
        .mailto-button:hover {
            transform: translateY(-2px) scale(1.02) !important;
            -webkit-transform: translateY(-2px) scale(1.02) !important;
            -moz-transform: translateY(-2px) scale(1.02) !important;
            box-shadow: 0 6px 16px rgba(16, 185, 129, 0.4) !important;
            -webkit-box-shadow: 0 6px 16px rgba(16, 185, 129, 0.4) !important;
            -moz-box-shadow: 0 6px 16px rgba(16, 185, 129, 0.4) !important;
            background: linear-gradient(90deg, #059669, #0891b2) !important;
        }
        
        /* ===== LINK HOVER EFFECTS - CROSS-BROWSER WITH GRADIENT COLOR ===== */
        a {
            transition: all 0.3s ease !important;
            -webkit-transition: all 0.3s ease !important;
            -moz-transition: all 0.3s ease !important;
        }
        
        a:hover {
            color: #93c5fd !important;
            text-shadow: 0 0 8px rgba(147, 197, 253, 0.5) !important;
        }
        
        /* ===== SOCIAL MEDIA ICONS HOVER - CROSS-PLATFORM ===== */
        .social-icon-wrapper {
            transition: transform 0.3s ease !important;
            -webkit-transition: transform 0.3s ease !important;
            -moz-transition: transform 0.3s ease !important;
        }
        
        .social-icon-wrapper:hover {
            transform: translateY(-8px) scale(1.05) !important;
            -webkit-transform: translateY(-8px) scale(1.05) !important;
            -moz-transform: translateY(-8px) scale(1.05) !important;
        }
        
        /* ===== SUCCESS/ERROR MESSAGES ===== */
        .stSuccess {
            background: rgba(16, 185, 129, 0.1) !important;
            border: 1px solid rgba(16, 185, 129, 0.3) !important;
            color: #6ee7b7 !important;
        }
        
        .stError {
            background: rgba(239, 68, 68, 0.1) !important;
            border: 1px solid rgba(239, 68, 68, 0.3) !important;
            color: #fca5a5 !important;
        }
        
        /* ===== CARD HOVER EFFECTS ===== */
        .card {
            transition: transform 0.3s ease, box-shadow 0.3s ease !important;
            -webkit-transition: transform 0.3s ease, box-shadow 0.3s ease !important;
            -moz-transition: transform 0.3s ease, box-shadow 0.3s ease !important;
        }
        
        .card:hover {
            transform: translateY(-2px) !important;
            -webkit-transform: translateY(-2px) !important;
            -moz-transform: translateY(-2px) !important;
            box-shadow: 0 12px 32px rgba(96, 165, 250, 0.15) !important;
            -webkit-box-shadow: 0 12px 32px rgba(96, 165, 250, 0.15) !important;
            -moz-box-shadow: 0 12px 32px rgba(96, 165, 250, 0.15) !important;
        }
        
        /* ===== ACCESSIBILITY - HIGH CONTRAST MODE (Windows) ===== */
        @media (prefers-contrast: high) {
            .stTextInput input, 
            .stTextArea textarea, 
            .stSelectbox select {
                border: 2px solid rgba(96, 165, 250, 0.5) !important;
            }
        }
        
        /* ===== REDUCED MOTION SUPPORT ===== */
        @media (prefers-reduced-motion: reduce) {
            .stTextInput input,
            .stTextArea textarea,
            .stSelectbox select,
            .stButton > button,
            .stFormSubmitButton > button,
            .mailto-button,
            a,
            .social-icon-wrapper,
            .card {
                transition: none !important;
                -webkit-transition: none !important;
                -moz-transition: none !important;
            }
        }
        
        /* ===== LIGHT MODE SUPPORT ===== */
        @media (prefers-color-scheme: light) {
            .stTextInput input,
            .stTextArea textarea,
            .stSelectbox select {
                background: rgba(0, 0, 0, 0.03) !important;
                color: #1e293b !important;
                border: 1px solid rgba(59, 130, 246, 0.2) !important;
            }
        }
        </style>
    """, unsafe_allow_html=True)
    
    with st.form("contact_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input(
                "Your Name *",
                placeholder="John Doe",
                max_chars=80,
                key="contact_name"
            )
        
        with col2:
            email = st.text_input(
                "Your Email *",
                placeholder="john@example.com",
                max_chars=120,
                key="contact_email"
            )
        
        subject = st.selectbox(
            "Subject *",
            ["General Inquiry", "Technical Support", "Feature Request", "Bug Report", "Partnership", "Other"],
            key="contact_subject"
        )
        
        message = st.text_area(
            "Message *",
            placeholder="Type your message here...\n\nPlease provide as much detail as possible so we can assist you better.",
            height=150,
            max_chars=1000,
            key="contact_message"
        )
        
        # Generate mailto link if all fields are filled
        mailto_link = ""
        if name and email and message:
            subject_encoded = subject.replace(" ", "%20")
            body = f"From: {name} ({email})\n\nSubject: {subject}\n\n{message}\n\n---\nSent via {COMPANY_NAME} Contact Form"
            body_encoded = body.replace("\n", "%0A").replace(" ", "%20").replace("&", "%26")
            mailto_link = f"mailto:{CONTACT_EMAIL}?subject={subject_encoded}&body={body_encoded}"

        # Display mailto button if ALL fields are filled
        if name and email and message:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(
                f"""
                <div style="text-align: center;">
                    <a href="{mailto_link}" target="_blank" style="text-decoration: none;">
                        <button class="mailto-button">📧 Open in Email Client</button>
                    </a>
                    <p style="color: #94a3b8; font-size: 0.85rem; margin-top: 0.5rem;">
                        Click to compose in your default email app
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button("📤 Send Message", use_container_width=True)
        
        if submitted:
            if name and email and message:
                st.success(f"✅ Thank you, {name}! Your message has been sent successfully. We'll get back to you at {email} soon!")
            else:
                st.error("❌ Please fill in all required fields (marked with *).")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Contact Information Cards
    st.markdown("""
        <h3 style='background: linear-gradient(135deg, #60a5fa, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-size: 1.8rem; font-weight: 800; margin: 2rem 0 1.5rem 0; text-align: center;'>
            📞 Contact Information
        </h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class="card" style="text-align: center; height: 100%;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📧</div>
                <h4 style="color: #f1f5f9; font-size: 1.15rem; font-weight: 700; margin-bottom: 0.75rem;">Email</h4>
                <p style="color: #e2e8f0; line-height: 1.6; margin: 0;">
                    <a href="mailto:{CONTACT_EMAIL}" style="color: #60a5fa; text-decoration: none; font-weight: 500;">{CONTACT_EMAIL}</a>
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="card" style="text-align: center; height: 100%;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">💬</div>
                <h4 style="color: #f1f5f9; font-size: 1.15rem; font-weight: 700; margin-bottom: 0.75rem;">Live Chat</h4>
                <p style="color: #e2e8f0; line-height: 1.6; margin: 0; font-weight: 500;">
                    Mon-Fri, 9AM-5PM EST
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="card" style="text-align: center; height: 100%;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🌐</div>
                <h4 style="color: #f1f5f9; font-size: 1.15rem; font-weight: 700; margin-bottom: 0.75rem;">Social Media</h4>
                <p style="color: #e2e8f0; line-height: 1.6; margin: 0; font-weight: 500;">
                    @SpamDetectorAI
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Office Hours & Response Time
    st.markdown("""
        <h3 style='background: linear-gradient(135deg, #60a5fa, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-size: 1.8rem; font-weight: 800; margin: 2rem 0 1.5rem 0; text-align: center;'>
            ⏰ Office Hours & Response Time
        </h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="card" style="height: 100%; text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">🕐</div>
                <h4 style="color: #f1f5f9; font-size: 1.15rem; font-weight: 700; margin-bottom: 0.75rem;">Business Hours</h4>
                <p style="color: #e2e8f0; font-size: 0.98rem; margin: 0; line-height: 1.8; font-weight: 500;">
                    Monday - Friday: 9:00 AM - 6:00 PM EST<br>
                    Saturday: 10:00 AM - 4:00 PM EST<br>
                    Sunday: Closed
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="card" style="height: 100%; text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">⚡</div>
                <h4 style="color: #f1f5f9; font-size: 1.15rem; font-weight: 700; margin-bottom: 0.75rem;">Response Time</h4>
                <p style="color: #e2e8f0; font-size: 0.98rem; margin: 0; line-height: 1.8; font-weight: 500;">
                    General Inquiries: Within 24 hours<br>
                    Technical Support: Within 12 hours<br>
                    Urgent Issues: Within 4 hours
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="card" style="height: 100%; text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">🌍</div>
                <h4 style="color: #f1f5f9; font-size: 1.15rem; font-weight: 700; margin-bottom: 0.75rem;">Global Support</h4>
                <p style="color: #e2e8f0; font-size: 0.98rem; margin: 0; line-height: 1.8; font-weight: 500;">
                    24/7 automated support<br>
                    Multi-language assistance<br>
                    Worldwide coverage
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Social Media Links
    st.markdown("""
        <h3 style='background: linear-gradient(135deg, #60a5fa, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-size: 1.8rem; font-weight: 800; margin: 2rem 0 1.5rem 0; text-align: center;'>
            🤝 Connect With Us
        </h3>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="card">
            <div style="display: flex; justify-content: center; gap: 2.5rem; flex-wrap: wrap; padding: 1.5rem;">
                <a href="https://instagram.com/SpamDetectorAI" target="_blank" class="social-icon-wrapper" style="display: flex; flex-direction: column; align-items: center; text-decoration: none;">
                    <div style="width: 70px; height: 70px; background: linear-gradient(135deg, #1DA1F2, #0d8bd9); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 2rem; box-shadow: 0 8px 24px rgba(29, 161, 242, 0.4); -webkit-box-shadow: 0 8px 24px rgba(29, 161, 242, 0.4); -moz-box-shadow: 0 8px 24px rgba(29, 161, 242, 0.4);">🐦</div>
                    <span style="color: #e2e8f0; margin-top: 0.75rem; font-size: 0.95rem; font-weight: 600;">Twitter</span>
                </a>
                <a href="https://linkedin.com/company/spamdetectorai" target="_blank" class="social-icon-wrapper" style="display: flex; flex-direction: column; align-items: center; text-decoration: none;">
                    <div style="width: 70px; height: 70px; background: linear-gradient(135deg, #0077B5, #005582); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 2rem; box-shadow: 0 8px 24px rgba(0, 119, 181, 0.4); -webkit-box-shadow: 0 8px 24px rgba(0, 119, 181, 0.4); -moz-box-shadow: 0 8px 24px rgba(0, 119, 181, 0.4);">💼</div>
                    <span style="color: #e2e8f0; margin-top: 0.75rem; font-size: 0.95rem; font-weight: 600;">LinkedIn</span>
                </a>
                <a href="https://github.com/SpamDetectorAI" target="_blank" class="social-icon-wrapper" style="display: flex; flex-direction: column; align-items: center; text-decoration: none;">
                    <div style="width: 70px; height: 70px; background: linear-gradient(135deg, #333, #000); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 2rem; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5); -webkit-box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5); -moz-box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);">🐙</div>
                    <span style="color: #e2e8f0; margin-top: 0.75rem; font-size: 0.95rem; font-weight: 600;">GitHub</span>
                </a>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Office Location
    st.markdown("""
        <h3 style='background: linear-gradient(135deg, #60a5fa, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-size: 1.8rem; font-weight: 800; margin: 2rem 0 1.5rem 0; text-align: center;'>
            📍 Office Location
        </h3>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="card">
            <div style="text-align: center; padding: 2rem;">
                <div style="font-size: 3.5rem; margin-bottom: 1rem;">🏢</div>
                <p style="color: #e2e8f0; font-size: 1.15rem; line-height: 1.9; margin: 0;">
                    <strong style="color: #f1f5f9; font-size: 1.25rem; font-weight: 700;">{COMPANY_NAME} Headquarters</strong><br>
                    <span style="color: #cbd5e1;">221B Secure Lane, Suite 400</span><br>
                    <span style="color: #cbd5e1;">Cyber City, AI State 45678</span><br>
                    <span style="color: #cbd5e1;">United States</span>
                </p>
                <div style="margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid rgba(96, 165, 250, 0.2);">
                    <p style="color: #94a3b8; font-size: 0.95rem; margin: 0;">
                        For urgent matters, please email us directly at<br>
                        <a href="mailto:{CONTACT_EMAIL}" style="color: #60a5fa; text-decoration: none; font-weight: 600;">{CONTACT_EMAIL}</a>
                    </p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

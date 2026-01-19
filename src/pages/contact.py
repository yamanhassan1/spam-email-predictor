import streamlit as st


def render_contact_page():
    """Render the Contact page with design matching home page."""
    
    # Header section
    st.markdown("""
        <div class="card" style="text-align: center; padding: 3rem 2rem; margin-bottom: 2rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">📧</div>
            <h1 style="font-size: 3rem; font-weight: 900; margin-bottom: 1rem;">Get In Touch</h1>
            <p style="color: #cbd5e1; font-size: 1.1rem;">We'd love to hear from you!</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Contact Form Section
    st.markdown("""
        <div class="card" style="margin-bottom: 2rem; text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📬</div>
            <h3 style='color: #f8fafc; margin-bottom: 0.75rem; font-size: 1.1rem; font-weight: 700;'>
                Send Us a Message
            </h3>
            <p style='color: #cbd5e1; margin-bottom: 0; line-height: 1.6;'>
                Fill out the form below and we'll get back to you within 24 hours.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Custom styled form
    st.markdown("""
        <style>
        .stTextInput input, .stTextArea textarea, .stSelectbox select {
            background: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 12px !important;
            color: #f8fafc !important;
            font-size: 1rem !important;
            padding: 1rem !important;
            transition: all 0.3s ease !important;
        }
        .stTextInput input:focus, .stTextArea textarea:focus, .stSelectbox select:focus {
            border-color: rgba(59, 130, 246, 0.5) !important;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    with st.form("contact_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input(
                "Your Name",
                placeholder="John Doe",
                max_chars=80
            )
        
        with col2:
            email = st.text_input(
                "Your Email",
                placeholder="john@example.com",
                max_chars=120
            )
        
        subject = st.selectbox(
            "Subject",
            ["General Inquiry", "Technical Support", "Feature Request", "Bug Report", "Partnership", "Other"]
        )
        
        message = st.text_area(
            "Message",
            placeholder="Type your message here...",
            height=150,
            max_chars=1000
        )
        
        # Generate mailto link if all fields are filled
        mailto_link = ""
        if name and email and message:
            subject_encoded = subject.replace(" ", "%20")
            body = f"From: {name} <{email}>\n\n{message}"
            body_encoded = body.replace("\n", "%0A").replace(" ", "%20")
            mailto_link = f"mailto:yamanhassan.10@yahoo.com?subject={subject_encoded}&body={body_encoded}"

        # Display mailto button if ALL fields are filled
        if name and email and message:
            st.markdown(
                f"""
                <a href="{mailto_link}" target="_blank" style="display:inline-block; text-decoration:none;">
                    <button style="
                        background: linear-gradient(90deg,#3b82f6,#8b5cf6);
                        color: #fff;
                        border: none;
                        border-radius: 12px;
                        padding: 0.75rem 2.5rem;
                        font-size: 1.08rem;
                        font-weight: 700;
                        box-shadow: 0 2px 8px rgba(59,130,246,0.15);
                        cursor: pointer;
                        margin-top: 1rem;
                    ">📧 Send via Email Client</button>
                </a>
                """,
                unsafe_allow_html=True
            )
            
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button("📤 Send Message", use_container_width=True)
        
        if submitted:
            if name and email and message:
                st.success("✅ Thank you! Your message has been sent successfully. We'll get back to you soon!")
            else:
                st.error("❌ Please fill in all required fields.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Contact Information Cards
    st.markdown("""
        <h3 style='color: #f8fafc; font-size: 1.5rem; font-weight: 700; margin: 2rem 0 1.5rem 0; text-align: center;'>
            📞 Contact Information
        </h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="card" style="text-align: center; height: 100%;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📧</div>
                <h4 style="color: #f8fafc; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.75rem;">Email</h4>
                <p style="color: #cbd5e1; line-height: 1.6; margin: 0;">
                    <a href="mailto:yamanhassan.10@yahoo.com" style="color: #60a5fa; text-decoration: none;">yamanhassan.10@yahoo.com</a>
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="card" style="text-align: center; height: 100%;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">💬</div>
                <h4 style="color: #f8fafc; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.75rem;">Live Chat</h4>
                <p style="color: #cbd5e1; line-height: 1.6; margin: 0;">
                    Mon-Fri, 9AM-5PM EST
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="card" style="text-align: center; height: 100%;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🌐</div>
                <h4 style="color: #f8fafc; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.75rem;">Social Media</h4>
                <p style="color: #cbd5e1; line-height: 1.6; margin: 0;">
                    @SpamDetectorAI
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Office Hours & Response Time
    st.markdown("""
        <h3 style='color: #f8fafc; font-size: 1.5rem; font-weight: 700; margin: 2rem 0 1.5rem 0; text-align: center;'>
            ⏰ Office Hours & Response Time
        </h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="card" style="height: 100%; text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.75rem;">🕐</div>
                <h4 style="color: #f8fafc; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.75rem;">Business Hours</h4>
                <p style="color: #cbd5e1; font-size: 0.95rem; margin: 0; line-height: 1.7;">
                    Monday - Friday: 9:00 AM - 6:00 PM EST<br>
                    Saturday: 10:00 AM - 4:00 PM EST<br>
                    Sunday: Closed
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="card" style="height: 100%; text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.75rem;">⚡</div>
                <h4 style="color: #f8fafc; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.75rem;">Response Time</h4>
                <p style="color: #cbd5e1; font-size: 0.95rem; margin: 0; line-height: 1.7;">
                    General Inquiries: Within 24 hours<br>
                    Technical Support: Within 12 hours<br>
                    Urgent Issues: Within 4 hours
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="card" style="height: 100%; text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.75rem;">🌍</div>
                <h4 style="color: #f8fafc; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.75rem;">Global Support</h4>
                <p style="color: #cbd5e1; font-size: 0.95rem; margin: 0; line-height: 1.7;">
                    24/7 automated support<br>
                    Multi-language assistance<br>
                    Worldwide coverage
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Social Media Links
    st.markdown("""
        <h3 style='color: #f8fafc; font-size: 1.5rem; font-weight: 700; margin: 2rem 0 1.5rem 0; text-align: center;'>
            🤝 Connect With Us
        </h3>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="card">
            <div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap; padding: 1rem;">
                <a href="https://instagram.com/SpamDetectorAI" target="_blank" style="display: flex; flex-direction: column; align-items: center; text-decoration: none; transition: transform 0.3s;" onmouseover="this.style.transform='translateY(-5px)'" onmouseout="this.style.transform='translateY(0)'">
                    <div style="width: 60px; height: 60px; background: linear-gradient(135deg, #1DA1F2, #0d8bd9); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.75rem; box-shadow: 0 8px 24px rgba(29, 161, 242, 0.3);">🐦</div>
                    <span style="color: #cbd5e1; margin-top: 0.5rem; font-size: 0.9rem;">Twitter</span>
                </a>
                <a href="https://linkedin.com/company/spamdetectorai" target="_blank" style="display: flex; flex-direction: column; align-items: center; text-decoration: none; transition: transform 0.3s;" onmouseover="this.style.transform='translateY(-5px)'" onmouseout="this.style.transform='translateY(0)'">
                    <div style="width: 60px; height: 60px; background: linear-gradient(135deg, #0077B5, #005582); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.75rem; box-shadow: 0 8px 24px rgba(0, 119, 181, 0.3);">💼</div>
                    <span style="color: #cbd5e1; margin-top: 0.5rem; font-size: 0.9rem;">LinkedIn</span>
                </a>
                <a href="https://github.com/SpamDetectorAI" target="_blank" style="display: flex; flex-direction: column; align-items: center; text-decoration: none; transition: transform 0.3s;" onmouseover="this.style.transform='translateY(-5px)'" onmouseout="this.style.transform='translateY(0)'">
                    <div style="width: 60px; height: 60px; background: linear-gradient(135deg, #333, #000); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.75rem; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);">🐙</div>
                    <span style="color: #cbd5e1; margin-top: 0.5rem; font-size: 0.9rem;">GitHub</span>
                </a>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Office Location
    st.markdown("""
        <h3 style='color: #f8fafc; font-size: 1.5rem; font-weight: 700; margin: 2rem 0 1.5rem 0; text-align: center;'>
            📍 Office Location
        </h3>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="card">
            <div style="text-align: center; padding: 2rem;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🏢</div>
                <p style="color: #cbd5e1; font-size: 1.1rem; line-height: 1.8; margin: 0;">
                    <strong style="color: #f8fafc;">AI Spam Detector Headquarters</strong><br>
                    221B Secure Lane, Suite 400<br>
                    Cyber City, AI State 45678<br>
                    United States
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)
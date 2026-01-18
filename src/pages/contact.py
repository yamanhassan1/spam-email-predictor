import streamlit as st
import streamlit.components.v1 as components


def render_contact_page():
    """Render the Contact page."""

    # ---------------- HEADER ----------------
    st.markdown("""
        <div class="card gradient-border animate" style="text-align: center; padding: 3rem 2rem; margin-bottom: 2rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">📧</div>
            <h1 style="font-size: 3rem; font-weight: 900; margin-bottom: 1rem; color: #f8fafc;">Get In Touch</h1>
            <div style="height: 4px; width: 100px; margin: 0 auto 1.5rem; background: linear-gradient(90deg, #3b82f6, #8b5cf6); border-radius: 999px;"></div>
            <p style="color: #cbd5e1; font-size: 1.1rem;">We'd love to hear from you!</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    # ---------------- FORM ----------------
    with col1:
        st.markdown("""
            <div class="card animate">
                <h3 style="color: #f8fafc; font-size: 1.5rem; font-weight: 700; margin-bottom: 1.5rem;">
                    📬 Send Us a Message
                </h3>
        """, unsafe_allow_html=True)

        with st.form("contact_form"):
            name = st.text_input("Your Name", placeholder="John Doe")
            email = st.text_input("Your Email", placeholder="john@example.com")
            subject = st.selectbox(
                "Subject",
                ["General Inquiry", "Technical Support", "Feature Request", "Bug Report", "Other"]
            )
            message = st.text_area("Message", placeholder="Type your message here...", height=150)

            submitted = st.form_submit_button("📤 Send Message", use_container_width=True)

            if submitted:
                if name and email and message:
                    st.success("✅ Thank you! Your message has been sent successfully. We'll get back to you soon!")
                else:
                    st.error("❌ Please fill in all required fields.")

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- CONTACT INFO (FIXED) ----------------
    with col2:
        components.html("""
            <div class="card animate" style="animation-delay: 0.1s; height: 100%;">
                <h3 style="color: #f8fafc; font-size: 1.5rem; font-weight: 700; margin-bottom: 1.5rem;">
                    📞 Contact Information
                </h3>

                <div style="display: grid; gap: 1.25rem;">
                    <div style="background: rgba(59, 130, 246, 0.05); padding: 1.25rem; border-radius: 12px; border-left: 4px solid #3b82f6;">
                        <div style="font-size: 1.75rem; margin-bottom: 0.5rem;">📧</div>
                        <h4 style="color: #60a5fa; font-weight: 700; margin-bottom: 0.5rem;">Email</h4>
                        <p style="color: #cbd5e1; margin: 0;">support@spamdetector.ai</p>
                    </div>

                    <div style="background: rgba(139, 92, 246, 0.05); padding: 1.25rem; border-radius: 12px; border-left: 4px solid #8b5cf6;">
                        <div style="font-size: 1.75rem; margin-bottom: 0.5rem;">💬</div>
                        <h4 style="color: #a78bfa; font-weight: 700; margin-bottom: 0.5rem;">Live Chat</h4>
                        <p style="color: #cbd5e1; margin: 0;">Available Mon-Fri, 9AM-5PM EST</p>
                    </div>

                    <div style="background: rgba(16, 185, 129, 0.05); padding: 1.25rem; border-radius: 12px; border-left: 4px solid #10b981;">
                        <div style="font-size: 1.75rem; margin-bottom: 0.5rem;">🌐</div>
                        <h4 style="color: #34d399; font-weight: 700; margin-bottom: 0.5rem;">Social Media</h4>
                        <p style="color: #cbd5e1; margin: 0;">Follow us @SpamDetectorAI</p>
                    </div>
                </div>

                <div style="margin-top: 2rem; padding-top: 2rem; border-top: 1px solid rgba(255, 255, 255, 0.08);">
                    <h4 style="color: #f8fafc; font-weight: 700; margin-bottom: 1rem; text-align: center;">Response Time</h4>
                    <p style="color: #94a3b8; text-align: center; line-height: 1.7;">
                        We typically respond within 24 hours during business days.
                        For urgent technical issues, please mark your inquiry as "Technical Support".
                    </p>
                </div>
            </div>
        """, height=620)

    # ---------------- CONNECT WITH US (FIXED) ----------------
    components.html("""
        <div class="card gradient-border animate" style="animation-delay: 0.2s;">
            <h3 style="color: #f8fafc; font-size: 1.5rem; font-weight: 700; margin-bottom: 1.5rem; text-align: center;">
                🤝 Connect With Us
            </h3>

            <div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap; margin-top: 1.5rem;">
                <div style="text-align:center">
                    <div style="width: 60px; height: 60px; background: linear-gradient(135deg, #1DA1F2, #0d8bd9); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.75rem;">🐦</div>
                    <span style="color: #cbd5e1;">Twitter</span>
                </div>

                <div style="text-align:center">
                    <div style="width: 60px; height: 60px; background: linear-gradient(135deg, #0077B5, #005582); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.75rem;">💼</div>
                    <span style="color: #cbd5e1;">LinkedIn</span>
                </div>

                <div style="text-align:center">
                    <div style="width: 60px; height: 60px; background: linear-gradient(135deg, #333, #000); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.75rem;">🐙</div>
                    <span style="color: #cbd5e1;">GitHub</span>
                </div>

                <div style="text-align:center">
                    <div style="width: 60px; height: 60px; background: linear-gradient(135deg, #7289DA, #5865F2); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.75rem;">💬</div>
                    <span style="color: #cbd5e1;">Discord</span>
                </div>
            </div>
        </div>
    """, height=260)

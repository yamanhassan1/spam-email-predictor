import streamlit as st
import streamlit.components.v1 as components
def render_contact_page():

    # ================= HEADER =================
    st.markdown("""
        <div class="card gradient-border animate" style="text-align: center; padding: 3rem 2rem; margin-bottom: 2rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">📧</div>
            <h1 style="font-size: 3rem; font-weight: 900; margin-bottom: 1rem; color: #f8fafc;">Get In Touch</h1>
            <div style="height: 4px; width: 100px; margin: 0 auto 1.5rem; background: linear-gradient(90deg, #3b82f6, #8b5cf6); border-radius: 999px;"></div>
            <p style="color: #cbd5e1; font-size: 1.1rem;">We'd love to hear from you!</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # ================= SEND MESSAGE =================
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
                    st.success("✅ Thank you! Your message has been sent successfully.")
                else:
                    st.error("❌ Please fill in all required fields.")

        st.markdown("</div>", unsafe_allow_html=True)

    # ================= CONTACT INFORMATION (FIXED OUTPUT) =================
    with col2:
        st.markdown("""
            <div class="card animate" style="height: 100%;">
                <h3 style="color: #f8fafc; font-size: 1.5rem; font-weight: 700; margin-bottom: 1.5rem;">
                    📞 Contact Information
                </h3>
                <div style="color: #cbd5e1; font-size: 1rem; margin-bottom: 1rem;">
                    <strong>Email:</strong> <a href="mailto:support@spamdetector.com" style="color: #60a5fa;">support@spamdetector.com</a>
                </div>
                <div style="color: #cbd5e1; font-size: 1rem; margin-bottom: 1rem;">
                    <strong>Twitter:</strong> <a href="https://twitter.com/spamdetector" target="_blank" style="color: #60a5fa;">@spamdetector</a>
                </div>
                <div style="color: #cbd5e1; font-size: 1rem; margin-bottom: 1rem;">
                    <strong>GitHub:</strong> <a href="https://github.com/spamdetector" target="_blank" style="color: #60a5fa;">github.com/spamdetector</a>
                </div>
                <div style="color: #cbd5e1; font-size: 1rem; margin-bottom: 0.5rem;">
                    <strong>Location:</strong> Remote • Worldwide 🌎
                </div>
                <div style="color: #94a3b8; font-size: 0.93rem; margin-top: 1.5rem;">
                    <em>We're always open to feedback and collaboration opportunities.</em>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # ========== FOOTER (OPTIONAL) ==========
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <div style="text-align: center; padding: 1.5rem 0; border-top: 1px solid rgba(255, 255, 255, 0.08); margin-top: 2rem;">
            <p style="color: #94a3b8; font-size: 0.8rem; margin: 0;">
                © 2026 Spam Detector<br>
                Built with ❤️
            </p>
        </div>
    """, unsafe_allow_html=True)

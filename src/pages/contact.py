import streamlit as st
import streamlit.components.v1 as components


def render_contact_html():
    """
    Renders a custom HTML/CSS block for embedded contact/social links.
    """
    contact_html = """
        <div class="card animate" style="height: 100%;">
            <h3 style="color: #f8fafc; font-size: 1.5rem; font-weight: 700; margin-bottom: 1.5rem;">
                📞 Contact Information
            </h3>
            <div style="margin-bottom: 1.25rem;">
                <div style="display: flex; align-items: center; margin-bottom: 0.75rem;">
                    <div style="font-size: 1.3rem; margin-right: 0.7rem;">✉️</div>
                    <a href="mailto:support@spamdetector.com" style="color: #60a5fa; font-size: 1.02rem; text-decoration: none;">
                        support@spamdetector.com
                    </a>
                </div>
                <div style="display: flex; align-items: center; margin-bottom: 0.75rem;">
                    <div style="font-size: 1.3rem; margin-right: 0.7rem;">🌐</div>
                    <a href="https://www.spamdetector.com" target="_blank" style="color: #60a5fa; font-size: 1.02rem; text-decoration: none;">
                        www.spamdetector.com
                    </a>
                </div>
                <div style="display: flex; align-items: center; margin-bottom: 0.75rem;">
                    <div style="font-size: 1.3rem; margin-right: 0.7rem;">🐦</div>
                    <a href="https://twitter.com/spamdetector" target="_blank" style="color: #60a5fa; font-size: 1.02rem; text-decoration: none;">
                        @spamdetector
                    </a>
                </div>
                <div style="display: flex; align-items: center;">
                    <div style="font-size: 1.3rem; margin-right: 0.7rem;">💼</div>
                    <a href="https://linkedin.com/company/spamdetector" target="_blank" style="color: #60a5fa; font-size: 1.02rem; text-decoration: none;">
                        LinkedIn
                    </a>
                </div>
            </div>
            <hr style="border: 1px solid #1e293b; margin: 1.1rem 0;">
            <h4 style="color: #38bdf8; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.8rem;">
                Office Address
            </h4>
            <div style="color: #cbd5e1; font-size: 1rem;">
                221B Secure Lane,<br>
                Suite 400,<br>
                Cyber City, AI State<br>
                45678
            </div>
        </div>
    """
    components.html(contact_html, height=480, scrolling=False)



def render_contact_page():

    # ================= HEADER (UNCHANGED) =================
    st.markdown("""
        <div class="card gradient-border animate" style="text-align: center; padding: 3rem 2rem; margin-bottom: 2rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">📧</div>
            <h1 style="font-size: 3rem; font-weight: 900; margin-bottom: 1rem; color: #f8fafc;">Get In Touch</h1>
            <div style="height: 4px; width: 100px; margin: 0 auto 1.5rem; background: linear-gradient(90deg, #3b82f6, #8b5cf6); border-radius: 999px;"></div>
            <p style="color: #cbd5e1; font-size: 1.1rem;">We'd love to hear from you!</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

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
    
    # ================= CONTACT INFORMATION (STYLE MATCHED) =================
    with col2:
        st.markdown("""
            <div class="card animate" style="height: 100%;">
                <h3 style="color: #f8fafc; font-size: 1.5rem; font-weight: 700; margin-bottom: 1.5rem;">
                    📞 Contact Information
                </h3>
                <div style="display: grid; gap: 1.25rem;">
                    <div style="padding: 1.25rem; border-radius: 12px;
                                background: rgba(59,130,246,0.06);
                                border-left: 4px solid #3b82f6;">
                        <h4 style="color: #60a5fa; font-weight: 700; font-size: 1rem; margin-bottom: 0.4rem;">📧 Email</h4>
                        <p style="color: #cbd5e1; font-size: 1rem; margin: 0 0 0.2rem 0;">support@spamdetector.ai</p>
                    </div>
                    <div style="padding: 1.25rem; border-radius: 12px;
                                background: rgba(139,92,246,0.06);
                                border-left: 4px solid #8b5cf6;">
                        <h4 style="color: #a78bfa; font-weight: 700; font-size: 1rem; margin-bottom: 0.4rem;">💬 Live Chat</h4>
                        <p style="color: #cbd5e1; font-size: 1rem; margin: 0 0 0.2rem 0;">Mon–Fri, 9AM–5PM EST</p>
                    </div>
                    <div style="padding: 1.25rem; border-radius: 12px;
                                background: rgba(16,185,129,0.06);
                                border-left: 4px solid #10b981;">
                        <h4 style="color: #34d399; font-weight: 700; font-size: 1rem; margin-bottom: 0.4rem;">🌐 Social Media</h4>
                        <p style="color: #cbd5e1; font-size: 1rem; margin: 0 0 0.2rem 0;">@SpamDetectorAI</p>
                    </div>
                </div>
                <div style="margin-top: 2rem; padding-top: 1.5rem; border-top: 1px solid rgba(255,255,255,0.08);">
                    <p style="color: #94a3b8; font-size: 0.95rem; text-align: center; line-height: 1.7;">
                        ⏱ We typically respond within 24 hours on business days.
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        
    st.markdown("""
        <div class="card animate" style="height: 100%;">
            <h3 style="color: #f8fafc; font-size: 1.5rem; font-weight: 700; margin-bottom: 1.5rem; text-align: center;">
                🤝 Connect With Us
            </h3>
            <div style="display: flex; gap: 1.75rem; flex-wrap: wrap; justify-content: center;">
                <a href="https://twitter.com/SpamDetectorAI" target="_blank" style="text-decoration: none;">
                    <div style="width: 56px; height: 56px; border-radius: 14px;
                                background: linear-gradient(135deg, #1DA1F2, #0d8bd9);
                                display: flex; align-items: center; justify-content: center;
                                font-size: 1.5rem;
                                margin-bottom: 0.5rem;">
                        🐦
                    </div>
                    <div style="color: #cbd5e1; font-size: 0.95rem; text-align: center;">Twitter</div>
                </a>
                <a href="https://linkedin.com/company/spamdetectorai" target="_blank" style="text-decoration: none;">
                    <div style="width: 56px; height: 56px; border-radius: 14px;
                                background: linear-gradient(135deg, #0077B5, #005582);
                                display: flex; align-items: center; justify-content: center;
                                font-size: 1.5rem;
                                margin-bottom: 0.5rem;">
                        💼
                    </div>
                    <div style="color: #cbd5e1; font-size: 0.95rem; text-align: center;">LinkedIn</div>
                </a>
                <a href="https://github.com/SpamDetectorAI" target="_blank" style="text-decoration: none;">
                    <div style="width: 56px; height: 56px; border-radius: 14px;
                                background: linear-gradient(135deg, #333, #000);
                                display: flex; align-items: center; justify-content: center;
                                font-size: 1.5rem;
                                margin-bottom: 0.5rem;">
                        🐙
                    </div>
                    <div style="color: #cbd5e1; font-size: 0.95rem; text-align: center;">GitHub</div>
                </a>
                <a href="https://discord.gg/spamdetectorai" target="_blank" style="text-decoration: none;">
                    <div style="width: 56px; height: 56px; border-radius: 14px;
                                background: linear-gradient(135deg, #7289DA, #5865F2);
                                display: flex; align-items: center; justify-content: center;
                                font-size: 1.5rem;
                                margin-bottom: 0.5rem;">
                        💬
                    </div>
                    <div style="color: #cbd5e1; font-size: 0.95rem; text-align: center;">Discord</div>
                </a>
            </div>
        </div>
    """, unsafe_allow_html=True)

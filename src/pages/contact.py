import streamlit as st


def render_contact_page():
    # ---------------- HEADER ----------------
    st.markdown(
        """
        <div class="card gradient-border" style="text-align:center; padding:3rem 2rem; margin-bottom:2rem;">
            <div style="font-size:4rem;">📧</div>
            <h1 style="font-size:3rem; font-weight:900; color:#f8fafc;">Get In Touch</h1>
            <div style="height:4px; width:90px; margin:1rem auto;
                        background:linear-gradient(90deg,#3b82f6,#8b5cf6);
                        border-radius:999px;"></div>
            <p style="color:#cbd5e1; font-size:1.1rem;">
                We’d love to hear from you!
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------------- MAIN LAYOUT ----------------
    col1, col2 = st.columns(2)

    # ---------------- CONTACT FORM ----------------
    with col1:
        st.markdown(
            """
            <div class="card">
                <h3 style="color:#f8fafc; font-weight:700; margin-bottom:1.5rem;">
                    📬 Send Us a Message
                </h3>
            """,
            unsafe_allow_html=True
        )

        with st.form("contact_form"):
            name = st.text_input("Your Name", placeholder="John Doe")
            email = st.text_input("Your Email", placeholder="john@example.com")
            subject = st.selectbox(
                "Subject",
                ["General Inquiry", "Technical Support", "Feature Request", "Bug Report", "Other"]
            )
            message = st.text_area(
                "Message",
                placeholder="Type your message here...",
                height=160
            )

            submit = st.form_submit_button("📤 Send Message", use_container_width=True)

            if submit:
                if not name or not email or not message:
                    st.error("❌ Please fill in all required fields.")
                else:
                    st.success("✅ Thank you! Your message has been sent successfully.")

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- CONTACT INFO ----------------
    with col2:
        st.markdown(
            """
            <div class="card">
                <h3 style="color:#f8fafc; font-weight:700; margin-bottom:1.5rem;">
                    📞 Contact Information
                </h3>

                <div style="display:grid; gap:1.25rem;">
                    <div style="background:rgba(59,130,246,0.05);
                                padding:1.25rem; border-radius:12px;
                                border-left:4px solid #3b82f6;">
                        <h4 style="color:#60a5fa;">📧 Email</h4>
                        <p style="color:#cbd5e1;">support@spamdetector.ai</p>
                    </div>

                    <div style="background:rgba(139,92,246,0.05);
                                padding:1.25rem; border-radius:12px;
                                border-left:4px solid #8b5cf6;">
                        <h4 style="color:#a78bfa;">💬 Live Chat</h4>
                        <p style="color:#cbd5e1;">Mon–Fri, 9AM–5PM EST</p>
                    </div>

                    <div style="background:rgba(16,185,129,0.05);
                                padding:1.25rem; border-radius:12px;
                                border-left:4px solid #10b981;">
                        <h4 style="color:#34d399;">🌐 Social Media</h4>
                        <p style="color:#cbd5e1;">@SpamDetectorAI</p>
                    </div>
                </div>

                <div style="margin-top:2rem; padding-top:1.5rem;
                            border-top:1px solid rgba(255,255,255,0.1);">
                    <h4 style="color:#f8fafc; text-align:center;">Response Time</h4>
                    <p style="color:#94a3b8; text-align:center; line-height:1.6;">
                        We usually reply within 24 hours on business days.
                        For urgent issues, choose <b>Technical Support</b>.
                    </p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ---------------- SOCIAL LINKS ----------------
    st.markdown(
        """
        <div class="card gradient-border" style="margin-top:2.5rem;">
            <h3 style="color:#f8fafc; font-weight:700; text-align:center;">
                🤝 Connect With Us
            </h3>

            <div style="display:flex; justify-content:center;
                        gap:2rem; flex-wrap:wrap; margin-top:1.5rem;">
                
                <a href="#" style="text-align:center; text-decoration:none;">
                    <div style="width:60px; height:60px;
                                background:linear-gradient(135deg,#1DA1F2,#0d8bd9);
                                border-radius:50%; display:flex;
                                align-items:center; justify-content:center;
                                font-size:1.6rem;">🐦</div>
                    <span style="color:#cbd5e1;">Twitter</span>
                </a>

                <a href="#" style="text-align:center; text-decoration:none;">
                    <div style="width:60px; height:60px;
                                background:linear-gradient(135deg,#0077B5,#005582);
                                border-radius:50%; display:flex;
                                align-items:center; justify-content:center;
                                font-size:1.6rem;">💼</div>
                    <span style="color:#cbd5e1;">LinkedIn</span>
                </a>

                <a href="#" style="text-align:center; text-decoration:none;">
                    <div style="width:60px; height:60px;
                                background:linear-gradient(135deg,#333,#000);
                                border-radius:50%; display:flex;
                                align-items:center; justify-content:center;
                                font-size:1.6rem;">🐙</div>
                    <span style="color:#cbd5e1;">GitHub</span>
                </a>

                <a href="#" style="text-align:center; text-decoration:none;">
                    <div style="width:60px; height:60px;
                                background:linear-gradient(135deg,#7289DA,#5865F2);
                                border-radius:50%; display:flex;
                                align-items:center; justify-content:center;
                                font-size:1.6rem;">💬</div>
                    <span style="color:#cbd5e1;">Discord</span>
                </a>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

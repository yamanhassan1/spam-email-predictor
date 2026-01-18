import streamlit as st
import streamlit.components.v1 as components


def render_contact_page():

    # ================= HEADER =================
    st.markdown(
        """
        <div style="text-align:center; padding:3rem 2rem;">
            <div style="font-size:4rem;">📧</div>
            <h1 style="color:#f8fafc; font-size:3rem; font-weight:900;">Get In Touch</h1>
            <div style="height:4px;width:90px;margin:1rem auto;
                        background:linear-gradient(90deg,#3b82f6,#8b5cf6);
                        border-radius:999px;"></div>
            <p style="color:#cbd5e1;font-size:1.1rem;">
                We’d love to hear from you!
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    # ================= FORM =================
    with col1:
        st.markdown("### 📬 Send Us a Message")

        with st.form("contact_form"):
            name = st.text_input("Your Name", placeholder="John Doe")
            email = st.text_input("Your Email", placeholder="john@example.com")
            subject = st.selectbox(
                "Subject",
                ["General Inquiry", "Technical Support", "Feature Request", "Bug Report", "Other"]
            )
            message = st.text_area("Message", height=160)

            submit = st.form_submit_button("📤 Send Message", use_container_width=True)

            if submit:
                if not name or not email or not message:
                    st.error("❌ Please fill in all required fields.")
                else:
                    st.success("✅ Message sent successfully!")

    # ================= CONTACT INFO (HTML COMPONENT) =================
    with col2:
        components.html(
            """
            <div style="background:#0f172a;padding:1.8rem;border-radius:16px;color:white">
                <h3 style="margin-bottom:1.2rem;">📞 Contact Information</h3>

                <div style="display:grid;gap:1.2rem">
                    <div style="padding:1rem;border-left:4px solid #3b82f6;background:rgba(59,130,246,0.08);border-radius:10px">
                        <h4 style="color:#60a5fa;">📧 Email</h4>
                        <p>support@spamdetector.ai</p>
                    </div>

                    <div style="padding:1rem;border-left:4px solid #8b5cf6;background:rgba(139,92,246,0.08);border-radius:10px">
                        <h4 style="color:#a78bfa;">💬 Live Chat</h4>
                        <p>Mon–Fri, 9AM–5PM EST</p>
                    </div>

                    <div style="padding:1rem;border-left:4px solid #10b981;background:rgba(16,185,129,0.08);border-radius:10px">
                        <h4 style="color:#34d399;">🌐 Social Media</h4>
                        <p>@SpamDetectorAI</p>
                    </div>
                </div>

                <hr style="margin:1.5rem 0;border:0;border-top:1px solid #1e293b">

                <p style="color:#94a3b8;text-align:center">
                    ⏱ We respond within 24 hours on business days
                </p>
            </div>
            """,
            height=480,
        )

    # ================= SOCIAL LINKS (HTML COMPONENT) =================
    components.html(
        """
        <div style="margin-top:3rem;padding:2rem;text-align:center;
                    background:#020617;border-radius:18px">

            <h3 style="color:white;margin-bottom:1.5rem">🤝 Connect With Us</h3>

            <div style="display:flex;justify-content:center;gap:2rem;flex-wrap:wrap">

                <div>
                    <div style="width:60px;height:60px;border-radius:50%;
                                background:linear-gradient(135deg,#1DA1F2,#0d8bd9);
                                display:flex;align-items:center;justify-content:center;
                                font-size:1.6rem">🐦</div>
                    <p style="color:#cbd5e1">Twitter</p>
                </div>

                <div>
                    <div style="width:60px;height:60px;border-radius:50%;
                                background:linear-gradient(135deg,#0077B5,#005582);
                                display:flex;align-items:center;justify-content:center;
                                font-size:1.6rem">💼</div>
                    <p style="color:#cbd5e1">LinkedIn</p>
                </div>

                <div>
                    <div style="width:60px;height:60px;border-radius:50%;
                                background:linear-gradient(135deg,#333,#000);
                                display:flex;align-items:center;justify-content:center;
                                font-size:1.6rem">🐙</div>
                    <p style="color:#cbd5e1">GitHub</p>
                </div>

                <div>
                    <div style="width:60px;height:60px;border-radius:50%;
                                background:linear-gradient(135deg,#7289DA,#5865F2);
                                display:flex;align-items:center;justify-content:center;
                                font-size:1.6rem">💬</div>
                    <p style="color:#cbd5e1">Discord</p>
                </div>

            </div>
        </div>
        """,
        height=260,
    )

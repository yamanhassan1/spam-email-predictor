"""
Optimized AI Spam Detector Application
Main entry point with improved architecture, security, and features.
"""
import streamlit as st
from pathlib import Path

# Core services
from src.core.spam_detector import SpamDetectorService, ModelLoadError
from src.core.file_handler import SecureFileHandler

# UI components
from src.ui.file_upload import render_file_upload_section, render_batch_mode_selector
from src.ui.batch_analysis import render_batch_analysis_results


class SpamDetectorApp:
    """Main application class with proper OOP design."""
    
    def __init__(self):
        """Initialize application."""
        self.setup_page_config()
        self.detector_service = None
        self.file_handler = SecureFileHandler()
        
        # Initialize session state
        if 'initialized' not in st.session_state:
            st.session_state.initialized = False
            st.session_state.analysis_mode = 'single'
    
    def setup_page_config(self):
        """Configure Streamlit page settings."""
        st.set_page_config(
            page_title="AI Spam Detector - Advanced ML Protection",
            page_icon="🛡️",
            layout="centered",
            initial_sidebar_state="collapsed",
            menu_items={
                'Get Help': None,
                'Report a bug': None,
                'About': "AI-Powered Spam Detector with Advanced ML"
            }
        )
    
    @st.cache_resource(show_spinner=False)
    def _load_detector_service(_self):
        """Load spam detector service (cached)."""
        try:
            return SpamDetectorService()
        except ModelLoadError as e:
            st.error(f"⚠️ Failed to load ML models: {str(e)}")
            st.stop()
    
    def apply_custom_css(self):
        """Apply custom CSS styling."""
        st.markdown("""
        <style>
        /* Import from uploaded design.py or use inline */
        :root {
            --bg-dark: #0a0e27;
            --glass-bg: rgba(255, 255, 255, 0.03);
            --glass-border: rgba(255, 255, 255, 0.08);
            --primary-blue: #3b82f6;
            --primary-purple: #8b5cf6;
            --success-green: #10b981;
            --danger-red: #ef4444;
            --text-primary: #f8fafc;
            --text-secondary: #cbd5e1;
        }
        
        .stApp {
            background: radial-gradient(ellipse at top, #0f1433, #0a0e27);
            color: var(--text-primary);
        }
        
        .card {
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1rem;
        }
        
        .stButton > button {
            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.75rem 2rem;
            font-weight: 700;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 32px rgba(59, 130, 246, 0.4);
        }
        
        /* Hide Streamlit branding */
        #MainMenu, footer, header {visibility: hidden;}
        </style>
        """, unsafe_allow_html=True)
    
    def render_header(self):
        """Render application header."""
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <div style="font-size: 4rem; margin-bottom: 0.5rem;">🛡️</div>
            <h1 style='color: var(--text-primary); font-size: 2.5rem; font-weight: 900; 
                       margin-bottom: 0.5rem; background: linear-gradient(135deg, #3b82f6, #8b5cf6); 
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                AI Spam Detector
            </h1>
            <p style='color: var(--text-secondary); font-size: 1.1rem; max-width: 600px; 
                     margin: 0 auto; line-height: 1.6;'>
                Advanced machine learning protection against phishing, scams, and malicious messages
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_single_message_mode(self):
        """Render single message analysis interface."""
        from src.components.input_section import render_input_section
        from src.pages.prediction_analysis import render_analysis_section
        from src.design import render_result_card
        
        # Input section
        st.markdown("""
        <div class="card" style="margin-bottom: 2rem; text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📝</div>
            <h3 style='color: #f8fafc; margin-bottom: 0.75rem; font-size: 1.1rem; font-weight: 700;'>
                Enter Your Message
            </h3>
            <p style='color: #cbd5e1; margin-bottom: 0; line-height: 1.6;'>
                Paste any email or SMS message below for instant AI-powered analysis
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        input_text = st.text_area(
            "Message",
            height=220,
            placeholder="📧 Paste your message here...\n\nExample: 'Congratulations! You've won $1,000,000! Click here now!'",
            label_visibility="collapsed",
            key="single_message_input"
        )
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            analyze_button = st.button("🔍 Analyze Message", use_container_width=True, type="primary")
        
        if analyze_button and input_text.strip():
            self._analyze_single_message(input_text)
    
    def _analyze_single_message(self, text: str):
        """Analyze a single message."""
        if len(text) > 50000:
            st.warning("⚠️ Message too long. Maximum 50,000 characters.")
            return
        
        with st.spinner("🔍 Analyzing message with AI..."):
            result = self.detector_service.predict(text)
        
        # Display result
        from src.design import render_result_card
        st.markdown(render_result_card(result.is_spam, result.confidence), unsafe_allow_html=True)
        
        # Detailed analysis
        from src.pages.prediction_analysis import render_single_prediction_analysis
        render_single_prediction_analysis(result, text)
    
    def render_batch_mode(self):
        """Render batch file upload and analysis interface."""
        # File upload section
        upload_results = render_file_upload_section()
        
        if upload_results and any(r.success for r in upload_results):
            # Collect all messages
            all_messages = []
            for result in upload_results:
                if result.success:
                    all_messages.extend(result.extracted_messages)
            
            if all_messages:
                # Analyze button
                st.markdown("<br>", unsafe_allow_html=True)
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    analyze_batch = st.button(
                        f"🚀 Analyze {len(all_messages)} Message(s)",
                        use_container_width=True,
                        type="primary",
                        key="analyze_batch_button"
                    )
                
                if analyze_batch:
                    self._analyze_batch_messages(all_messages)
    
    def _analyze_batch_messages(self, messages: list):
        """Analyze multiple messages in batch."""
        with st.spinner(f"🔍 Analyzing {len(messages)} messages..."):
            batch_result = self.detector_service.predict_batch(messages)
        
        # Display batch results
        render_batch_analysis_results(batch_result)
    
    def run(self):
        """Main application entry point."""
        # Apply styling
        self.apply_custom_css()
        
        # Load detector service
        if not st.session_state.initialized:
            with st.spinner("🤖 Loading AI models..."):
                self.detector_service = self._load_detector_service()
            st.session_state.initialized = True
        else:
            self.detector_service = self._load_detector_service()
        
        # Render header
        self.render_header()
        
        # Mode selector
        mode = render_batch_mode_selector()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Render appropriate mode
        if mode == 'single':
            self.render_single_message_mode()
        else:
            self.render_batch_mode()
        
        # Footer
        self.render_footer()
    
    def render_footer(self):
        """Render application footer."""
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align: center; padding: 2rem 0; border-top: 1px solid var(--glass-border); margin-top: 3rem;">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🛡️</div>
            <p style="color: #94a3b8; font-size: 0.85rem; margin: 0;">
                © 2026 AI Spam Detector • Built with ❤️ using Machine Learning<br>
                <span style="font-size: 0.75rem;">97%+ Accuracy • Real-time Analysis • 100% Privacy</span>
            </p>
        </div>
        """, unsafe_allow_html=True)


def main():
    """Application entry point."""
    app = SpamDetectorApp()
    app.run()


if __name__ == "__main__":
    main()
import streamlit as st

# ============================
# Core modules
# ============================
from src.design import setup_page, render_header, render_sidebar
from src.nlp import setup_nltk, get_stopwords
from src.model import load_model
from src.analysis import load_word_lists

# ============================
# Page modules - Import directly to avoid circular imports
# ============================
from src.pages.home import render_home_page
from src.pages.info_section import render_info_sections
from src.pages.about import render_about_page
from src.pages.help import render_help_page
from src.pages.contact import render_contact_page


@st.cache_data(show_spinner=False)
def _cached_load_model():
    """Load model and vectorizer once per session."""
    return load_model()


@st.cache_data(show_spinner=False)
def _cached_get_stopwords():
    """Load NLTK stopwords once per session."""
    return get_stopwords()


@st.cache_data(show_spinner=False)
def _cached_word_lists():
    """Load spam/ham word lists once per session."""
    return load_word_lists()


def main():
    """
    Main application function.
    Initializes the app and orchestrates page rendering.
    """

    # ----------------------------
    # 1. CRITICAL: Configure Streamlit page FIRST
    # This loads all CSS and styles before any rendering
    # ----------------------------
    setup_page(
        title="AI Spam Detector - Protect Your Inbox",
        animations=True,
        compact=False
    )

    # ----------------------------
    # 2. Render sidebar navigation AFTER page setup
    # ----------------------------
    page = render_sidebar()

    # ----------------------------
    # 3. Initialize NLP resources (only needed for Home page)
    # ----------------------------
    if page == "🏠 Home":
        setup_nltk()
        stop_words = _cached_get_stopwords()
        tfidf, model = _cached_load_model()
        spam_words_set, ham_words_set = _cached_word_lists()

    # ----------------------------
    # 4. Render content based on selected page
    # ----------------------------
    if page == "🏠 Home":
        # Render premium header
        render_header(
            title="AI-Powered Spam Detector",
            subtitle="Advanced ML protection against phishing, scams, and unwanted messages"
        )
        
        # Render home page
        render_home_page(tfidf, model, spam_words_set, ham_words_set, stop_words)
        
        # Render info sections
        render_info_sections()
    
    elif page == "ℹ️ About":
        render_header(
            title="About Spam Detector",
            subtitle="Learn more about our advanced spam detection technology"
        )
        render_about_page()
    
    elif page == "❓ Help":
        render_header(
            title="Help & Support",
            subtitle="Get assistance with using the Spam Detector"
        )
        render_help_page()
    
    elif page == "📧 Contact":
        render_header(
            title="Contact Us",
            subtitle="Get in touch with our team"
        )
        render_contact_page()


# ============================
# Application entry point
# ============================
if __name__ == "__main__":
    main()

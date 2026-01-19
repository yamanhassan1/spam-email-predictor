import streamlit as st

# ============================
# Core modules
# ============================
from src.design import setup_page, render_header, render_sidebar, render_slidebar
from src.nlp import setup_nltk, get_stopwords
from src.model import load_model
from src.analysis import SPAM_WORDS, HAM_WORDS

# ============================
# Page modules - Import directly to avoid circular imports
# ============================
from src.pages.home import render_home_page
from src.pages.info_section import render_info_sections
from src.pages.about import render_about_page
from src.pages.help import render_help_page
from src.pages.contact import render_contact_page


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
    page = render_slidebar()
    page = render_sidebar()

    # ----------------------------
    # 3. Initialize NLP resources (only needed for Home page)
    # ----------------------------
    if page == "🏠 Home":
        setup_nltk()
        stop_words = get_stopwords()
        
        # Load ML model and vectorizer
        tfidf, model = load_model()
        
        # Load word lists for pattern detection
        spam_words_set = SPAM_WORDS
        ham_words_set = HAM_WORDS

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
        render_about_page()
    
    elif page == "❓ Help":
        render_help_page()
    
    elif page == "📧 Contact":
        render_contact_page()


# ============================
# Application entry point
# ============================
if __name__ == "__main__":
    main()
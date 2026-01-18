import streamlit as st

# Core modules
from src.design import setup_page, render_header
from src.nlp import setup_nltk, get_stopwords
from src.model import load_model
from src.analysis import SPAM_WORDS, HAM_WORDS

# Page modules
from src.pages import home, info_sections


def main():
    """
    Main application function.
    Initializes the app and orchestrates page rendering.
    """
    # Initialize page configuration
    setup_page(
        title="AI Spam Detector - Protect Your Inbox",
        animations=True,
        compact=False
    )
    
    # Initialize NLP resources
    setup_nltk()
    STOP_WORDS = get_stopwords()
    
    # Load ML model and vectorizer
    tfidf, model = load_model()
    
    # Load word lists for pattern detection
    spam_words_set = SPAM_WORDS
    ham_words_set = HAM_WORDS
    
    # Render premium header
    render_header(
        title="AI-Powered Spam Detector",
        subtitle="Advanced machine learning protection against phishing, scams, and unwanted messages"
    )
    
    # Render main home page with prediction functionality
    home.render_home_page(tfidf, model, spam_words_set, ham_words_set)
    
    # Render information sections (How It Works, Features, Tips, etc.)
    info_sections.render_info_sections()


# Application entry point
if __name__ == "__main__":
    main()
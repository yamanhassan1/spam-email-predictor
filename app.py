import streamlit as st

# ============================
# Core modules
# ============================
from src.design import setup_page, render_header
from src.nlp import setup_nltk, get_stopwords
from src.model import load_model
from src.analysis import SPAM_WORDS, HAM_WORDS

# ============================
# Page modules
# ============================
# Only import pages at the top-level, no cross-page imports inside pages
from src.pages import home, info_sections


def main():
    """
    Main application function.
    Initializes the app and orchestrates page rendering.
    """

    # ----------------------------
    # 1. Configure Streamlit page
    # ----------------------------
    setup_page(
        title="AI Spam Detector - Protect Your Inbox",
        animations=True,
        compact=False
    )

    # ----------------------------
    # 2. Initialize NLP resources
    # ----------------------------
    setup_nltk()
    stop_words = get_stopwords()

    # ----------------------------
    # 3. Load ML model and vectorizer
    # ----------------------------
    tfidf, model = load_model()

    # ----------------------------
    # 4. Load word lists for pattern detection
    # ----------------------------
    spam_words_set = SPAM_WORDS
    ham_words_set = HAM_WORDS

    # ----------------------------
    # 5. Render premium header
    # ----------------------------
    render_header(
        title="AI-Powered Spam Detector",
        subtitle="Advanced ML protection against phishing, scams, and unwanted messages"
    )

    # ----------------------------
    # 6. Render home page
    # ----------------------------
    # Lazy imports inside page functions are unnecessary since pages no longer import each other
    home.render_home_page(tfidf, model, spam_words_set, ham_words_set, stop_words)

    # ----------------------------
    # 7. Render info sections
    # ----------------------------
    info_sections.render_info_sections()


# ============================
# Application entry point
# ============================
if __name__ == "__main__":
    main()

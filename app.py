import streamlit as st
# Core modules
from src.design import setup_page, render_header, render_sidebar
from src.nlp import setup_nltk, get_stopwords
from src.model import load_model
from src.analysis import SPAM_WORDS, HAM_WORDS
from src.pages.home import render_home_page
from src.pages.info_section import render_info_sections
from src.pages.about import render_about_page
from src.pages.help import render_help_page
from src.pages.contact import render_contact_page

def main():
    # 1. Setup page configuration
    setup_page(
        title="AI Spam Detector - Protect Your Inbox",
        animations=True,
        compact=False
    )
    
    # 2. Render sidebar and get selected page
    page = render_sidebar()
    
    # 3. Render content based on selected page
    if page == "🏠 Home":
        # Initialize NLP resources and model
        setup_nltk()
        stop_words = get_stopwords()
        
        # Load ML model and vectorizer
        tfidf, model = load_model()
        
        # Load word lists for pattern detection
        spam_words_set = SPAM_WORDS
        ham_words_set = HAM_WORDS
        
        # Render header
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

# Application entry point
if __name__ == "__main__":
    main()

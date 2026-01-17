import streamlit as st
import nltk
from collections import Counter
from pathlib import Path
import re
import numpy as np
import pandas as pd

# existing libs kept for compatibility with other parts of the app
import matplotlib.pyplot as plt
import plotly.express as px
from PIL import Image

# src helpers (advanced design + visualization)
from src.design import setup_page, render_header, render_result_card, render_info_cards
from src.nlp import setup_nltk, transformed_text, get_stopwords
from src.model import load_model
from src.analysis import SPAM_WORDS, HAM_WORDS
from src.visualization import (
    confidence_gauge,
    probability_bar,
    top_words_bar,
    characters_pie,
    word_length_line,
    wordcloud_figure,
    annotated_message_html,
)

# Initialize page + CSS and NLTK
setup_page()
setup_nltk()
STOP_WORDS = get_stopwords()

# Load model and vectorizer
tfidf, model = load_model()

# Wordlists from analysis module
spam_words_set = SPAM_WORDS
ham_words_set = HAM_WORDS

# Render header (keeps content identical but with updated styling)
render_header()

# Input Section
st.markdown("""
    <div class="input-card">
        <h3 style='color: #e6eefc; margin-bottom: 0.6rem; font-size: 1.1rem; font-weight: 700;'>📝 Enter Your Message</h3>
        <p style='color: #9aa4b2; margin-bottom: 1rem;'>Paste the email or SMS message you want to check below:</p>
    </div>
""", unsafe_allow_html=True)

input_sms = st.text_area(
    "Message",
    height=220,
    placeholder="Paste your email or SMS message here...\n\nExample: 'Congratulations! You've won $1,000,000! Click here to claim your prize now!'",
    label_visibility="collapsed"
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    predict_button = st.button("🔍 Analyze Message", use_container_width=True)

# Prediction & Analysis
if predict_button:
    if not input_sms.strip():
        st.warning("⚠️ Please enter a message to analyze.")
    else:
        with st.spinner("🔎 Analyzing message..."):
            # Preprocess
            transformed_sms = transformed_text(input_sms)

            # Vectorize + Predict
            vector_input = tfidf.transform([transformed_sms])
            result = model.predict(vector_input)[0]
            prediction_proba = model.predict_proba(vector_input)[0]
            confidence = max(prediction_proba) * 100
            spam_prob = prediction_proba[1] * 100
            ham_prob = prediction_proba[0] * 100

            # Message statistics
            word_count = len(input_sms.split())
            char_count = len(input_sms)
            char_count_no_spaces = len(input_sms.replace(" ", ""))
            sentence_count = len(nltk.sent_tokenize(input_sms))

            # Word frequency
            words = transformed_sms.split()
            word_freq = Counter(words)
            top_words = dict(word_freq.most_common(10)) if words else {}
            words_list = list(top_words.keys())
            freq_list = list(top_words.values())

            # Display result using design helper (consistent look)
            st.markdown(render_result_card(result == 1, confidence), unsafe_allow_html=True)

            # Statistics & Visualizations header
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 📊 Message Analysis & Statistics")

            # Info cards (words/characters/sentences/unique words)
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"""
                    <div class="info-card" style="padding: 1rem; text-align: center;">
                        <div style="font-size: 1.4rem; color: #5b7cff; font-weight: 700;">{word_count}</div>
                        <div style="color: #9aa4b2; margin-top: 0.4rem;">Words</div>
                    </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                    <div class="info-card" style="padding: 1rem; text-align: center;">
                        <div style="font-size: 1.4rem; color: #5b7cff; font-weight: 700;">{char_count}</div>
                        <div style="color: #9aa4b2; margin-top: 0.4rem;">Characters</div>
                    </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                    <div class="info-card" style="padding: 1rem; text-align: center;">
                        <div style="font-size: 1.4rem; color: #5b7cff; font-weight: 700;">{sentence_count}</div>
                        <div style="color: #9aa4b2; margin-top: 0.4rem;">Sentences</div>
                    </div>
                """, unsafe_allow_html=True)
            with col4:
                st.markdown(f"""
                    <div class="info-card" style="padding: 1rem; text-align: center;">
                        <div style="font-size: 1.4rem; color: #5b7cff; font-weight: 700;">{len(words)}</div>
                        <div style="color: #9aa4b2; margin-top: 0.4rem;">Unique Words</div>
                    </div>
                """, unsafe_allow_html=True)

            # Visualizations (use visualization helpers for consistent, advanced charts)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### 🎯 Prediction Confidence")
                fig_gauge = confidence_gauge(confidence, result == 1, show_threshold=True)
                st.plotly_chart(fig_gauge, use_container_width=True)
            with col2:
                st.markdown("#### 📈 Classification Probabilities")
                fig_prob = probability_bar(ham_prob, spam_prob)
                st.plotly_chart(fig_prob, use_container_width=True)

            # Top words / Wordcloud
            if top_words:
                st.markdown("#### 🔤 Top Words in Message")
                # show wordcloud on left and bar on right in a responsive layout
                col1, col2 = st.columns([1, 1])
                with col1:
                    fig_wc = wordcloud_figure(dict(word_freq))
                    st.plotly_chart(fig_wc, use_container_width=True)
                with col2:
                    fig_words = top_words_bar(words_list, freq_list, spam_wordset=spam_words_set)
                    st.plotly_chart(fig_words, use_container_width=True)

            # Message characteristics charts
            st.markdown("#### 📊 Message Characteristics")
            col1, col2 = st.columns(2)
            with col1:
                labels = ['Characters (no spaces)', 'Spaces']
                values = [char_count_no_spaces, char_count - char_count_no_spaces]
                fig_chars = characters_pie(labels, values)
                st.plotly_chart(fig_chars, use_container_width=True)
            with col2:
                word_lengths = [len(word) for word in words if word]
                if word_lengths:
                    length_counts = Counter(word_lengths)
                    lengths = sorted(length_counts.keys())
                    counts = [length_counts[l] for l in lengths]
                    fig_length = word_length_line(lengths, counts)
                    st.plotly_chart(fig_length, use_container_width=True)
                else:
                    st.info("No words to analyze")

            # Detailed Analysis: patterns, URLs, numbers, punctuation, uppercase ratio
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 🔍 Detailed Analysis: What Makes This Message Spam or Safe?")

            url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
            urls = re.findall(url_pattern, input_sms)
            url_count = len(urls)
            numbers = re.findall(r'\d+', input_sms)
            number_count = len(numbers)
            exclamation_count = input_sms.count('!')
            question_count = input_sms.count('?')
            uppercase_count = sum(1 for c in input_sms if c.isupper())
            uppercase_ratio = uppercase_count / char_count if char_count > 0 else 0

            spam_patterns = {
                'Free/Freebie': bool(re.search(r'\bfree\b', input_sms, re.IGNORECASE)),
                'Win/Prize': bool(re.search(r'\b(win|won|prize|award)\b', input_sms, re.IGNORECASE)),
                'Urgent': bool(re.search(r'\burgent\b', input_sms, re.IGNORECASE)),
                'Click Here': bool(re.search(r'\bclick\b', input_sms, re.IGNORECASE)),
                'Limited Time': bool(re.search(r'\b(limited|time|offer|expire)\b', input_sms, re.IGNORECASE)),
                'Money/Cash': bool(re.search(r'\b(money|cash|dollar|£|€|$)\b', input_sms, re.IGNORECASE)),
                'Congratulations': bool(re.search(r'\bcongrat\b', input_sms, re.IGNORECASE)),
            }

            ham_patterns = {
                'Personal Greeting': bool(re.search(r'\b(hi|hello|hey|dear|thanks|thank you)\b', input_sms, re.IGNORECASE)),
                'Personal Pronouns': bool(re.search(r'\b(i|you|we|they|me|us)\b', input_sms, re.IGNORECASE)),
                'Question Words': bool(re.search(r'\b(what|when|where|why|how|who)\b', input_sms, re.IGNORECASE)),
                'Casual Language': bool(re.search(r'\b(ok|yeah|sure|maybe|probably)\b', input_sms, re.IGNORECASE)),
            }

            message_words_lower = [w.lower() for w in words]
            found_spam_words = [w for w in message_words_lower if w in spam_words_set]
            found_ham_words = [w for w in message_words_lower if w in ham_words_set]

            spam_indicators = sum(spam_patterns.values()) + len(found_spam_words) + (1 if url_count > 0 else 0) + (1 if exclamation_count > 3 else 0) + (1 if uppercase_ratio > 0.3 else 0)
            ham_indicators = sum(ham_patterns.values()) + len(found_ham_words)

            # Two-column analysis summary
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                    <div class="info-card" style="padding: 1rem; text-align: left;">
                        <h4 style="color: #ff8a8a; margin-bottom: 0.6rem;">🚨 Spam Indicators Found</h4>
                """, unsafe_allow_html=True)
                spam_patterns_found = [k for k, v in spam_patterns.items() if v]
                if spam_patterns_found:
                    st.markdown("**Patterns Detected:**")
                    for pattern in spam_patterns_found:
                        st.markdown(f"• {pattern}")
                else:
                    st.markdown("• No common spam patterns detected")

                if found_spam_words:
                    st.markdown(f"<br><strong>Common Spam Words Found ({len(found_spam_words)}):</strong>", unsafe_allow_html=True)
                    spam_words_display = ", ".join(found_spam_words[:10])
                    st.markdown(f"• {spam_words_display}")
                    if len(found_spam_words) > 10:
                        st.markdown(f"• ... and {len(found_spam_words) - 10} more")
                else:
                    st.markdown("<br><strong>Common Spam Words:</strong> None found", unsafe_allow_html=True)

                st.markdown("<br><strong>Other Indicators:</strong>", unsafe_allow_html=True)
                if url_count > 0:
                    st.markdown(f"• Contains {url_count} URL(s)")
                if exclamation_count > 3:
                    st.markdown(f"• Excessive exclamation marks ({exclamation_count})")
                if uppercase_ratio > 0.3:
                    st.markdown(f"• High uppercase ratio ({uppercase_ratio*100:.1f}%)")
                if number_count > 5:
                    st.markdown(f"• Many numbers detected ({number_count})")

                st.markdown("</div>", unsafe_allow_html=True)

            with col2:
                st.markdown("""
                    <div class="info-card" style="padding: 1rem; text-align: left;">
                        <h4 style="color: #7bd389; margin-bottom: 0.6rem;">✅ Safe (Ham) Indicators Found</h4>
                """, unsafe_allow_html=True)

                ham_patterns_found = [k for k, v in ham_patterns.items() if v]
                if ham_patterns_found:
                    st.markdown("**Patterns Detected:**")
                    for pattern in ham_patterns_found:
                        st.markdown(f"• {pattern}")
                else:
                    st.markdown("• No common safe patterns detected")

                if found_ham_words:
                    st.markdown(f"<br><strong>Common Safe Words Found ({len(found_ham_words)}):</strong>", unsafe_allow_html=True)
                    ham_words_display = ", ".join(found_ham_words[:10])
                    st.markdown(f"• {ham_words_display}")
                    if len(found_ham_words) > 10:
                        st.markdown(f"• ... and {len(found_ham_words) - 10} more")
                else:
                    st.markdown("<br><strong>Common Safe Words:</strong> None found", unsafe_allow_html=True)

                st.markdown("<br><strong>Other Indicators:</strong>", unsafe_allow_html=True)
                if url_count == 0:
                    st.markdown("• No suspicious URLs")
                if exclamation_count <= 1:
                    st.markdown("• Normal punctuation usage")
                if uppercase_ratio < 0.1:
                    st.markdown("• Normal capitalization")

                st.markdown("</div>", unsafe_allow_html=True)

            # Summary Explanation (keeps wording identical but uses same card look)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
                <div class="info-card" style="padding: 1.25rem; text-align: left;">
                    <h4 style="color: #5b7cff; margin-bottom: 0.6rem;">📝 Classification Summary</h4>
            """, unsafe_allow_html=True)

            if result == 1:
                st.markdown(f"""
                    <p style="color: #ff6b6b; font-weight: 600; margin-bottom: 0.6rem;">
                        This message was classified as <strong>SPAM</strong> because:
                    </p>
                    <ul style="color: #9aa4b2; line-height: 1.8;">
                        <li>It contains <strong>{spam_indicators} spam indicator(s)</strong> compared to <strong>{ham_indicators} safe indicator(s)</strong></li>
                        <li>The model assigned a <strong>{spam_prob:.1f}% probability</strong> that this is spam</li>
                """, unsafe_allow_html=True)

                if spam_patterns_found:
                    st.markdown(f"<li>Detected spam patterns: {', '.join(spam_patterns_found)}</li>", unsafe_allow_html=True)
                if found_spam_words:
                    st.markdown(f"<li>Contains words commonly found in spam messages</li>", unsafe_allow_html=True)
                if url_count > 0:
                    st.markdown(f"<li>Contains {url_count} URL(s) which may be suspicious</li>", unsafe_allow_html=True)

                st.markdown("</ul>", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <p style="color: #4facfe; font-weight: 600; margin-bottom: 0.6rem;">
                        This message was classified as <strong>SAFE (HAM)</strong> because:
                    </p>
                    <ul style="color: #9aa4b2; line-height: 1.8;">
                        <li>It contains <strong>{ham_indicators} safe indicator(s)</strong> compared to <strong>{spam_indicators} spam indicator(s)</strong></li>
                        <li>The model assigned a <strong>{ham_prob:.1f}% probability</strong> that this is safe</li>
                """, unsafe_allow_html=True)

                if ham_patterns_found:
                    st.markdown(f"<li>Contains natural language patterns typical of legitimate messages</li>", unsafe_allow_html=True)
                if found_ham_words:
                    st.markdown(f"<li>Contains words commonly found in safe messages</li>", unsafe_allow_html=True)
                if url_count == 0:
                    st.markdown(f"<li>No suspicious URLs detected</li>", unsafe_allow_html=True)

                st.markdown("</ul>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

            # Annotated message: highlight spam/ham words inline
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### 🧾 Annotated Message (highlights spam/ham indicative words)")
            annotated_html = annotated_message_html(input_sms, spam_words=spam_words_set, ham_words=ham_words_set)
            st.markdown(annotated_html, unsafe_allow_html=True)

# Info Section and Key Features (keeps content unchanged but uses helper to render the cards)
st.markdown("---")
st.markdown("### ℹ️ How It Works")
cards = [
    {"icon": "🔍", "title": "Text Analysis", "desc": "Advanced NLP techniques analyze your message content, structure, and patterns"},
    {"icon": "🤖", "title": "AI Detection", "desc": "Machine learning model trained on thousands of messages identifies spam patterns"},
    {"icon": "⚡", "title": "Instant Results", "desc": "Get immediate feedback with confidence scores on message safety"},
]
render_info_cards(cards)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 🎯 Key Features")
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div class="info-card" style="text-align: left; padding: 1rem;">
        <div style="font-size: 1.05rem; margin-bottom: 0.5rem;">🔒 <strong style="color: #5b7cff;">Privacy First</strong></div>
        <div class="info-desc" style="text-align: left;">Your messages are processed securely and never stored</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="info-card" style="text-align: left; padding: 1rem;">
        <div style="font-size: 1.05rem; margin-bottom: 0.5rem;">📊 <strong style="color: #5b7cff;">High Accuracy</strong></div>
        <div class="info-desc" style="text-align: left;">Trained on extensive datasets for reliable detection</div>
    </div>
    """, unsafe_allow_html=True)
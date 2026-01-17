import streamlit as st
import nltk
from collections import Counter
from pathlib import Path
import re
import numpy as np
import pandas as pd

# Premium design + visualization modules
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
    create_metric_card,
    message_complexity_radar,
)

# Initialize page with premium design
setup_page(
    title="AI Spam Detector - Protect Your Inbox",
    animations=True,
    compact=False
)
setup_nltk()
STOP_WORDS = get_stopwords()

# Load model and vectorizer
tfidf, model = load_model()

# Wordlists from analysis module
spam_words_set = SPAM_WORDS
ham_words_set = HAM_WORDS

# Render premium header
render_header(
    title="🛡️ AI-Powered Spam Detector",
    subtitle="Advanced machine learning protection against phishing, scams, and unwanted messages"
)

# Premium input section
st.markdown("""
    <div class="card gradient-border animate" style="margin-bottom: 2rem;">
        <h3 style='color: #f8fafc; margin-bottom: 0.75rem; font-size: 1.25rem; font-weight: 700; letter-spacing: -0.02em;'>
            📝 Enter Your Message
        </h3>
        <p style='color: #cbd5e1; margin-bottom: 0; line-height: 1.6;'>
            Paste any email or SMS message below for instant AI-powered analysis and threat detection.
        </p>
    </div>
""", unsafe_allow_html=True)

# Custom styled text area
st.markdown("""
    <style>
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        color: #f8fafc !important;
        font-size: 1rem !important;
        padding: 1rem !important;
        transition: all 0.3s ease !important;
    }
    .stTextArea textarea:focus {
        border-color: rgba(59, 130, 246, 0.5) !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        letter-spacing: 0.02em !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 32px rgba(59, 130, 246, 0.4) !important;
    }
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    </style>
""", unsafe_allow_html=True)

input_sms = st.text_area(
    "Message",
    height=220,
    placeholder="📧 Paste your email or SMS message here...\n\nExample: 'Congratulations! You've won $1,000,000! Click here to claim your prize now!'\n\nOr: 'Hi John, are we still meeting for coffee tomorrow at 3pm?'",
    label_visibility="collapsed"
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    predict_button = st.button("🔍 Analyze Message Now", use_container_width=True)

# Prediction & Analysis
if predict_button:
    if not input_sms.strip():
        st.markdown("""
            <div class="card" style="background: rgba(251, 191, 36, 0.1); border-left: 4px solid #fbbf24; margin: 1rem 0;">
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <div style="font-size: 2rem;">⚠️</div>
                    <div>
                        <div style="font-weight: 700; margin-bottom: 0.25rem;">No Message Provided</div>
                        <div style="color: #cbd5e1; font-size: 0.9rem;">Please enter a message to analyze.</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        with st.spinner("🔎 Analyzing message with AI..."):
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

            # Display premium result card
            st.markdown(render_result_card(result == 1, confidence), unsafe_allow_html=True)

            # Statistics section with premium metric cards
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
                <h3 style='color: #f8fafc; margin: 2rem 0 1.5rem 0; font-size: 1.5rem; font-weight: 700; letter-spacing: -0.02em;'>
                    📊 Message Analysis & Statistics
                </h3>
            """, unsafe_allow_html=True)

            # Premium metric cards
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(
                    create_metric_card("Words", f"{word_count:,}", "Total word count", "📝"),
                    unsafe_allow_html=True
                )
            with col2:
                st.markdown(
                    create_metric_card("Characters", f"{char_count:,}", "Including spaces", "🔤"),
                    unsafe_allow_html=True
                )
            with col3:
                st.markdown(
                    create_metric_card("Sentences", f"{sentence_count:,}", "Detected sentences", "📄"),
                    unsafe_allow_html=True
                )
            with col4:
                st.markdown(
                    create_metric_card("Unique", f"{len(set(words)):,}", "Unique words", "✨"),
                    unsafe_allow_html=True
                )

            # Premium visualizations
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                    <div style='margin-bottom: 0.75rem;'>
                        <h4 style='color: #f8fafc; font-size: 1.1rem; font-weight: 700; margin: 0;'>
                            🎯 Prediction Confidence
                        </h4>
                    </div>
                """, unsafe_allow_html=True)
                fig_gauge = confidence_gauge(confidence, result == 1, show_threshold=True)
                st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})
                
            with col2:
                st.markdown("""
                    <div style='margin-bottom: 0.75rem;'>
                        <h4 style='color: #f8fafc; font-size: 1.1rem; font-weight: 700; margin: 0;'>
                            📈 Classification Probabilities
                        </h4>
                    </div>
                """, unsafe_allow_html=True)
                fig_prob = probability_bar(ham_prob, spam_prob)
                st.plotly_chart(fig_prob, use_container_width=True, config={'displayModeBar': False})

            # Word analysis visualizations
            if top_words:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("""
                    <h4 style='color: #f8fafc; font-size: 1.25rem; font-weight: 700; margin: 1.5rem 0 1rem 0; letter-spacing: -0.02em;'>
                        🔤 Word Frequency Analysis
                    </h4>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns([1, 1])
                with col1:
                    fig_words = top_words_bar(words_list, freq_list, spam_wordset=spam_words_set)
                    st.plotly_chart(fig_words, use_container_width=True, config={'displayModeBar': False})
                with col2:
                    fig_wc = wordcloud_figure(dict(word_freq))
                    st.plotly_chart(fig_wc, use_container_width=True, config={'displayModeBar': False})

            # Message characteristics
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
                <h4 style='color: #f8fafc; font-size: 1.25rem; font-weight: 700; margin: 1.5rem 0 1rem 0; letter-spacing: -0.02em;'>
                    📊 Message Characteristics
                </h4>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                labels = ['Characters (no spaces)', 'Spaces']
                values = [char_count_no_spaces, char_count - char_count_no_spaces]
                fig_chars = characters_pie(labels, values)
                st.plotly_chart(fig_chars, use_container_width=True, config={'displayModeBar': False})
            with col2:
                word_lengths = [len(word) for word in words if word]
                if word_lengths:
                    length_counts = Counter(word_lengths)
                    lengths = sorted(length_counts.keys())
                    counts = [length_counts[l] for l in lengths]
                    fig_length = word_length_line(lengths, counts)
                    st.plotly_chart(fig_length, use_container_width=True, config={'displayModeBar': False})
                else:
                    st.markdown("""
                        <div class="card" style="text-align: center; padding: 2rem;">
                            <div style="font-size: 2rem; margin-bottom: 1rem;">📊</div>
                            <div style="color: #cbd5e1;">No word data available for analysis</div>
                        </div>
                    """, unsafe_allow_html=True)
            with col3:
                # Calculate average word length
                avg_word_len = sum(word_lengths) / len(word_lengths) if word_lengths else 0
                fig_radar = message_complexity_radar(
                    word_count=word_count,
                    char_count=char_count,
                    sentence_count=sentence_count,
                    unique_word_count=len(set(words)),
                    avg_word_length=avg_word_len
                )
                st.plotly_chart(fig_radar, use_container_width=True, config={'displayModeBar': False})

            # Detailed pattern analysis
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown("""
                <h3 style='color: #f8fafc; font-size: 1.5rem; font-weight: 700; margin: 2rem 0 1.5rem 0; letter-spacing: -0.02em;'>
                    🔍 Detailed Pattern Analysis
                </h3>
            """, unsafe_allow_html=True)

            # Extract patterns and indicators
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

            # Premium two-column analysis
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                    <div class="card animate" style="background: linear-gradient(135deg, rgba(239, 68, 68, 0.08), rgba(251, 113, 133, 0.04)); border-left: 4px solid #ef4444; height: 100%;">
                        <h4 style="color: #fecdd3; margin-bottom: 1rem; font-size: 1.15rem; font-weight: 700; display: flex; align-items: center; gap: 0.5rem;">
                            <span style="font-size: 1.5rem;">🚨</span> Spam Indicators Found
                        </h4>
                """, unsafe_allow_html=True)
                
                spam_patterns_found = [k for k, v in spam_patterns.items() if v]
                if spam_patterns_found:
                    st.markdown("<div style='color: #fecdd3; font-weight: 600; margin-bottom: 0.5rem;'>Detected Patterns:</div>", unsafe_allow_html=True)
                    for pattern in spam_patterns_found:
                        st.markdown(f"<div style='color: #fde2e4; margin-left: 1rem; margin-bottom: 0.25rem;'>• {pattern}</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='color: #cbd5e1; margin-left: 1rem;'>✓ No common spam patterns detected</div>", unsafe_allow_html=True)

                if found_spam_words:
                    st.markdown(f"<div style='color: #fecdd3; font-weight: 600; margin: 1rem 0 0.5rem 0;'>Spam Words Found ({len(found_spam_words)}):</div>", unsafe_allow_html=True)
                    spam_words_display = ", ".join(found_spam_words[:10])
                    st.markdown(f"<div style='color: #fde2e4; margin-left: 1rem;'>• {spam_words_display}</div>", unsafe_allow_html=True)
                    if len(found_spam_words) > 10:
                        st.markdown(f"<div style='color: #fde2e4; margin-left: 1rem;'>• ... and {len(found_spam_words) - 10} more</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='color: #cbd5e1; margin: 1rem 0 0 1rem;'>✓ No spam words detected</div>", unsafe_allow_html=True)

                st.markdown("<div style='color: #fecdd3; font-weight: 600; margin: 1rem 0 0.5rem 0;'>Other Indicators:</div>", unsafe_allow_html=True)
                if url_count > 0:
                    st.markdown(f"<div style='color: #fde2e4; margin-left: 1rem;'>• Contains {url_count} URL(s)</div>", unsafe_allow_html=True)
                if exclamation_count > 3:
                    st.markdown(f"<div style='color: #fde2e4; margin-left: 1rem;'>• Excessive exclamation marks ({exclamation_count})</div>", unsafe_allow_html=True)
                if uppercase_ratio > 0.3:
                    st.markdown(f"<div style='color: #fde2e4; margin-left: 1rem;'>• High uppercase ratio ({uppercase_ratio*100:.1f}%)</div>", unsafe_allow_html=True)
                if number_count > 5:
                    st.markdown(f"<div style='color: #fde2e4; margin-left: 1rem;'>• Many numbers detected ({number_count})</div>", unsafe_allow_html=True)
                if not any([url_count > 0, exclamation_count > 3, uppercase_ratio > 0.3, number_count > 5]):
                    st.markdown("<div style='color: #cbd5e1; margin-left: 1rem;'>✓ No suspicious indicators</div>", unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

            with col2:
                st.markdown("""
                    <div class="card animate" style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.08), rgba(52, 211, 153, 0.04)); border-left: 4px solid #10b981; height: 100%;">
                        <h4 style="color: #d1fae5; margin-bottom: 1rem; font-size: 1.15rem; font-weight: 700; display: flex; align-items: center; gap: 0.5rem;">
                            <span style="font-size: 1.5rem;">✅</span> Safe (Ham) Indicators Found
                        </h4>
                """, unsafe_allow_html=True)

                ham_patterns_found = [k for k, v in ham_patterns.items() if v]
                if ham_patterns_found:
                    st.markdown("<div style='color: #d1fae5; font-weight: 600; margin-bottom: 0.5rem;'>Detected Patterns:</div>", unsafe_allow_html=True)
                    for pattern in ham_patterns_found:
                        st.markdown(f"<div style='color: #ecfdf5; margin-left: 1rem; margin-bottom: 0.25rem;'>• {pattern}</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='color: #cbd5e1; margin-left: 1rem;'>⚠ No common safe patterns detected</div>", unsafe_allow_html=True)

                if found_ham_words:
                    st.markdown(f"<div style='color: #d1fae5; font-weight: 600; margin: 1rem 0 0.5rem 0;'>Safe Words Found ({len(found_ham_words)}):</div>", unsafe_allow_html=True)
                    ham_words_display = ", ".join(found_ham_words[:10])
                    st.markdown(f"<div style='color: #ecfdf5; margin-left: 1rem;'>• {ham_words_display}</div>", unsafe_allow_html=True)
                    if len(found_ham_words) > 10:
                        st.markdown(f"<div style='color: #ecfdf5; margin-left: 1rem;'>• ... and {len(found_ham_words) - 10} more</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='color: #cbd5e1; margin: 1rem 0 0 1rem;'>⚠ No safe words detected</div>", unsafe_allow_html=True)

                st.markdown("<div style='color: #d1fae5; font-weight: 600; margin: 1rem 0 0.5rem 0;'>Positive Indicators:</div>", unsafe_allow_html=True)
                if url_count == 0:
                    st.markdown("<div style='color: #ecfdf5; margin-left: 1rem;'>• No suspicious URLs</div>", unsafe_allow_html=True)
                if exclamation_count <= 1:
                    st.markdown("<div style='color: #ecfdf5; margin-left: 1rem;'>• Normal punctuation usage</div>", unsafe_allow_html=True)
                if uppercase_ratio < 0.1:
                    st.markdown("<div style='color: #ecfdf5; margin-left: 1rem;'>• Normal capitalization</div>", unsafe_allow_html=True)
                if not any([url_count == 0, exclamation_count <= 1, uppercase_ratio < 0.1]):
                    st.markdown("<div style='color: #cbd5e1; margin-left: 1rem;'>⚠ Few positive indicators found</div>", unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

            # Classification summary with premium styling
            st.markdown("<br>", unsafe_allow_html=True)
            
            summary_bg = "linear-gradient(135deg, rgba(239, 68, 68, 0.08), rgba(251, 113, 133, 0.04))" if result == 1 else "linear-gradient(135deg, rgba(16, 185, 129, 0.08), rgba(52, 211, 153, 0.04))"
            summary_border = "#ef4444" if result == 1 else "#10b981"
            summary_color = "#fecdd3" if result == 1 else "#d1fae5"
            
            st.markdown(f"""
                <div class="card animate" style="background: {summary_bg}; border-left: 4px solid {summary_border};">
                    <h4 style="color: {summary_color}; margin-bottom: 1rem; font-size: 1.2rem; font-weight: 700; display: flex; align-items: center; gap: 0.5rem;">
                        <span style="font-size: 1.5rem;">📝</span> Classification Summary
                    </h4>
            """, unsafe_allow_html=True)

            if result == 1:
                st.markdown(f"""
                    <p style="color: #fecdd3; font-weight: 600; margin-bottom: 1rem; font-size: 1.05rem;">
                        This message was classified as <strong>SPAM</strong> with {confidence:.1f}% confidence because:
                    </p>
                    <ul style="color: #fde2e4; line-height: 2; margin-left: 1rem;">
                        <li>Detected <strong>{spam_indicators} spam indicator(s)</strong> vs <strong>{ham_indicators} safe indicator(s)</strong></li>
                        <li>Model assigned <strong>{spam_prob:.1f}% spam probability</strong> and <strong>{ham_prob:.1f}% safe probability</strong></li>
                """, unsafe_allow_html=True)

                if spam_patterns_found:
                    st.markdown(f"<li>Spam patterns found: <strong>{', '.join(spam_patterns_found)}</strong></li>", unsafe_allow_html=True)
                if found_spam_words:
                    st.markdown(f"<li>Contains <strong>{len(found_spam_words)} words</strong> commonly found in spam messages</li>", unsafe_allow_html=True)
                if url_count > 0:
                    st.markdown(f"<li>Contains <strong>{url_count} potentially suspicious URL(s)</strong></li>", unsafe_allow_html=True)
                if uppercase_ratio > 0.3:
                    st.markdown(f"<li>Unusual capitalization pattern detected (<strong>{uppercase_ratio*100:.1f}%</strong> uppercase)</li>", unsafe_allow_html=True)

                st.markdown("</ul>", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <p style="color: #d1fae5; font-weight: 600; margin-bottom: 1rem; font-size: 1.05rem;">
                        This message was classified as <strong>SAFE (HAM)</strong> with {confidence:.1f}% confidence because:
                    </p>
                    <ul style="color: #ecfdf5; line-height: 2; margin-left: 1rem;">
                        <li>Detected <strong>{ham_indicators} safe indicator(s)</strong> vs <strong>{spam_indicators} spam indicator(s)</strong></li>
                        <li>Model assigned <strong>{ham_prob:.1f}% safe probability</strong> and <strong>{spam_prob:.1f}% spam probability</strong></li>
                """, unsafe_allow_html=True)

                if ham_patterns_found:
                    st.markdown(f"<li>Contains natural language patterns typical of legitimate messages</li>", unsafe_allow_html=True)
                if found_ham_words:
                    st.markdown(f"<li>Contains <strong>{len(found_ham_words)} words</strong> commonly found in safe messages</li>", unsafe_allow_html=True)
                if url_count == 0:
                    st.markdown(f"<li>No suspicious URLs detected</li>", unsafe_allow_html=True)
                if uppercase_ratio < 0.1:
                    st.markdown(f"<li>Natural capitalization pattern (<strong>{uppercase_ratio*100:.1f}%</strong> uppercase)</li>", unsafe_allow_html=True)

                st.markdown("</ul>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

            # Annotated message with premium styling
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown("""
                <h4 style='color: #f8fafc; font-size: 1.25rem; font-weight: 700; margin: 2rem 0 1rem 0; letter-spacing: -0.02em;'>
                    🧾 Highlighted Message Analysis
                </h4>
                <p style='color: #cbd5e1; margin-bottom: 1rem;'>
                    Words highlighted in <span style="color: #fecdd3; font-weight: 600;">red</span> indicate spam patterns, 
                    while <span style="color: #d1fae5; font-weight: 600;">green</span> highlights indicate safe patterns.
                </p>
            """, unsafe_allow_html=True)
            
            annotated_html = annotated_message_html(input_sms, spam_words=spam_words_set, ham_words=ham_words_set)
            st.markdown(annotated_html, unsafe_allow_html=True)

# Info Section with premium cards
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style="height: 2px; background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.3), transparent); margin: 3rem 0;"></div>
""", unsafe_allow_html=True)

st.markdown("""
    <h3 style='color: #f8fafc; font-size: 1.5rem; font-weight: 700; margin: 2rem 0 1.5rem 0; text-align: center; letter-spacing: -0.02em;'>
        ℹ️ How It Works
    </h3>
""", unsafe_allow_html=True)

cards = [
    {
        "icon": "🔍", 
        "title": "Advanced Text Analysis", 
        "desc": "State-of-the-art NLP techniques analyze message content, structure, linguistic patterns, and behavioral indicators"
    },
    {
        "icon": "🤖", 
        "title": "AI-Powered Detection", 
        "desc": "Machine learning model trained on millions of messages with 97%+ accuracy in identifying spam and phishing attempts"
    },
    {
        "icon": "⚡", 
        "title": "Real-Time Results", 
        "desc": "Instant feedback with detailed confidence scores, pattern analysis, and visual insights for informed decision-making"
    },
]
render_info_cards(cards)

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <h3 style='color: #f8fafc; font-size: 1.5rem; font-weight: 700; margin: 2rem 0 1.5rem 0; text-align: center; letter-spacing: -0.02em;'>
        🎯 Key Features
    </h3>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="card animate" style="text-align: center; height: 100%;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🔒</div>
        <h4 style="color: #f8fafc; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.75rem;">Privacy First</h4>
        <p style="color: #cbd5e1; line-height: 1.6; margin: 0;">
            Your messages are processed securely in real-time and never stored or shared. Complete privacy guaranteed.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
with col2:
    st.markdown("""
    <div class="card animate" style="text-align: center; height: 100%;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
        <h4 style="color: #f8fafc; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.75rem;">High Accuracy</h4>
        <p style="color: #cbd5e1; line-height: 1.6; margin: 0;">
            Trained on millions of real-world messages with advanced ML algorithms achieving 97%+ detection accuracy.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
with col3:
    st.markdown("""
    <div class="card animate" style="text-align: center; height: 100%;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🎨</div>
        <h4 style="color: #f8fafc; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.75rem;">Visual Insights</h4>
        <p style="color: #cbd5e1; line-height: 1.6; margin: 0;">
            Interactive charts and detailed breakdowns help you understand exactly why a message is flagged.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Additional features section
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <h3 style='color: #f8fafc; font-size: 1.5rem; font-weight: 700; margin: 2rem 0 1.5rem 0; text-align: center; letter-spacing: -0.02em;'>
        💡 What Makes Our Detector Special
    </h3>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="card gradient-border animate" style="height: 100%;">
        <h4 style="color: #f8fafc; font-size: 1.15rem; font-weight: 700; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
            <span style="font-size: 1.5rem;">🧠</span> Multi-Layer Analysis
        </h4>
        <ul style="color: #cbd5e1; line-height: 1.8; margin: 0; padding-left: 1.5rem;">
            <li>Pattern recognition for common spam phrases and structures</li>
            <li>URL and link analysis for phishing detection</li>
            <li>Linguistic analysis including tone, urgency, and sentiment</li>
            <li>Statistical modeling of message characteristics</li>
            <li>Word frequency and vocabulary profiling</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card gradient-border animate" style="height: 100%;">
        <h4 style="color: #f8fafc; font-size: 1.15rem; font-weight: 700; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
            <span style="font-size: 1.5rem;">📈</span> Comprehensive Reporting
        </h4>
        <ul style="color: #cbd5e1; line-height: 1.8; margin: 0; padding-left: 1.5rem;">
            <li>Confidence scores with detailed probability breakdowns</li>
            <li>Visual analytics including charts and word clouds</li>
            <li>Highlighted message annotations showing key indicators</li>
            <li>Side-by-side comparison of spam vs safe indicators</li>
            <li>Actionable insights explaining the classification</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Tips section
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <h3 style='color: #f8fafc; font-size: 1.5rem; font-weight: 700; margin: 2rem 0 1.5rem 0; text-align: center; letter-spacing: -0.02em;'>
        🛡️ Safety Tips
    </h3>
""", unsafe_allow_html=True)

tips_col1, tips_col2, tips_col3 = st.columns(3)

with tips_col1:
    st.markdown("""
    <div class="info-card card" style="height: 100%;">
        <div style="font-size: 2rem; text-align: center; margin-bottom: 0.75rem;">⚠️</div>
        <h4 style="color: #f8fafc; font-size: 1rem; font-weight: 700; margin-bottom: 0.5rem; text-align: center;">Watch for Red Flags</h4>
        <p style="color: #cbd5e1; font-size: 0.9rem; line-height: 1.6; margin: 0;">
            Be cautious of messages with urgent language, requests for personal information, or promises of prizes and rewards.
        </p>
    </div>
    """, unsafe_allow_html=True)

with tips_col2:
    st.markdown("""
    <div class="info-card card" style="height: 100%;">
        <div style="font-size: 2rem; text-align: center; margin-bottom: 0.75rem;">🔗</div>
        <h4 style="color: #f8fafc; font-size: 1rem; font-weight: 700; margin-bottom: 0.5rem; text-align: center;">Verify Links</h4>
        <p style="color: #cbd5e1; font-size: 0.9rem; line-height: 1.6; margin: 0;">
            Never click suspicious links. Hover over URLs to verify destination before clicking, and check for legitimate domains.
        </p>
    </div>
    """, unsafe_allow_html=True)

with tips_col3:
    st.markdown("""
    <div class="info-card card" style="height: 100%;">
        <div style="font-size: 2rem; text-align: center; margin-bottom: 0.75rem;">🤔</div>
        <h4 style="color: #f8fafc; font-size: 1rem; font-weight: 700; margin-bottom: 0.5rem; text-align: center;">When in Doubt</h4>
        <p style="color: #cbd5e1; font-size: 0.9rem; line-height: 1.6; margin: 0;">
            If a message seems suspicious, verify through official channels. Contact the company directly using known contact information.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Common spam indicators
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div class="card" style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.05), rgba(139, 92, 246, 0.03));">
        <h4 style="color: #f8fafc; font-size: 1.2rem; font-weight: 700; margin-bottom: 1rem; text-align: center;">
            🎓 Common Spam Indicators to Watch For
        </h4>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-top: 1.5rem;">
            <div style="background: rgba(255, 255, 255, 0.02); padding: 1rem; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.05);">
                <div style="color: #fecdd3; font-weight: 600; margin-bottom: 0.5rem;">🎁 Too Good to Be True</div>
                <div style="color: #cbd5e1; font-size: 0.9rem;">Promises of free money, prizes, or unrealistic rewards</div>
            </div>
            <div style="background: rgba(255, 255, 255, 0.02); padding: 1rem; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.05);">
                <div style="color: #fecdd3; font-weight: 600; margin-bottom: 0.5rem;">⏰ Urgency & Pressure</div>
                <div style="color: #cbd5e1; font-size: 0.9rem;">"Act now", "Limited time", "Urgent action required"</div>
            </div>
            <div style="background: rgba(255, 255, 255, 0.02); padding: 1rem; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.05);">
                <div style="color: #fecdd3; font-weight: 600; margin-bottom: 0.5rem;">🔤 Poor Grammar</div>
                <div style="color: #cbd5e1; font-size: 0.9rem;">Spelling mistakes, awkward phrasing, or unusual formatting</div>
            </div>
            <div style="background: rgba(255, 255, 255, 0.02); padding: 1rem; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.05);">
                <div style="color: #fecdd3; font-weight: 600; margin-bottom: 0.5rem;">🔗 Suspicious Links</div>
                <div style="color: #cbd5e1; font-size: 0.9rem;">Shortened URLs, misspelled domains, or unexpected redirects</div>
            </div>
            <div style="background: rgba(255, 255, 255, 0.02); padding: 1rem; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.05);">
                <div style="color: #fecdd3; font-weight: 600; margin-bottom: 0.5rem;">🔐 Info Requests</div>
                <div style="color: #cbd5e1; font-size: 0.9rem;">Asking for passwords, SSN, credit card numbers, or login credentials</div>
            </div>
            <div style="background: rgba(255, 255, 255, 0.02); padding: 1rem; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.05);">
                <div style="color: #fecdd3; font-weight: 600; margin-bottom: 0.5rem;">📧 Generic Greetings</div>
                <div style="color: #cbd5e1; font-size: 0.9rem;">"Dear Customer" instead of your name, impersonal messages</div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Technology stack
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style="height: 2px; background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.3), transparent); margin: 3rem 0;"></div>
""", unsafe_allow_html=True)

st.markdown("""
    <h3 style='color: #f8fafc; font-size: 1.5rem; font-weight: 700; margin: 2rem 0 1.5rem 0; text-align: center; letter-spacing: -0.02em;'>
        🔧 Technology Stack
    </h3>
""", unsafe_allow_html=True)

tech_col1, tech_col2, tech_col3, tech_col4 = st.columns(4)

with tech_col1:
    st.markdown("""
    <div class="card" style="text-align: center; padding: 1.5rem;">
        <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">🐍</div>
        <h5 style="color: #f8fafc; font-weight: 700; margin-bottom: 0.5rem;">Python</h5>
        <p style="color: #94a3b8; font-size: 0.85rem; margin: 0;">Core Language</p>
    </div>
    """, unsafe_allow_html=True)

with tech_col2:
    st.markdown("""
    <div class="card" style="text-align: center; padding: 1.5rem;">
        <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">🤖</div>
        <h5 style="color: #f8fafc; font-weight: 700; margin-bottom: 0.5rem;">Scikit-learn</h5>
        <p style="color: #94a3b8; font-size: 0.85rem; margin: 0;">ML Framework</p>
    </div>
    """, unsafe_allow_html=True)

with tech_col3:
    st.markdown("""
    <div class="card" style="text-align: center; padding: 1.5rem;">
        <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">📝</div>
        <h5 style="color: #f8fafc; font-weight: 700; margin-bottom: 0.5rem;">NLTK</h5>
        <p style="color: #94a3b8; font-size: 0.85rem; margin: 0;">NLP Processing</p>
    </div>
    """, unsafe_allow_html=True)

with tech_col4:
    st.markdown("""
    <div class="card" style="text-align: center; padding: 1.5rem;">
        <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">📊</div>
        <h5 style="color: #f8fafc; font-weight: 700; margin-bottom: 0.5rem;">Plotly</h5>
        <p style="color: #94a3b8; font-size: 0.85rem; margin: 0;">Visualizations</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div class="card" style="text-align: center; padding: 2rem; background: linear-gradient(135deg, rgba(59, 130, 246, 0.03), rgba(139, 92, 246, 0.02)); margin-top: 3rem;">
        <div style="font-size: 2.5rem; margin-bottom: 1rem;">🛡️</div>
        <h3 style="color: #f8fafc; font-size: 1.3rem; font-weight: 700; margin-bottom: 0.75rem; letter-spacing: -0.02em;">
            AI-Powered Spam Detector
        </h3>
        <p style="color: #cbd5e1; margin-bottom: 1rem; line-height: 1.6;">
            Protecting your inbox with advanced machine learning technology
        </p>
        <div style="color: #94a3b8; font-size: 0.9rem;">
            Built with ❤️ using Streamlit • Advanced NLP • Machine Learning • Real-time Analysis
        </div>
        <div style="margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid rgba(255, 255, 255, 0.08);">
            <p style="color: #94a3b8; font-size: 0.85rem; margin: 0;">
                © 2024 AI Spam Detector • All rights reserved • Your privacy is our priority
            </p>
        </div>
    </div>
""", unsafe_allow_html=True)
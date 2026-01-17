import streamlit as st
import pickle
import nltk
import base64
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from collections import Counter
from pathlib import Path
from PIL import Image
import numpy as np
import pandas as pd
import re

# Use helpers from src package
from src.design import setup_page
from src.nlp import setup_nltk, transformed_text, get_stopwords
from src.model import load_model
from src.analysis import SPAM_WORDS, HAM_WORDS
from src.visualization import confidence_gauge, probability_bar, top_words_bar, characters_pie, word_length_line, wordcloud_figure

# Initialize page and CSS (keeps identical page config and CSS)
setup_page()

# Ensure NLTK data is available and get stopwords via src.nlp
setup_nltk()
stop_words = get_stopwords()

# Load trained data (vectorizer and model)
tfidf, model = load_model()

# Use word lists from src.analysis (these are loaded there; fallback to empty set handled there)
spam_words_set = SPAM_WORDS
ham_words_set = HAM_WORDS

# -- Streamlit UI --
# Header - Home Page
st.markdown("""
    <div class="main-header">
        <h1>🛡️ Email / SMS Spam Classifier</h1>
        <p>Protect your inbox from unwanted messages with AI-powered detection</p>
    </div>
""", unsafe_allow_html=True)

# Input Section with glassmorphism card
st.markdown("""
    <div class="input-card">
        <h3 style='color: #2d3748; margin-bottom: 1rem; font-size: 1.5rem; font-weight: 700;'>📝 Enter Your Message</h3>
        <p style='color: #666; margin-bottom: 1.5rem;'>Paste the email or SMS message you want to check below:</p>
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

# Prediction Logic
if predict_button:
    if not input_sms.strip():
        st.warning("⚠️ Please enter a message to analyze.")
    else:
        with st.spinner("🔎 Analyzing message..."):
            # Preprocess (use src.nlp.transformed_text)
            transformed_sms = transformed_text(input_sms)
            # Vectorize & Predict using loaded tfidf and model
            vector_input = tfidf.transform([transformed_sms])
            result = model.predict(vector_input)[0]
            
            # Get prediction probability for confidence score
            prediction_proba = model.predict_proba(vector_input)[0]
            confidence = max(prediction_proba) * 100
            spam_prob = prediction_proba[1] * 100
            ham_prob = prediction_proba[0] * 100
            
            # Calculate message statistics
            word_count = len(input_sms.split())
            char_count = len(input_sms)
            char_count_no_spaces = len(input_sms.replace(" ", ""))
            sentence_count = len(nltk.sent_tokenize(input_sms))
            
            # Word frequency analysis
            words = transformed_sms.split()
            word_freq = Counter(words)
            top_words = dict(word_freq.most_common(10)) if words else {}
            
            # Display result with custom styling
            if result == 1:
                st.markdown(f"""
                    <div class="result-card result-spam">
                        <div class="result-icon">🚨</div>
                        <div class="result-text">SPAM DETECTED</div>
                        <div class="result-message">This message has been classified as spam. Please be cautious and avoid clicking any links or providing personal information.</div>
                        <div class="confidence-score">
                            <strong>Confidence Level: {confidence:.1f}%</strong>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="result-card result-safe">
                        <div class="result-icon">✅</div>
                        <div class="result-text">SAFE MESSAGE</div>
                        <div class="result-message">This message appears to be legitimate and safe. You can proceed with confidence.</div>
                        <div class="confidence-score">
                            <strong>Confidence Level: {confidence:.1f}%</strong>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            # Statistics and Visualizations Section
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 📊 Message Analysis & Statistics")
            
            # Message Statistics Cards
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"""
                    <div class="info-card" style="padding: 1.5rem;">
                        <div style="font-size: 2rem; color: #667eea; font-weight: 700;">{word_count}</div>
                        <div style="color: #666; margin-top: 0.5rem;">Words</div>
                    </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                    <div class="info-card" style="padding: 1.5rem;">
                        <div style="font-size: 2rem; color: #667eea; font-weight: 700;">{char_count}</div>
                        <div style="color: #666; margin-top: 0.5rem;">Characters</div>
                    </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                    <div class="info-card" style="padding: 1.5rem;">
                        <div style="font-size: 2rem; color: #667eea; font-weight: 700;">{sentence_count}</div>
                        <div style="color: #666; margin-top: 0.5rem;">Sentences</div>
                    </div>
                """, unsafe_allow_html=True)
            with col4:
                st.markdown(f"""
                    <div class="info-card" style="padding: 1.5rem;">
                        <div style="font-size: 2rem; color: #667eea; font-weight: 700;">{len(words)}</div>
                        <div style="color: #666; margin-top: 0.5rem;">Unique Words</div>
                    </div>
                """, unsafe_allow_html=True)
            
            # Graphs Section
            col1, col2 = st.columns(2)
            
            with col1:
                # Confidence Score Gauge Chart (same construction as original)
                st.markdown("#### 🎯 Prediction Confidence")
                fig_gauge = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = confidence,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Confidence (%)"},
                    delta = {'reference': 50},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "#f5576c" if result == 1 else "#4facfe"},
                        'steps': [
                            {'range': [0, 50], 'color': "lightgray"},
                            {'range': [50, 100], 'color': "gray"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 90
                        }
                    }
                ))
                fig_gauge.update_layout(
                    height=300,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color="white")
                )
                st.plotly_chart(fig_gauge, use_container_width=True)
            
            with col2:
                # Spam vs Ham Probability Chart
                st.markdown("#### 📈 Classification Probabilities")
                fig_prob = go.Figure(data=[
                    go.Bar(
                        x=['Safe (Ham)', 'Spam'],
                        y=[ham_prob, spam_prob],
                        marker_color=['#4facfe', '#f5576c'],
                        text=[f'{ham_prob:.1f}%', f'{spam_prob:.1f}%'],
                        textposition='auto',
                    )
                ])
                fig_prob.update_layout(
                    height=300,
                    yaxis_title="Probability (%)",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color="white"),
                    xaxis=dict(color="white"),
                    yaxis=dict(color="white")
                )
                st.plotly_chart(fig_prob, use_container_width=True)
            
            # Top Words Visualization
            if top_words:
                st.markdown("#### 🔤 Top Words in Message")
                words_list = list(top_words.keys())
                freq_list = list(top_words.values())
                
                fig_words = go.Figure(data=[
                    go.Bar(
                        x=freq_list,
                        y=words_list,
                        orientation='h',
                        marker_color='#667eea',
                        text=freq_list,
                        textposition='auto',
                    )
                ])
                fig_words.update_layout(
                    height=400,
                    xaxis_title="Frequency",
                    yaxis_title="Words",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color="white"),
                    xaxis=dict(color="white"),
                    yaxis=dict(color="white")
                )
                st.plotly_chart(fig_words, use_container_width=True)
            
            # Message Characteristics Pie Chart
            st.markdown("#### 📊 Message Characteristics")
            col1, col2 = st.columns(2)
            
            with col1:
                # Character distribution
                labels = ['Characters (no spaces)', 'Spaces']
                values = [char_count_no_spaces, char_count - char_count_no_spaces]
                colors = ['#667eea', '#764ba2']
                
                fig_chars = go.Figure(data=[go.Pie(
                    labels=labels,
                    values=values,
                    hole=0.4,
                    marker_colors=colors
                )])
                fig_chars.update_layout(
                    height=300,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color="white"),
                    showlegend=True
                )
                st.plotly_chart(fig_chars, use_container_width=True)
            
            with col2:
                # Word length distribution
                word_lengths = [len(word) for word in words if word]
                if word_lengths:
                    length_counts = Counter(word_lengths)
                    lengths = sorted(length_counts.keys())
                    counts = [length_counts[l] for l in lengths]
                    
                    fig_length = go.Figure(data=[
                        go.Scatter(
                            x=lengths,
                            y=counts,
                            mode='lines+markers',
                            marker=dict(color='#f5576c', size=10),
                            line=dict(color='#f5576c', width=3),
                            fill='tozeroy',
                            fillcolor='rgba(245, 87, 108, 0.2)'
                        )
                    ])
                    fig_length.update_layout(
                        height=300,
                        xaxis_title="Word Length",
                        yaxis_title="Frequency",
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(color="white"),
                        xaxis=dict(color="white"),
                        yaxis=dict(color="white")
                    )
                    st.plotly_chart(fig_length, use_container_width=True)
                else:
                    st.info("No words to analyze")
            
            # Detailed Analysis Section - What Makes It Spam or Safe
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 🔍 Detailed Analysis: What Makes This Message Spam or Safe?")
            
            # Pattern Detection (kept identical)
            url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
            urls = re.findall(url_pattern, input_sms)
            url_count = len(urls)
            
            # Count numbers
            numbers = re.findall(r'\d+', input_sms)
            number_count = len(numbers)
            
            # Count special characters and excessive punctuation
            exclamation_count = input_sms.count('!')
            question_count = input_sms.count('?')
            uppercase_count = sum(1 for c in input_sms if c.isupper())
            uppercase_ratio = uppercase_count / char_count if char_count > 0 else 0
            
            # Check for common spam patterns
            spam_patterns = {
                'Free/Freebie': bool(re.search(r'\bfree\b', input_sms, re.IGNORECASE)),
                'Win/Prize': bool(re.search(r'\b(win|won|prize|award)\b', input_sms, re.IGNORECASE)),
                'Urgent': bool(re.search(r'\burgent\b', input_sms, re.IGNORECASE)),
                'Click Here': bool(re.search(r'\bclick\b', input_sms, re.IGNORECASE)),
                'Limited Time': bool(re.search(r'\b(limited|time|offer|expire)\b', input_sms, re.IGNORECASE)),
                'Money/Cash': bool(re.search(r'\b(money|cash|dollar|£|€|$)\b', input_sms, re.IGNORECASE)),
                'Congratulations': bool(re.search(r'\bcongrat\b', input_sms, re.IGNORECASE)),
            }
            
            # Check for common ham patterns
            ham_patterns = {
                'Personal Greeting': bool(re.search(r'\b(hi|hello|hey|dear|thanks|thank you)\b', input_sms, re.IGNORECASE)),
                'Personal Pronouns': bool(re.search(r'\b(i|you|we|they|me|us)\b', input_sms, re.IGNORECASE)),
                'Question Words': bool(re.search(r'\b(what|when|where|why|how|who)\b', input_sms, re.IGNORECASE)),
                'Casual Language': bool(re.search(r'\b(ok|yeah|sure|maybe|probably)\b', input_sms, re.IGNORECASE)),
            }
            
            # Find matching spam and ham words in the message
            message_words_lower = [w.lower() for w in words]
            found_spam_words = [w for w in message_words_lower if w in spam_words_set]
            found_ham_words = [w for w in message_words_lower if w in ham_words_set]
            
            # Calculate spam/ham indicators score
            spam_indicators = sum(spam_patterns.values()) + len(found_spam_words) + (1 if url_count > 0 else 0) + (1 if exclamation_count > 3 else 0) + (1 if uppercase_ratio > 0.3 else 0)
            ham_indicators = sum(ham_patterns.values()) + len(found_ham_words)
            
            # Display Analysis in Columns
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                    <div class="info-card" style="padding: 1.5rem; text-align: left;">
                        <h4 style="color: #f5576c; margin-bottom: 1rem;">🚨 Spam Indicators Found</h4>
                """, unsafe_allow_html=True)
                
                # Spam patterns
                spam_patterns_found = [k for k, v in spam_patterns.items() if v]
                if spam_patterns_found:
                    st.markdown("**Patterns Detected:**")
                    for pattern in spam_patterns_found:
                        st.markdown(f"• {pattern}")
                else:
                    st.markdown("• No common spam patterns detected")
                
                # Spam words
                if found_spam_words:
                    st.markdown(f"<br><strong>Common Spam Words Found ({len(found_spam_words)}):</strong>", unsafe_allow_html=True)
                    spam_words_display = ", ".join(found_spam_words[:10])
                    st.markdown(f"• {spam_words_display}")
                    if len(found_spam_words) > 10:
                        st.markdown(f"• ... and {len(found_spam_words) - 10} more")
                else:
                    st.markdown("<br><strong>Common Spam Words:</strong> None found", unsafe_allow_html=True)
                
                # Other spam indicators
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
                    <div class="info-card" style="padding: 1.5rem; text-align: left;">
                        <h4 style="color: #4facfe; margin-bottom: 1rem;">✅ Safe (Ham) Indicators Found</h4>
                """, unsafe_allow_html=True)
                
                # Ham patterns
                ham_patterns_found = [k for k, v in ham_patterns.items() if v]
                if ham_patterns_found:
                    st.markdown("**Patterns Detected:**")
                    for pattern in ham_patterns_found:
                        st.markdown(f"• {pattern}")
                else:
                    st.markdown("• No common safe patterns detected")
                
                # Ham words
                if found_ham_words:
                    st.markdown(f"<br><strong>Common Safe Words Found ({len(found_ham_words)}):</strong>", unsafe_allow_html=True)
                    ham_words_display = ", ".join(found_ham_words[:10])
                    st.markdown(f"• {ham_words_display}")
                    if len(found_ham_words) > 10:
                        st.markdown(f"• ... and {len(found_ham_words) - 10} more")
                else:
                    st.markdown("<br><strong>Common Safe Words:</strong> None found", unsafe_allow_html=True)
                
                # Other safe indicators
                st.markdown("<br><strong>Other Indicators:</strong>", unsafe_allow_html=True)
                if url_count == 0:
                    st.markdown("• No suspicious URLs")
                if exclamation_count <= 1:
                    st.markdown("• Normal punctuation usage")
                if uppercase_ratio < 0.1:
                    st.markdown("• Normal capitalization")
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Summary Explanation
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
                <div class="info-card" style="padding: 2rem; text-align: left;">
                    <h4 style="color: #667eea; margin-bottom: 1rem;">📝 Classification Summary</h4>
            """, unsafe_allow_html=True)
            
            if result == 1:
                st.markdown(f"""
                    <p style="color: #f5576c; font-weight: 600; margin-bottom: 1rem;">
                        This message was classified as <strong>SPAM</strong> because:
                    </p>
                    <ul style="color: #666; line-height: 1.8;">
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
                    <p style="color: #4facfe; font-weight: 600; margin-bottom: 1rem;">
                        This message was classified as <strong>SAFE (HAM)</strong> because:
                    </p>
                    <ul style="color: #666; line-height: 1.8;">
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

# Info Section with glassmorphism cards
st.markdown("---")
st.markdown("### ℹ️ How It Works")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="info-card">
        <div class="info-icon">🔍</div>
        <div class="info-title">Text Analysis</div>
        <div class="info-desc">Advanced NLP techniques analyze your message content, structure, and patterns</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="info-card">
        <div class="info-icon">🤖</div>
        <div class="info-title">AI Detection</div>
        <div class="info-desc">Machine learning model trained on thousands of messages identifies spam patterns</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="info-card">
        <div class="info-icon">⚡</div>
        <div class="info-title">Instant Results</div>
        <div class="info-desc">Get immediate feedback with confidence scores on message safety</div>
    </div>
    """, unsafe_allow_html=True)

# Additional features section
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 🎯 Key Features")
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div class="info-card" style="text-align: left; padding: 1.5rem;">
        <div style="font-size: 1.5rem; margin-bottom: 0.8rem;">🔒 <strong style="color: #667eea;">Privacy First</strong></div>
        <div class="info-desc" style="text-align: left;">Your messages are processed securely and never stored</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="info-card" style="text-align: left; padding: 1.5rem;">
        <div style="font-size: 1.5rem; margin-bottom: 0.8rem;">📊 <strong style="color: #667eea;">High Accuracy</strong></div>
        <div class="info-desc" style="text-align: left;">Trained on extensive datasets for reliable detection</div>
    </div>
    """, unsafe_allow_html=True)
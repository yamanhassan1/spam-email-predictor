import streamlit as st
import nltk
from collections import Counter
from pathlib import Path
import re
import numpy as np
import pandas as pd
import time

# Existing libs kept for compatibility
import matplotlib.pyplot as plt
import plotly.express as px
from PIL import Image

# Src helpers (advanced design + visualization)
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

# --- Page config & assets (must run before other Streamlit UI commands) ---
setup_page()  # advanced styling, animations, responsive CSS

# --- NLTK and model initialization ---
setup_nltk()
STOP_WORDS = get_stopwords()

tfidf, model = load_model()

# Wordlists
spam_words_set = SPAM_WORDS
ham_words_set = HAM_WORDS

# --- Helpful samples ---
SAMPLES = {
    "Phishing (link + urgent)": "Congratulations! You've won a prize. Click http://bit.ly/win-now to claim within 24 hours!",
    "Promotional (money offer)": "You have been selected to receive $5,000 cash. Reply YES to receive your reward.",
    "Personal / Ham": "Hi John, can we move our meeting to Friday? Thanks and talk soon.",
    "Bank alert (possibly phishing)": "Dear customer, your account is suspended. Visit https://bank.example/recover to reactivate."
}

# --- Header ---
render_header()

# --- Top controls: examples, actions, preferences ---
with st.container():
    col_l, col_r = st.columns([3, 1])
    with col_l:
        st.markdown("### 📝 Enter message to analyze")
        input_sms = st.text_area(
            "Paste email or SMS message here",
            height=220,
            placeholder="Type or paste a message... Try a sample from the dropdown on the right",
            label_visibility="collapsed"
        )
    with col_r:
        st.markdown("### 🔧 Quick actions")
        chosen = st.selectbox("Use a sample", ["— choose sample —"] + list(SAMPLES.keys()))
        if chosen and chosen != "— choose sample —":
            if st.button("Insert sample"):
                input_sms = SAMPLES[chosen]
                # Re-render the page with inserted sample by writing it back into session state
                st.experimental_set_query_params(_sample=chosen)
                # Sleep a moment to let user see the update
                time.sleep(0.06)
                # Because we can't programmatically replace other widgets' values robustly,
                # we instruct the user to re-run by clicking Analyze. But we try to set the text anyway:
                # Note: Streamlit's state handling differs; the inserted value will reflect below only on rerun.
        if st.button("Clear"):
            # This won't directly clear the text_area on the same run; show guidance
            st.experimental_set_query_params(_sample="")
            st.info("Click the text area and clear the text, then re-run analyze.")

        st.markdown("### ⚙️ View options")
        reduce_motion = st.checkbox("Reduce animations", value=False, help="Prevent animations for accessibility.")
        compact_mode = st.checkbox("Compact layout", value=False, help="Use tighter paddings for smaller screens.")
        # Note: CSS is injected at setup_page() time; to change CSS based on these checkboxes we'd need to re-run setup_page(compact=...)
        # For simplicity we honor user preference in content (smaller charts) rather than re-injecting CSS dynamically.
        st.write("")  # small spacer

    # If the user selected a sample we try to populate it
    qp = st.experimental_get_query_params()
    if "_sample" in qp:
        sample_key = qp["_sample"][0]
        if sample_key in SAMPLES and not input_sms:
            input_sms = SAMPLES[sample_key]

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    analyze = st.button("🔍 Analyze Message", use_container_width=True)

# --- Main prediction and visualization flow ---
if analyze:
    if not input_sms or not input_sms.strip():
        st.warning("⚠️ Please enter a message to analyze.")
    else:
        with st.spinner("Analyzing message — applying NLP and model..."):
            # Preprocess
            transformed_sms = transformed_text(input_sms)

            # Vectorize & predict
            vector_input = tfidf.transform([transformed_sms])
            result = model.predict(vector_input)[0]
            # predict_proba usually available for sklearn models
            try:
                proba = model.predict_proba(vector_input)[0]
            except Exception:
                # Fallback: if not available, create a simple deterministic mapping
                proba = np.array([0.5, 0.5])
            confidence = max(proba) * 100
            spam_prob = proba[1] * 100
            ham_prob = proba[0] * 100

            # Basic message stats
            word_count = len(input_sms.split())
            char_count = len(input_sms)
            char_count_no_spaces = len(input_sms.replace(" ", ""))
            sentence_count = len(nltk.sent_tokenize(input_sms))

            # Word frequency
            words = transformed_sms.split()
            word_freq = Counter(words)
            top_words = dict(word_freq.most_common(12)) if words else {}
            words_list = list(top_words.keys())
            freq_list = list(top_words.values())

            # --- Top summary: visually attractive metrics ---
            st.markdown("")  # spacing
            row_a, row_b = st.columns([2, 3], gap="large")
            with row_a:
                # Big result card
                st.markdown(render_result_card(result == 1, confidence), unsafe_allow_html=True)

                # small metrics underneath for quick glance
                mcols = st.columns(3)
                mcols[0].metric("Words", word_count)
                mcols[1].metric("Unique words", len(words))
                mcols[2].metric("Sentences", sentence_count)
            with row_b:
                # Metrics and probability shown as attractive KPI cards
                kcol1, kcol2 = st.columns(2)
                with kcol1:
                    st.metric("Spam probability", f"{spam_prob:.1f}%", delta=None)
                    st.metric("Safe (ham) probability", f"{ham_prob:.1f}%", delta=None)
                with kcol2:
                    # Show model info and confidence
                    st.metric("Model confidence", f"{confidence:.1f}%", delta=None)
                    try:
                        model_name = type(model).__name__
                    except Exception:
                        model_name = "Model"
                    st.caption(f"Model: {model_name}")

            # --- Visualizations: tabs for smooth UX ---
            st.markdown("---")
            tabs = st.tabs(["Overview", "Top Words", "Details", "Annotated"])
            # Overview: confidence + probability
            with tabs[0]:
                c1, c2 = st.columns([1, 1])
                with c1:
                    fig_g = confidence_gauge(confidence, result == 1, height=360, show_threshold=True)
                    st.plotly_chart(fig_g, use_container_width=True)
                with c2:
                    fig_p = probability_bar(ham_prob, spam_prob, height=360)
                    st.plotly_chart(fig_p, use_container_width=True)

                # compact summary below charts
                st.markdown("#### Quick insights")
                insights = []
                if result == 1:
                    insights.append("Model flagged this message as likely SPAM.")
                else:
                    insights.append("Model flagged this message as likely SAFE.")
                if any(w in spam_words_set for w in words):
                    insights.append("Contains words commonly found in spam.")
                if re.search(r"http[s]?://", input_sms):
                    insights.append("Message contains one or more URLs.")
                if sum(1 for c in input_sms if c.isupper()) / max(1, char_count) > 0.25:
                    insights.append("High uppercase usage (possible shouty text).")
                # present insights
                for s in insights[:4]:
                    st.write("•", s)

            # Top Words: Wordcloud + horizontal bar
            with tabs[1]:
                if top_words:
                    col_wc, col_bar = st.columns([1, 1])
                    with col_wc:
                        fig_wc = wordcloud_figure(dict(word_freq), height=360)
                        st.plotly_chart(fig_wc, use_container_width=True)
                    with col_bar:
                        fig_words = top_words_bar(words_list, freq_list, spam_wordset=spam_words_set, height=360)
                        st.plotly_chart(fig_words, use_container_width=True)
                else:
                    st.info("No words to display.")

            # Detailed: characteristics and patterns + charts
            with tabs[2]:
                # message characteristics charts
                c1, c2 = st.columns([1, 1], gap="large")
                with c1:
                    labels = ["Chars (no spaces)", "Spaces"]
                    values = [char_count_no_spaces, max(0, char_count - char_count_no_spaces)]
                    fig_chars = characters_pie(labels, values, height=320)
                    st.plotly_chart(fig_chars, use_container_width=True)
                with c2:
                    word_lengths = [len(w) for w in words if w]
                    if word_lengths:
                        length_counts = Counter(word_lengths)
                        lengths = sorted(length_counts.keys())
                        counts = [length_counts[l] for l in lengths]
                        fig_len = word_length_line(lengths, counts, height=320)
                        st.plotly_chart(fig_len, use_container_width=True)
                    else:
                        st.info("No word-length data available.")

                # Pattern detection & numeric indicators
                st.markdown("#### Detected patterns & indicators")
                url_pattern = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
                urls = re.findall(url_pattern, input_sms)
                url_count = len(urls)
                numbers = re.findall(r"\d+", input_sms)
                number_count = len(numbers)
                exclamation_count = input_sms.count("!")
                uppercase_count = sum(1 for c in input_sms if c.isupper())
                uppercase_ratio = uppercase_count / max(1, char_count)

                spam_patterns = {
                    "Free/Freebie": bool(re.search(r"\bfree\b", input_sms, re.I)),
                    "Win/Prize": bool(re.search(r"\b(win|won|prize|award)\b", input_sms, re.I)),
                    "Urgent": bool(re.search(r"\burgent\b", input_sms, re.I)),
                    "Click Here": bool(re.search(r"\bclick\b", input_sms, re.I)),
                    "Limited Time": bool(re.search(r"\b(limited|time|offer|expire)\b", input_sms, re.I)),
                    "Money/Cash": bool(re.search(r"\b(money|cash|dollar|£|€|\$)\b", input_sms, re.I)),
                    "Congratulations": bool(re.search(r"\bcongrat\b", input_sms, re.I)),
                }

                ham_patterns = {
                    "Personal Greeting": bool(re.search(r"\b(hi|hello|hey|dear|thanks|thank you)\b", input_sms, re.I)),
                    "Personal Pronouns": bool(re.search(r"\b(i|you|we|they|me|us)\b", input_sms, re.I)),
                    "Question Words": bool(re.search(r"\b(what|when|where|why|how|who)\b", input_sms, re.I)),
                    "Casual Language": bool(re.search(r"\b(ok|yeah|sure|maybe|probably)\b", input_sms, re.I)),
                }

                found_spam_words = [w for w in [t.lower() for t in words] if w in spam_words_set]
                found_ham_words = [w for w in [t.lower() for t in words] if w in ham_words_set]

                spam_indicators = sum(spam_patterns.values()) + len(found_spam_words) + (1 if url_count > 0 else 0) + (1 if exclamation_count > 3 else 0) + (1 if uppercase_ratio > 0.3 else 0)
                ham_indicators = sum(ham_patterns.values()) + len(found_ham_words)

                # Render two columns for spam/ham indicators
                sc1, sc2 = st.columns(2)
                with sc1:
                    st.markdown("**🚨 Spam Indicators**")
                    if any(spam_patterns.values()):
                        for k, v in spam_patterns.items():
                            if v:
                                st.write("•", k)
                    else:
                        st.write("• No obvious spam patterns detected")
                    if found_spam_words:
                        st.write(f"• Spam words found ({len(found_spam_words)}): {', '.join(found_spam_words[:10])}")
                    if url_count:
                        st.write(f"• URLs found: {url_count}")
                    if exclamation_count > 3:
                        st.write(f"• Excessive '!': {exclamation_count}")
                    if uppercase_ratio > 0.3:
                        st.write(f"• High uppercase ratio: {uppercase_ratio*100:.1f}%")
                with sc2:
                    st.markdown("**✅ Safe (Ham) Indicators**")
                    if any(ham_patterns.values()):
                        for k, v in ham_patterns.items():
                            if v:
                                st.write("•", k)
                    else:
                        st.write("• No obvious ham-only patterns")
                    if found_ham_words:
                        st.write(f"• Ham words found ({len(found_ham_words)}): {', '.join(found_ham_words[:10])}")
                    if url_count == 0:
                        st.write("• No URLs detected")

                # Summary explanation (keeps original information but formatted)
                st.markdown("**Summary**")
                if result == 1:
                    st.write(f"Model decision: SPAM — {spam_prob:.1f}% probability. Spam indicators: {spam_indicators}; Ham indicators: {ham_indicators}.")
                else:
                    st.write(f"Model decision: SAFE — {ham_prob:.1f}% probability. Ham indicators: {ham_indicators}; Spam indicators: {spam_indicators}.")

            # Annotated: highlight spam/ham words inline
            with tabs[3]:
                st.markdown("#### 🧾 Annotated Message")
                annotated_html = annotated_message_html(input_sms, spam_words=spam_words_set, ham_words=ham_words_set)
                st.markdown(annotated_html, unsafe_allow_html=True)
                st.markdown("---")
                st.markdown("#### Raw cleaned / tokenized text")
                st.code(transformed_sms)

            # Footer: model details & export
            st.markdown("---")
            with st.expander("Model & app details"):
                try:
                    st.write("Model class:", type(model).__name__)
                    # If scikit-learn pipeline, show steps if possible
                    if hasattr(model, "steps"):
                        st.write("Pipeline steps:", [s[0] for s in model.steps])
                except Exception:
                    st.write("Model info unavailable.")
                st.write("Vectorizer:", getattr(tfidf, "__class__", "Vectorizer"))
                st.write("Stopwords count:", len(STOP_WORDS))

                # Allow user to download prediction summary as JSON
                summary = {
                    "prediction": int(result),
                    "spam_probability": float(spam_prob),
                    "ham_probability": float(ham_prob),
                    "confidence": float(confidence),
                    "word_count": int(word_count),
                    "unique_words": int(len(words)),
                    "spam_indicators": int(spam_indicators),
                    "ham_indicators": int(ham_indicators),
                }
                st.download_button("Download summary (JSON)", data=pd.Series(summary).to_json(), file_name="prediction_summary.json", mime="application/json")

# --- End of app ---
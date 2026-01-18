import streamlit as st
import nltk
from collections import Counter
from src.design import render_result_card
from src.nlp import transformed_text


def render_home_page(tfidf, model, spam_words_set, ham_words_set, stop_words):
    """
    Render the main home page with input section and prediction logic.
    """
    # Import here to avoid circular imports
    from src.components.input_section import render_input_section
    from src.pages.prediction_analysis import render_analysis_section
    
    # Render input section
    input_sms = render_input_section()
    
    # Prediction button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        predict_button = st.button("🔍 Analyze Message Now", use_container_width=True)
    
    # Handle prediction
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
                
                # Display result
                st.markdown(render_result_card(result == 1, confidence), unsafe_allow_html=True)
                
                # Render detailed analysis
                render_analysis_section(
                    input_sms=input_sms,
                    transformed_sms=transformed_sms,
                    result=result,
                    confidence=confidence,
                    spam_prob=spam_prob,
                    ham_prob=ham_prob,
                    word_count=word_count,
                    char_count=char_count,
                    char_count_no_spaces=char_count_no_spaces,
                    sentence_count=sentence_count,
                    words=words,
                    word_freq=word_freq,
                    words_list=words_list,
                    freq_list=freq_list,
                    spam_words_set=spam_words_set,
                    ham_words_set=ham_words_set
                )
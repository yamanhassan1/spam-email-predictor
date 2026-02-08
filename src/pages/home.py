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

    # Render input section - now returns both text and files
    input_sms, uploaded_files = render_input_section()

    # Prediction button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        predict_button = st.button("🔍 Analyze Message Now", use_container_width=True)

    # Max input length to prevent DoS from very large inputs
    MAX_INPUT_CHARS = 50_000

    # Handle prediction
    if predict_button:
        # Determine input source
        messages_to_analyze = []

        # Check if files were uploaded
        if uploaded_files:
            for uploaded_file in uploaded_files:
                try:
                    # Read file content
                    content = uploaded_file.read().decode('utf-8', errors='ignore')
                    if content.strip():
                        messages_to_analyze.append({
                            'text': content,
                            'source': uploaded_file.name
                        })
                except Exception as e:
                    st.error(f"Error reading {uploaded_file.name}: {str(e)}")
        # Check if text was entered
        elif input_sms.strip():
            messages_to_analyze.append({
                'text': input_sms,
                'source': 'Manual Input'
            })

        # Validate input
        if not messages_to_analyze:
            st.markdown("""
                <div class="card" style="background: rgba(251, 191, 36, 0.1); border-left: 4px solid #fbbf24; margin: 1rem 0;">
                    <div style="display: flex; align-items: center; gap: 1rem;">
                        <div style="font-size: 2rem;">⚠️</div>
                        <div>
                            <div style="font-weight: 700; margin-bottom: 0.25rem; color: var(--text-primary);">No Message Provided</div>
                            <div style="color: var(--text-secondary); font-size: 0.9rem;">Please enter a message or upload files to analyze.</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            return

        # Check if any message is too long
        oversized = [msg for msg in messages_to_analyze if len(msg['text']) > MAX_INPUT_CHARS]
        if oversized:
            st.markdown(f"""
                <div class="card" style="background: rgba(239, 68, 68, 0.1); border-left: 4px solid var(--danger-red); margin: 1rem 0;">
                    <div style="display: flex; align-items: center; gap: 1rem;">
                        <div style="font-size: 2rem;">⚠️</div>
                        <div>
                            <div style="font-weight: 700; margin-bottom: 0.25rem; color: var(--text-primary);">Message Too Long</div>
                            <div style="color: var(--text-secondary); font-size: 0.9rem;">Some files exceed {MAX_INPUT_CHARS:,} characters. Please use smaller files.</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            return

        # Process messages
        if len(messages_to_analyze) == 1:
            # Single message analysis
            msg_data = messages_to_analyze[0]
            with st.spinner("🔎 Analyzing message with AI..."):
                _analyze_single_message(
                    msg_data['text'], msg_data['source'],
                    tfidf, model, spam_words_set, ham_words_set, stop_words
                )
        else:
            # Batch analysis
            _analyze_batch_messages(
                messages_to_analyze, tfidf, model, spam_words_set, ham_words_set, stop_words
            )


def _analyze_single_message(input_sms, source, tfidf, model, spam_words_set, ham_words_set, stop_words):
    """Analyze a single message and display detailed results."""
    from src.pages.prediction_analysis import render_analysis_section

    # Preprocess (pass cached stop_words for performance)
    transformed_sms = transformed_text(input_sms, stop_words=stop_words)

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

    # Display source info if from file
    if source != 'Manual Input':
        st.info(f"📄 Analyzing: {source}")

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


def _analyze_batch_messages(messages, tfidf, model, spam_words_set, ham_words_set, stop_words):
    """Analyze multiple messages and display batch results."""
    st.markdown(f"""
        <div class="card" style="background: rgba(59, 130, 246, 0.1); border-left: 4px solid #3b82f6; margin: 1rem 0;">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <div style="font-size: 2rem;">📊</div>
                <div>
                    <div style="font-weight: 700; margin-bottom: 0.25rem; color: var(--text-primary);">Batch Analysis Mode</div>
                    <div style="color: var(--text-secondary); font-size: 0.9rem;">Analyzing {len(messages)} messages...</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    results = []
    progress_bar = st.progress(0)

    for idx, msg_data in enumerate(messages):
        # Update progress
        progress_bar.progress((idx + 1) / len(messages))

        # Process message
        transformed_sms = transformed_text(msg_data['text'], stop_words=stop_words)
        vector_input = tfidf.transform([transformed_sms])
        result = model.predict(vector_input)[0]
        prediction_proba = model.predict_proba(vector_input)[0]
        confidence = max(prediction_proba) * 100

        results.append({
            'source': msg_data['source'],
            'is_spam': result == 1,
            'confidence': confidence,
            'spam_prob': prediction_proba[1] * 100,
            'ham_prob': prediction_proba[0] * 100,
            'preview': msg_data['text'][:100] + '...' if len(msg_data['text']) > 100 else msg_data['text']
        })

    progress_bar.empty()

    # Display summary
    spam_count = sum(1 for r in results if r['is_spam'])
    ham_count = len(results) - spam_count

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <h3 style='color: var(--text-primary); font-size: 1.5rem; font-weight: 700; margin: 2rem 0 1rem 0; text-align: center;'>
            📊 Batch Analysis Results
        </h3>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
            <div class="card animate" style="text-align: center;">
                <div style="font-size: 2.5rem; font-weight: 900; color: var(--primary-blue); margin-bottom: 0.5rem;">{len(results)}</div>
                <p style="color: var(--text-secondary); font-size: 0.95rem; margin: 0;">Total Analyzed</p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="card animate" style="text-align: center;">
                <div style="font-size: 2.5rem; font-weight: 900; color: var(--danger-red); margin-bottom: 0.5rem;">{spam_count}</div>
                <p style="color: var(--text-secondary); font-size: 0.95rem; margin: 0;">Spam Detected</p>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="card animate" style="text-align: center;">
                <div style="font-size: 2.5rem; font-weight: 900; color: var(--success-green); margin-bottom: 0.5rem;">{ham_count}</div>
                <p style="color: var(--text-secondary); font-size: 0.95rem; margin: 0;">Safe Messages</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Display individual results in expandable cards
    st.markdown("""
        <h4 style='color: var(--text-primary); font-size: 1.25rem; font-weight: 700; margin: 1.5rem 0 1rem 0;'>
            Detailed Results
        </h4>
    """, unsafe_allow_html=True)

    for idx, r in enumerate(results, 1):
        status_color = "var(--danger-red)" if r['is_spam'] else "var(--success-green)"
        status_icon = "🚨" if r['is_spam'] else "✅"
        status_text = "SPAM" if r['is_spam'] else "SAFE"

        with st.expander(f"{status_icon} {r['source']} - {status_text} ({r['confidence']:.1f}% confidence)"):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"**Preview:** {r['preview']}")
            with col2:
                st.metric("Spam Probability", f"{r['spam_prob']:.1f}%")
                st.metric("Safe Probability", f"{r['ham_prob']:.1f}%")
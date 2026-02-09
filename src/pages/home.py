import streamlit as st
import nltk
from collections import Counter
from email import policy
from email.parser import BytesParser

from src.design import render_result_card
from src.nlp import transformed_text
from src.components.pattern_analysis import render_pattern_analysis
from src.components.feature_analysis import render_advanced_feature_analysis
from src.visualization import (
    probability_bar,
    top_words_bar,
    characters_pie
)
from src.model import explain_prediction


def _extract_eml_text_and_headers(data: bytes):
    """Extract plain text and key headers from an .eml payload."""
    try:
        msg = BytesParser(policy=policy.default).parsebytes(data)
    except Exception:
        return "", {}

    headers = {
        'From': msg.get('From', ''),
        'To': msg.get('To', ''),
        'Subject': msg.get('Subject', ''),
        'Authentication-Results': msg.get('Authentication-Results', '')
    }

    # Parse SPF/DKIM/DMARC summary if present
    try:
        import re
        auth = headers['Authentication-Results'] or ''

        def _status(key: str) -> str:
            m = re.search(rf"{key}\\s*=\\s*(pass|fail|softfail|neutral|temperror|permerror)", auth, re.I)
            return (m.group(1).lower() if m else 'unknown')

        headers['SPF'] = _status('spf')
        headers['DKIM'] = _status('dkim')
        headers['DMARC'] = _status('dmarc')
    except Exception:
        headers['SPF'] = headers['DKIM'] = headers['DMARC'] = 'unknown'

    # Extract a plain text body best-effort
    text = ''
    try:
        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                if ctype == 'text/plain':
                    try:
                        text += part.get_content() or ''
                    except Exception:
                        payload = part.get_payload(decode=True) or b''
                        text += payload.decode(part.get_content_charset() or 'utf-8', errors='ignore')
        else:
            if msg.get_content_type() == 'text/plain':
                try:
                    text = msg.get_content() or ''
                except Exception:
                    payload = msg.get_payload(decode=True) or b''
                    text = payload.decode(msg.get_content_charset() or 'utf-8', errors='ignore')
            else:
                payload = msg.get_payload(decode=True) or b''
                text = payload.decode(msg.get_content_charset() or 'utf-8', errors='ignore')
    except Exception:
        pass

    return text, headers


def _status_emoji(status: str) -> str:
    s = (status or 'unknown').lower()
    if s == 'pass':
        return '✅ PASS'
    if s == 'fail':
        return '❌ FAIL'
    return '⚪ UNKNOWN'


def _render_headers_card(headers: dict):
    """Render a clean Email Metadata section using native Streamlit layout."""
    from_ = headers.get('From', '')
    to_ = headers.get('To', '')
    subject = headers.get('Subject', '')
    spf = headers.get('SPF', 'unknown')
    dkim = headers.get('DKIM', 'unknown')
    dmarc = headers.get('DMARC', 'unknown')

    st.subheader('Email Metadata')

    # From
    c1, c2 = st.columns([1, 4])
    with c1:
        st.caption('From')
    with c2:
        st.write(from_ if from_ else '-')

    # To
    c1, c2 = st.columns([1, 4])
    with c1:
        st.caption('To')
    with c2:
        st.write(to_ if to_ else '-')

    # Subject
    c1, c2 = st.columns([1, 4])
    with c1:
        st.caption('Subject')
    with c2:
        st.write(subject if subject else '-')

    # Auth status
    st.caption('Authentication')
    a1, a2, a3 = st.columns(3)
    with a1:
        st.write(f"SPF: {_status_emoji(spf)}")
    with a2:
        st.write(f"DKIM: {_status_emoji(dkim)}")
    with a3:
        st.write(f"DMARC: {_status_emoji(dmarc)}")


def render_home_page(tfidf, model, spam_words_set, ham_words_set, stop_words):
    """
    Render the main home page with input section and prediction logic.
    """
    # Import here to avoid circular imports
    from src.components.input_section import render_input_section

    # Render input section - returns both text and files
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
                    raw = uploaded_file.read()
                    if uploaded_file.name.lower().endswith('.eml'):
                        text, headers = _extract_eml_text_and_headers(raw)
                        if text.strip():
                            messages_to_analyze.append({'text': text, 'source': uploaded_file.name, 'headers': headers})
                    else:
                        content = raw.decode('utf-8', errors='ignore')
                        if content.strip():
                            messages_to_analyze.append({'text': content, 'source': uploaded_file.name})
                except Exception as e:
                    st.error(f"Error reading {uploaded_file.name}: {str(e)}")
        # Check if text was entered
        elif input_sms.strip():
            messages_to_analyze.append({'text': input_sms, 'source': 'Manual Input'})

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
            # If available, render email headers/metadata
            if isinstance(msg_data, dict) and msg_data.get('headers'):
                _render_headers_card(msg_data['headers'])
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

    # Preprocess (pass cached stop_words for performance)
    transformed_sms = transformed_text(input_sms, stop_words=stop_words)

    # Vectorize + Predict
    vector_input = tfidf.transform([transformed_sms])
    # Prefer predict_proba when available
    if hasattr(model, 'predict_proba'):
        result = model.predict(vector_input)[0]
        prediction_proba = model.predict_proba(vector_input)[0]
    else:
        # Fallback for models without predict_proba
        result = model.predict(vector_input)[0]
        try:
            score = float(model.decision_function(vector_input)[0])
        except Exception:
            score = 0.0
        import numpy as np
        spam_prob_val = 1 / (1 + np.exp(-score))
        prediction_proba = [1 - spam_prob_val, spam_prob_val]

    confidence = max(prediction_proba) * 100
    spam_prob = prediction_proba[1] * 100
    ham_prob = prediction_proba[0] * 100

    # Message statistics
    word_count = len(input_sms.split())
    char_count = len(input_sms)
    char_count_no_spaces = len(input_sms.replace(" ", ""))
    try:
        sentence_count = len(nltk.sent_tokenize(input_sms))
    except LookupError:
        sentence_count = max(1, input_sms.count('.') + input_sms.count('!') + input_sms.count('?'))

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

    # Explanation (word impact)
    try:
        exp = explain_prediction(transformed_sms, tfidf, model, top_k=8)
        _render_explanation(exp)
    except Exception:
        pass

    # Render detailed analysis sections
    _render_analysis_section(
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


def _render_analysis_section(input_sms, transformed_sms, result, confidence, spam_prob,
                             ham_prob, word_count, char_count, char_count_no_spaces,
                             sentence_count, words, word_freq, words_list, freq_list,
                             spam_words_set, ham_words_set):
    """Render all analysis visualizations and insights."""

    # Probability bar (ham_prob first, spam_prob second)
    st.markdown("<br>", unsafe_allow_html=True)
    fig = probability_bar(ham_prob, spam_prob)
    st.plotly_chart(fig, use_container_width=True)

    # Stats cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
            <div class="card animate" style="text-align: center;">
                <div style="color: var(--text-muted); font-size: 0.85rem; margin-bottom: 0.25rem;">Words</div>
                <div style="font-size: 1.75rem; font-weight: 900; color: var(--primary-blue);">{word_count}</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="card animate" style="text-align: center;">
                <div style="color: var(--text-muted); font-size: 0.85rem; margin-bottom: 0.25rem;">Characters</div>
                <div style="font-size: 1.75rem; font-weight: 900; color: var(--primary-purple);">{char_count}</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="card animate" style="text-align: center;">
                <div style="color: var(--text-muted); font-size: 0.85rem; margin-bottom: 0.25rem;">Sentences</div>
                <div style="font-size: 1.75rem; font-weight: 900; color: var(--primary-cyan);">{sentence_count}</div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        avg_word_len = char_count_no_spaces / word_count if word_count > 0 else 0
        st.markdown(f"""
            <div class="card animate" style="text-align: center;">
                <div style="color: var(--text-muted); font-size: 0.85rem; margin-bottom: 0.25rem;">Avg Word Length</div>
                <div style="font-size: 1.75rem; font-weight: 900; color: var(--success-green);">{avg_word_len:.1f}</div>
            </div>
        """, unsafe_allow_html=True)

    # Charts in two columns
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        if words_list and freq_list:
            fig = top_words_bar(words_list, freq_list, spam_words_set)
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        if input_sms:
            # Calculate character distribution
            char_types = {
                'Letters': sum(1 for c in input_sms if c.isalpha()),
                'Numbers': sum(1 for c in input_sms if c.isdigit()),
                'Spaces': sum(1 for c in input_sms if c.isspace()),
                'Special': sum(1 for c in input_sms if not c.isalnum() and not c.isspace())
            }
            labels = list(char_types.keys())
            values = list(char_types.values())

            if sum(values) > 0:  # Only show if there's data
                fig = characters_pie(labels, values)
                st.plotly_chart(fig, use_container_width=True)

    # Pattern analysis
    render_pattern_analysis(
        input_sms, result, confidence, spam_prob, ham_prob,
        words, spam_words_set, ham_words_set
    )

    # Advanced feature analysis
    render_advanced_feature_analysis(
        input_sms, words, spam_words_set, ham_words_set
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
        if hasattr(model, 'predict_proba'):
            result = model.predict(vector_input)[0]
            prediction_proba = model.predict_proba(vector_input)[0]
        else:
            result = model.predict(vector_input)[0]
            try:
                score = float(model.decision_function(vector_input)[0])
            except Exception:
                score = 0.0
            import numpy as np
            spam_prob_val = 1 / (1 + np.exp(-score))
            prediction_proba = [1 - spam_prob_val, spam_prob_val]
        confidence = max(prediction_proba) * 100

        results.append({
            'source': msg_data['source'],
            'is_spam': result == 1,
            'confidence': confidence,
            'spam_prob': prediction_proba[1] * 100,
            'ham_prob': prediction_proba[0] * 100,
            'word_count': len(msg_data['text'].split()),
            'char_count': len(msg_data['text']),
            'preview': msg_data['text'][:100] + '...' if len(msg_data['text']) > 100 else msg_data['text']
        })

    progress_bar.empty()

    # Display summary
    spam_count = sum(1 for r in results if r['is_spam'])
    ham_count = len(results) - spam_count
    avg_confidence = sum(r['confidence'] for r in results) / len(results)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <h3 style='color: var(--text-primary); font-size: 1.5rem; font-weight: 700; margin: 2rem 0 1rem 0; text-align: center;'>
            📊 Batch Analysis Results
        </h3>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
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

    with col4:
        st.markdown(f"""
            <div class="card animate" style="text-align: center;">
                <div style="font-size: 2.5rem; font-weight: 900; color: var(--primary-cyan); margin-bottom: 0.5rem;">{avg_confidence:.0f}%</div>
                <p style="color: var(--text-secondary); font-size: 0.95rem; margin: 0;">Avg Confidence</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Display individual results in expandable cards
    st.markdown("""
        <h4 style='color: var(--text-primary); font-size: 1.25rem; font-weight: 700; margin: 1.5rem 0 1rem 0;'>
            📋 Detailed Results
        </h4>
    """, unsafe_allow_html=True)

    for idx, r in enumerate(results, 1):
        status_icon = "🚨" if r['is_spam'] else "✅"
        status_text = "SPAM" if r['is_spam'] else "SAFE"
        status_color = "#ef4444" if r['is_spam'] else "#10b981"

        with st.expander(f"{status_icon} {r['source']} - {status_text} ({r['confidence']:.1f}% confidence)",
                         expanded=False):
            col1, col2 = st.columns([2, 1])

            with col1:
                st.markdown(f"""
                    <div style="background: rgba(255, 255, 255, 0.03); padding: 1rem; border-radius: 8px; border-left: 3px solid {status_color};">
                        <div style="color: var(--text-muted); font-size: 0.85rem; margin-bottom: 0.5rem;">MESSAGE PREVIEW:</div>
                        <div style="color: var(--text-primary); line-height: 1.6;">{r['preview']}</div>
                    </div>
                """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                # Stats
                stat_col1, stat_col2 = st.columns(2)
                with stat_col1:
                    st.metric("Words", r['word_count'])
                with stat_col2:
                    st.metric("Characters", r['char_count'])

            with col2:
                st.markdown(f"""
                    <div style="text-align: center; padding: 1rem;">
                        <div style="font-size: 3rem; margin-bottom: 1rem;">{status_icon}</div>
                        <div style="font-size: 1.5rem; font-weight: 900; color: {status_color}; margin-bottom: 0.5rem;">{status_text}</div>
                        <div style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 1rem;">Confidence: {r['confidence']:.1f}%</div>
                    </div>
                """, unsafe_allow_html=True)

                st.metric("Spam Probability", f"{r['spam_prob']:.1f}%",
                          delta=f"{r['spam_prob'] - 50:.1f}%" if r['spam_prob'] > 50 else None,
                          delta_color="inverse")
                st.metric("Safe Probability", f"{r['ham_prob']:.1f}%",
                          delta=f"{r['ham_prob'] - 50:.1f}%" if r['ham_prob'] > 50 else None,
                          delta_color="normal")

import streamlit as st
import html
import re
from src.visualization import annotated_message_html


def render_pattern_analysis(input_sms, result, confidence, spam_prob, ham_prob, words, spam_words_set, ham_words_set):
    """Render detailed pattern analysis section."""
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <h3 style='color: #f8fafc; font-size: 1.5rem; font-weight: 700; margin: 2rem 0 1.5rem 0; letter-spacing: -0.02em;'>
            🔍 Detailed Pattern Analysis
        </h3>
    """, unsafe_allow_html=True)
    
    # Extract patterns
    patterns_data = extract_patterns(input_sms, words, spam_words_set, ham_words_set)
    
    # Render two-column analysis
    render_indicators_comparison(patterns_data)
    
    # Classification summary
    render_classification_summary(result, confidence, spam_prob, ham_prob, patterns_data)
    
    # Annotated message
    render_annotated_message(input_sms, spam_words_set, ham_words_set)


def extract_patterns(input_sms, words, spam_words_set, ham_words_set):
    """Extract all patterns and indicators from the message."""
    char_count = len(input_sms)
    
    # URL and character analysis
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    urls = re.findall(url_pattern, input_sms)
    url_count = len(urls)
    numbers = re.findall(r'\d+', input_sms)
    number_count = len(numbers)
    exclamation_count = input_sms.count('!')
    uppercase_count = sum(1 for c in input_sms if c.isupper())
    uppercase_ratio = uppercase_count / char_count if char_count > 0 else 0
    
    # Spam patterns
    spam_patterns = {
        'Free/Freebie': bool(re.search(r'\bfree\b', input_sms, re.IGNORECASE)),
        'Win/Prize': bool(re.search(r'\b(win|won|prize|award)\b', input_sms, re.IGNORECASE)),
        'Urgent': bool(re.search(r'\burgent\b', input_sms, re.IGNORECASE)),
        'Click Here': bool(re.search(r'\bclick\b', input_sms, re.IGNORECASE)),
        'Limited Time': bool(re.search(r'\b(limited|time|offer|expire)\b', input_sms, re.IGNORECASE)),
        'Money/Cash': bool(re.search(r'\b(money|cash|dollar|£|€|$)\b', input_sms, re.IGNORECASE)),
        'Congratulations': bool(re.search(r'\bcongrat\b', input_sms, re.IGNORECASE)),
    }
    
    # Ham patterns
    ham_patterns = {
        'Personal Greeting': bool(re.search(r'\b(hi|hello|hey|dear|thanks|thank you)\b', input_sms, re.IGNORECASE)),
        'Personal Pronouns': bool(re.search(r'\b(i|you|we|they|me|us)\b', input_sms, re.IGNORECASE)),
        'Question Words': bool(re.search(r'\b(what|when|where|why|how|who)\b', input_sms, re.IGNORECASE)),
        'Casual Language': bool(re.search(r'\b(ok|yeah|sure|maybe|probably)\b', input_sms, re.IGNORECASE)),
    }
    
    # Find words
    message_words_lower = [w.lower() for w in words]
    found_spam_words = [w for w in message_words_lower if w in spam_words_set]
    found_ham_words = [w for w in message_words_lower if w in ham_words_set]
    
    # Calculate indicators
    spam_indicators = (
        sum(spam_patterns.values()) + 
        len(found_spam_words) + 
        (1 if url_count > 0 else 0) + 
        (1 if exclamation_count > 3 else 0) + 
        (1 if uppercase_ratio > 0.3 else 0)
    )
    ham_indicators = sum(ham_patterns.values()) + len(found_ham_words)
    
    return {
        'spam_patterns': spam_patterns,
        'ham_patterns': ham_patterns,
        'found_spam_words': found_spam_words,
        'found_ham_words': found_ham_words,
        'spam_indicators': spam_indicators,
        'ham_indicators': ham_indicators,
        'url_count': url_count,
        'number_count': number_count,
        'exclamation_count': exclamation_count,
        'uppercase_ratio': uppercase_ratio
    }


def render_indicators_comparison(data):
    """Render spam vs ham indicators comparison."""
    col1, col2 = st.columns(2)
    
    with col1:
        render_spam_indicators(data)
    
    with col2:
        render_ham_indicators(data)


def render_spam_indicators(data):
    """Render spam indicators card."""
    st.markdown("""
        <div class="card animate" style="background: linear-gradient(135deg, rgba(239, 68, 68, 0.08), rgba(251, 113, 133, 0.04)); border-left: 4px solid #ef4444; height: 100%;">
            <h4 style="color: #fecdd3; margin-bottom: 1rem; font-size: 1.15rem; font-weight: 700; display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.5rem;">🚨</span> Spam Indicators Found
            </h4>
    """, unsafe_allow_html=True)
    
    spam_patterns_found = [k for k, v in data['spam_patterns'].items() if v]
    if spam_patterns_found:
        st.markdown("<div style='color: #fecdd3; font-weight: 600; margin-bottom: 0.5rem;'>Detected Patterns:</div>", unsafe_allow_html=True)
        for pattern in spam_patterns_found:
            st.markdown(f"<div style='color: #fde2e4; margin-left: 1rem; margin-bottom: 0.25rem;'>• {html.escape(pattern)}</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='color: #cbd5e1; margin-left: 1rem;'>✓ No common spam patterns detected</div>", unsafe_allow_html=True)
    
    if data['found_spam_words']:
        st.markdown(f"<div style='color: #fecdd3; font-weight: 600; margin: 1rem 0 0.5rem 0;'>Spam Words Found ({len(data['found_spam_words'])}):</div>", unsafe_allow_html=True)
        spam_words_display = html.escape(", ".join(data['found_spam_words'][:10]))
        st.markdown(f"<div style='color: #fde2e4; margin-left: 1rem;'>• {spam_words_display}</div>", unsafe_allow_html=True)
        if len(data['found_spam_words']) > 10:
            st.markdown(f"<div style='color: #fde2e4; margin-left: 1rem;'>• ... and {len(data['found_spam_words']) - 10} more</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='color: #cbd5e1; margin: 1rem 0 0 1rem;'>✓ No spam words detected</div>", unsafe_allow_html=True)
    
    st.markdown("<div style='color: #fecdd3; font-weight: 600; margin: 1rem 0 0.5rem 0;'>Other Indicators:</div>", unsafe_allow_html=True)
    has_indicators = False
    if data['url_count'] > 0:
        st.markdown(f"<div style='color: #fde2e4; margin-left: 1rem;'>• Contains {data['url_count']} URL(s)</div>", unsafe_allow_html=True)
        has_indicators = True
    if data['exclamation_count'] > 3:
        st.markdown(f"<div style='color: #fde2e4; margin-left: 1rem;'>• Excessive exclamation marks ({data['exclamation_count']})</div>", unsafe_allow_html=True)
        has_indicators = True
    if data['uppercase_ratio'] > 0.3:
        st.markdown(f"<div style='color: #fde2e4; margin-left: 1rem;'>• High uppercase ratio ({data['uppercase_ratio']*100:.1f}%)</div>", unsafe_allow_html=True)
        has_indicators = True
    if data['number_count'] > 5:
        st.markdown(f"<div style='color: #fde2e4; margin-left: 1rem;'>• Many numbers detected ({data['number_count']})</div>", unsafe_allow_html=True)
        has_indicators = True
    if not has_indicators:
        st.markdown("<div style='color: #cbd5e1; margin-left: 1rem;'>✓ No suspicious indicators</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)


def render_ham_indicators(data):
    """Render ham indicators card."""
    st.markdown("""
        <div class="card animate" style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.08), rgba(52, 211, 153, 0.04)); border-left: 4px solid #10b981; height: 100%;">
            <h4 style="color: #d1fae5; margin-bottom: 1rem; font-size: 1.15rem; font-weight: 700; display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.5rem;">✅</span> Safe (Ham) Indicators Found
            </h4>
    """, unsafe_allow_html=True)
    
    ham_patterns_found = [k for k, v in data['ham_patterns'].items() if v]
    if ham_patterns_found:
        st.markdown("<div style='color: #d1fae5; font-weight: 600; margin-bottom: 0.5rem;'>Detected Patterns:</div>", unsafe_allow_html=True)
        for pattern in ham_patterns_found:
            st.markdown(f"<div style='color: #ecfdf5; margin-left: 1rem; margin-bottom: 0.25rem;'>• {html.escape(pattern)}</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='color: #cbd5e1; margin-left: 1rem;'>⚠ No common safe patterns detected</div>", unsafe_allow_html=True)
    
    if data['found_ham_words']:
        st.markdown(f"<div style='color: #d1fae5; font-weight: 600; margin: 1rem 0 0.5rem 0;'>Safe Words Found ({len(data['found_ham_words'])}):</div>", unsafe_allow_html=True)
        ham_words_display = html.escape(", ".join(data['found_ham_words'][:10]))
        st.markdown(f"<div style='color: #ecfdf5; margin-left: 1rem;'>• {ham_words_display}</div>", unsafe_allow_html=True)
        if len(data['found_ham_words']) > 10:
            st.markdown(f"<div style='color: #ecfdf5; margin-left: 1rem;'>• ... and {len(data['found_ham_words']) - 10} more</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='color: #cbd5e1; margin: 1rem 0 0 1rem;'>⚠ No safe words detected</div>", unsafe_allow_html=True)
    
    st.markdown("<div style='color: #d1fae5; font-weight: 600; margin: 1rem 0 0.5rem 0;'>Positive Indicators:</div>", unsafe_allow_html=True)
    has_indicators = False
    if data['url_count'] == 0:
        st.markdown("<div style='color: #ecfdf5; margin-left: 1rem;'>• No suspicious URLs</div>", unsafe_allow_html=True)
        has_indicators = True
    if data['exclamation_count'] <= 1:
        st.markdown("<div style='color: #ecfdf5; margin-left: 1rem;'>• Normal punctuation usage</div>", unsafe_allow_html=True)
        has_indicators = True
    if data['uppercase_ratio'] < 0.1:
        st.markdown("<div style='color: #ecfdf5; margin-left: 1rem;'>• Normal capitalization</div>", unsafe_allow_html=True)
        has_indicators = True
    if not has_indicators:
        st.markdown("<div style='color: #cbd5e1; margin-left: 1rem;'>⚠ Few positive indicators found</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)


def render_classification_summary(result, confidence, spam_prob, ham_prob, data):
    """Render classification summary card."""
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
        render_spam_summary(confidence, spam_prob, ham_prob, data)
    else:
        render_ham_summary(confidence, spam_prob, ham_prob, data)
    
    st.markdown("</div>", unsafe_allow_html=True)


def render_spam_summary(confidence, spam_prob, ham_prob, data):
    """Render spam classification summary."""
    st.markdown(f"""
        <p style="color: #fecdd3; font-weight: 600; margin-bottom: 1rem; font-size: 1.05rem;">
            This message was classified as <strong>SPAM</strong> with {confidence:.1f}% confidence because:
        </p>
        <ul style="color: #fde2e4; line-height: 2; margin-left: 1rem;">
            <li>Detected <strong>{data['spam_indicators']} spam indicator(s)</strong> vs <strong>{data['ham_indicators']} safe indicator(s)</strong></li>
            <li>Model assigned <strong>{spam_prob:.1f}% spam probability</strong> and <strong>{ham_prob:.1f}% safe probability</strong></li>
    """, unsafe_allow_html=True)
    
    spam_patterns_found = [k for k, v in data['spam_patterns'].items() if v]
    if spam_patterns_found:
        st.markdown(f"<li>Spam patterns found: <strong>{html.escape(', '.join(spam_patterns_found))}</strong></li>", unsafe_allow_html=True)
    if data['found_spam_words']:
        st.markdown(f"<li>Contains <strong>{len(data['found_spam_words'])} words</strong> commonly found in spam messages</li>", unsafe_allow_html=True)
    if data['url_count'] > 0:
        st.markdown(f"<li>Contains <strong>{data['url_count']} potentially suspicious URL(s)</strong></li>", unsafe_allow_html=True)
    if data['uppercase_ratio'] > 0.3:
        st.markdown(f"<li>Unusual capitalization pattern detected (<strong>{data['uppercase_ratio']*100:.1f}%</strong> uppercase)</li>", unsafe_allow_html=True)
    
    st.markdown("</ul>", unsafe_allow_html=True)


def render_ham_summary(confidence, spam_prob, ham_prob, data):
    """Render ham classification summary."""
    st.markdown(f"""
        <p style="color: #d1fae5; font-weight: 600; margin-bottom: 1rem; font-size: 1.05rem;">
            This message was classified as <strong>SAFE (HAM)</strong> with {confidence:.1f}% confidence because:
        </p>
        <ul style="color: #ecfdf5; line-height: 2; margin-left: 1rem;">
            <li>Detected <strong>{data['ham_indicators']} safe indicator(s)</strong> vs <strong>{data['spam_indicators']} spam indicator(s)</strong></li>
            <li>Model assigned <strong>{ham_prob:.1f}% safe probability</strong> and <strong>{spam_prob:.1f}% spam probability</strong></li>
    """, unsafe_allow_html=True)
    
    ham_patterns_found = [k for k, v in data['ham_patterns'].items() if v]
    if ham_patterns_found:
        st.markdown("<li>Contains natural language patterns typical of legitimate messages</li>", unsafe_allow_html=True)
    if data['found_ham_words']:
        st.markdown(f"<li>Contains <strong>{len(data['found_ham_words'])} words</strong> commonly found in safe messages</li>", unsafe_allow_html=True)
    if data['url_count'] == 0:
        st.markdown("<li>No suspicious URLs detected</li>", unsafe_allow_html=True)
    if data['uppercase_ratio'] < 0.1:
        st.markdown(f"<li>Natural capitalization pattern (<strong>{data['uppercase_ratio']*100:.1f}%</strong> uppercase)</li>", unsafe_allow_html=True)
    
    st.markdown("</ul>", unsafe_allow_html=True)


def render_annotated_message(input_sms, spam_words_set, ham_words_set):
    """Render annotated message with highlighted words."""
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
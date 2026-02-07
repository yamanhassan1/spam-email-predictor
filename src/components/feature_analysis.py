"""
Advanced feature analysis UI: displays extracted text, formatting, URL, and behavioral features.
"""
import streamlit as st
import html
from typing import Set, List, Optional
from src.features import extract_all_features
from src.design import section_heading_html


def _row(label: str, value: str, tooltip: str = "") -> str:
    safe_label = html.escape(label)
    safe_value = html.escape(str(value))
    tt = f' title="{html.escape(tooltip)}"' if tooltip else ""
    return f'<tr><td style="color: var(--text-secondary); padding: 0.5rem 0.75rem; border-bottom: 1px solid var(--glass-border);">{safe_label}</td><td style="color: var(--text-primary); font-weight: 600; padding: 0.5rem 0.75rem; border-bottom: 1px solid var(--glass-border);"{tt}>{safe_value}</td></tr>'


def _feature_card(title: str, icon: str, rows: List[str]) -> str:
    body = "".join(rows)
    return f"""
    <div class="card animate" style="height: 100%;">
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem; color: var(--text-primary); font-weight: 700; font-size: 1.05rem;">
            <span style="font-size: 1.5rem;">{html.escape(icon)}</span>
            <span>{html.escape(title)}</span>
        </div>
        <table style="width: 100%; border-collapse: collapse; font-size: 0.9rem;">
            <tbody>{body}</tbody>
        </table>
    </div>
    """


def render_advanced_feature_analysis(
    raw_text: str,
    processed_words: List[str],
    spam_words_set: Set[str],
    ham_words_set: Set[str],
):
    """Render the Advanced Feature Analysis section with all extractable features."""
    feats = extract_all_features(
        raw_text,
        processed_words=processed_words,
        spam_words_set=spam_words_set,
        ham_words_set=ham_words_set,
    )

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(section_heading_html("📐", "Advanced Feature Analysis"), unsafe_allow_html=True)
    st.markdown("""
        <p style="color: var(--text-secondary); text-align: center; margin: 0 0 1.5rem 0; font-size: 0.95rem; max-width: 640px; margin-left: auto; margin-right: auto;">
            Detection signals derived from text content, formatting, URLs, and language. 
            Sender/header features (SPF, DKIM, domain) require full email headers.
        </p>
    """, unsafe_allow_html=True)

    # 1. Text content features
    c1 = _feature_card(
        "Text content",
        "📝",
        [
            _row("Word count", f"{feats['word_count']:,}", "Email length in words"),
            _row("Character count", f"{feats['char_count']:,}", ""),
            _row("Spam keyword frequency", feats["spam_keyword_frequency"], "Matches from spam dictionary"),
            _row("Ham keyword frequency", feats["ham_keyword_frequency"], "Matches from safe dictionary"),
            _row("Average word length", feats["avg_word_length"], ""),
            _row("Character n-grams (3)", f"{feats['char_ngram_count']} unique", "Text complexity"),
            _row("Unique words", feats["unique_word_count"], ""),
        ],
    )

    # 2. Formatting & style
    c2 = _feature_card(
        "Formatting & style",
        "🎨",
        [
            _row("Capital letter ratio", f"{feats['capital_letter_ratio']*100:.2f}%", "Uppercase / total letters"),
            _row("Exclamation marks", feats["exclamation_count"], ""),
            _row("Question marks", feats["question_mark_count"], ""),
            _row("Special chars ($@#)", feats["special_char_count"], ""),
            _row("All-caps words", feats["all_caps_word_count"], "Words with 2+ letters all uppercase"),
        ],
    )

    # 3. URL & link
    c3 = _feature_card(
        "URL & links",
        "🔗",
        [
            _row("URL count", feats["url_count"], ""),
            _row("URL shorteners", feats["url_shortener_count"], "e.g. bit.ly, tinyurl"),
            _row("IP-based URLs", feats["suspicious_ip_url_count"], "Suspicious"),
            _row("HTTPS links", feats["https_link_count"], ""),
            _row("HTTP links", feats["http_link_count"], "Insecure"),
        ],
    )

    # 4. Structural
    c4 = _feature_card(
        "Structural",
        "📄",
        [
            _row("HTML content", "Yes" if feats["html_content_presence"] else "No", ""),
            _row("Hidden/colored text", "Yes" if feats["hidden_or_colored_text"] else "No", ""),
        ],
    )

    # 5. Sender (N/A)
    na = '<span style="color: var(--text-muted);">N/A</span>'
    c5 = _feature_card(
        "Sender & headers",
        "📧",
        [
            _row("Domain reputation", na, "Requires full email"),
            _row("Free email provider", na, "Requires From header"),
            _row("Reply-To / From match", na, "Requires headers"),
            _row("SPF / DKIM / DMARC", na, "Requires headers"),
        ],
    )

    # 6. Statistical + 7. Behavioral
    c6 = _feature_card(
        "Statistical & behavioral",
        "📊",
        [
            _row("Text entropy", feats["text_entropy"], "Character randomness"),
            _row("Repeated word ratio", f"{feats['repeated_word_ratio']*100:.2f}%", ""),
            _row("Imperative verbs", feats["imperative_verb_count"], "e.g. click, buy, claim"),
            _row("Urgency words", feats["urgency_word_count"], "e.g. urgent, now, limited"),
        ],
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(c1, unsafe_allow_html=True)
    with col2:
        st.markdown(c2, unsafe_allow_html=True)
    with col3:
        st.markdown(c3, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col4, col5, col6 = st.columns(3)
    with col4:
        st.markdown(c4, unsafe_allow_html=True)
    with col5:
        st.markdown(c5, unsafe_allow_html=True)
    with col6:
        st.markdown(c6, unsafe_allow_html=True)

"""
Advanced feature extraction for spam detection.
Extracts text, formatting, URL, structural, and behavioral features from message content.
Sender/header features (SPF, DKIM, domain reputation) require full email headers - not available for pasted text.
"""
import re
import math
from collections import Counter
from typing import Dict, Any, List, Set, Optional

# Common URL shorteners and suspicious patterns
URL_SHORTENERS = {
    "bit.ly", "tinyurl.com", "goo.gl", "t.co", "ow.ly", "is.gd", "buff.ly",
    "adf.ly", "bit.do", "lnkd.in", "db.tt", "qr.ae", "cur.lv", "ity.im",
    "q.gs", "po.st", "bc.vc", "twitthis.com", "u.to", "j.mp", "buzurl.com",
    "cutt.ly", "short.io", "rebrand.ly", "bl.ink", "short.link",
}
IMPERATIVE_VERBS = {
    "click", "buy", "claim", "order", "register", "subscribe", "act", "call",
    "reply", "send", "verify", "confirm", "update", "unsubscribe", "open",
}
URGENCY_WORDS = {
    "urgent", "immediately", "asap", "now", "limited", "hurry", "expire",
    "expires", "deadline", "last chance", "act now", "don't wait", "limited time",
    "only today", "final notice", "instant", "quick", "rush", "emergency",
}


def _extract_urls(text: str) -> List[str]:
    """Extract URLs from text."""
    pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    return re.findall(pattern, text, re.IGNORECASE)


def _char_ngrams(text: str, n: int = 3) -> Counter:
    """Character n-grams (e.g. n=3 for trigrams)."""
    text = text.lower().replace(" ", "")
    if len(text) < n:
        return Counter()
    return Counter(text[i:i + n] for i in range(len(text) - n + 1))


def _text_entropy(text: str) -> float:
    """Shannon entropy of character distribution (0 = predictable, higher = more random)."""
    if not text:
        return 0.0
    counter = Counter(text.lower())
    total = len(text)
    return -sum(
        (c / total) * math.log2(c / total)
        for c in counter.values()
    )


def extract_all_features(
    raw_text: str,
    processed_words: Optional[List[str]] = None,
    spam_words_set: Optional[Set[str]] = None,
    ham_words_set: Optional[Set[str]] = None,
) -> Dict[str, Any]:
    """
    Extract all available features from raw message text.
    processed_words: tokenized/stemmed words (e.g. from transformed_text).
    spam_words_set / ham_words_set: known spam/ham word sets for keyword features.
    """
    spam_words_set = spam_words_set or set()
    ham_words_set = ham_words_set or set()
    words = processed_words or [w for w in re.findall(r"\b\w+\b", raw_text) if w]
    word_count = len(words)
    char_count = len(raw_text)
    unique_words = set(w.lower() for w in words)

    # ---- 1. Text content features ----
    spam_keyword_count = sum(1 for w in unique_words if w in spam_words_set)
    ham_keyword_count = sum(1 for w in unique_words if w in ham_words_set)
    word_lengths = [len(w) for w in words if w]
    avg_word_length = sum(word_lengths) / len(word_lengths) if word_lengths else 0

    # Character n-grams (count of unique trigrams as a simple measure)
    char_trigrams = _char_ngrams(raw_text, 3)
    char_ngram_count = len(char_trigrams)
    char_ngram_total = sum(char_trigrams.values())

    # ---- 2. Formatting & style features ----
    letters = [c for c in raw_text if c.isalpha()]
    alpha_count = len(letters)
    upper_count = sum(1 for c in raw_text if c.isupper())
    capital_ratio = upper_count / alpha_count if alpha_count else 0
    exclamation_count = raw_text.count("!")
    question_count = raw_text.count("?")
    special_chars = sum(1 for c in raw_text if c in "$@#%&*")
    all_caps_words = sum(1 for w in re.findall(r"\b[A-Z]+\b", raw_text) if len(w) > 1)

    # ---- 3. URL & link features ----
    urls = _extract_urls(raw_text)
    url_count = len(urls)
    url_shortener_count = 0
    suspicious_ip_url_count = 0
    https_count = 0
    http_count = 0
    for u in urls:
        lower = u.lower()
        if any(short in lower for short in URL_SHORTENERS):
            url_shortener_count += 1
        if re.search(r"https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", u):
            suspicious_ip_url_count += 1
        if lower.startswith("https://"):
            https_count += 1
        elif lower.startswith("http://"):
            http_count += 1

    # ---- 4. Structural features (from pasted text we only have "body") ----
    html_tags = bool(re.search(r"<[a-zA-Z][^>]*>", raw_text))
    # Simple heuristic: colored/hidden text often in style= or color=
    hidden_or_colored = bool(
        re.search(r"style\s*=\s*[^>]*(display:\s*none|color:\s*#?[fF]{6})", raw_text, re.I)
        or re.search(r"color\s*:\s*#?[fF]{6}", raw_text, re.I)
    )

    # ---- 5. Sender & header features ----
    # Not available without full email; we return placeholders.
    sender_domain_reputation = None  # N/A
    free_email_provider = None  # N/A
    reply_to_from_mismatch = None  # N/A
    spf_dkim_dmarc_status = None  # N/A

    # ---- 6. Statistical features ----
    entropy = _text_entropy(raw_text)
    total_word_occurrences = len(words)
    repeated_word_ratio = (
        1 - len(unique_words) / total_word_occurrences
        if total_word_occurrences else 0
    )

    # ---- 7. Behavioral indicators ----
    text_lower = raw_text.lower()
    imperative_count = sum(1 for v in IMPERATIVE_VERBS if re.search(r"\b" + re.escape(v) + r"\b", text_lower))
    urgency_count = sum(1 for u in URGENCY_WORDS if re.search(r"\b" + re.escape(u) + r"\b", text_lower))

    return {
        # 1. Text content
        "word_count": word_count,
        "char_count": char_count,
        "spam_keyword_frequency": spam_keyword_count,
        "ham_keyword_frequency": ham_keyword_count,
        "avg_word_length": round(avg_word_length, 2),
        "char_ngram_count": char_ngram_count,
        "char_ngram_total": char_ngram_total,
        "unique_word_count": len(unique_words),
        # 2. Formatting & style
        "capital_letter_ratio": round(capital_ratio, 4),
        "exclamation_count": exclamation_count,
        "question_mark_count": question_count,
        "special_char_count": special_chars,
        "all_caps_word_count": all_caps_words,
        # 3. URL & link
        "url_count": url_count,
        "url_shortener_count": url_shortener_count,
        "suspicious_ip_url_count": suspicious_ip_url_count,
        "https_link_count": https_count,
        "http_link_count": http_count,
        # 4. Structural
        "html_content_presence": html_tags,
        "hidden_or_colored_text": hidden_or_colored,
        # 5. Sender (N/A for pasted text)
        "sender_domain_reputation": sender_domain_reputation,
        "free_email_provider": free_email_provider,
        "reply_to_from_mismatch": reply_to_from_mismatch,
        "spf_dkim_dmarc_status": spf_dkim_dmarc_status,
        # 6. Statistical
        "text_entropy": round(entropy, 4),
        "repeated_word_ratio": round(repeated_word_ratio, 4),
        # 7. Behavioral
        "imperative_verb_count": imperative_count,
        "urgency_word_count": urgency_count,
    }

import re
import pandas as pd
from pathlib import Path
from collections import Counter


def _data_dir() -> Path:
    """Resolve data directory relative to project root."""
    return Path(__file__).resolve().parent.parent / "Data" / "preprocessed"


def load_word_lists():
    """Load spam/ham word sets from CSV. Use with st.cache_data in app."""
    base = _data_dir()
    spam_path = base / "top_30_most_used_spam_words.csv"
    ham_path = base / "top_30_most_used_ham_words.csv"
    try:
        spam_df = pd.read_csv(spam_path)
        ham_df = pd.read_csv(ham_path)
        return set(spam_df.word.str.lower()), set(ham_df.word.str.lower())
    except (FileNotFoundError, KeyError, pd.errors.EmptyDataError):
        return set(), set()


def analyze_message(raw_text, processed_words, spam_words_set=None, ham_words_set=None):
    """Analyze message for spam indicators.
    
    Args:
        raw_text: Original message text
        processed_words: Tokenized/stemmed words from NLP processing
        spam_words_set: Set of known spam words (optional, defaults to empty set)
        ham_words_set: Set of known ham words (optional, defaults to empty set)
    
    Returns:
        Dictionary with analysis results
    """
    if spam_words_set is None:
        spam_words_set = set()
    if ham_words_set is None:
        ham_words_set = set()
    
    urls = re.findall(r'http[s]?://\S+', raw_text)
    numbers = re.findall(r'\d+', raw_text)

    spam_patterns = {
        'Free/Freebie': bool(re.search(r'\bfree\b', raw_text, re.I)),
        'Win/Prize': bool(re.search(r'\b(win|won|prize)\b', raw_text, re.I)),
        'Urgent': bool(re.search(r'\burgent\b', raw_text, re.I)),
        'Click': bool(re.search(r'\bclick\b', raw_text, re.I)),
    }

    found_spam = [w for w in processed_words if w in spam_words_set]
    found_ham = [w for w in processed_words if w in ham_words_set]

    return {
        "urls": len(urls),
        "numbers": len(numbers),
        "spam_patterns": spam_patterns,
        "found_spam_words": found_spam,
        "found_ham_words": found_ham
    }

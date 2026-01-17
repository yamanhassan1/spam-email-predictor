import re
import pandas as pd
from collections import Counter

def load_word_lists():
    try:
        spam_df = pd.read_csv("Data/preprocessed/top_30_most_used_spam_words.csv")
        ham_df = pd.read_csv("Data/preprocessed/top_30_most_used_ham_words.csv")
        return set(spam_df.word.str.lower()), set(ham_df.word.str.lower())
    except Exception:
        return set(), set()

SPAM_WORDS, HAM_WORDS = load_word_lists()

def analyze_message(raw_text, processed_words):
    urls = re.findall(r'http[s]?://\S+', raw_text)
    numbers = re.findall(r'\d+', raw_text)

    spam_patterns = {
        'Free/Freebie': bool(re.search(r'\bfree\b', raw_text, re.I)),
        'Win/Prize': bool(re.search(r'\b(win|won|prize)\b', raw_text, re.I)),
        'Urgent': bool(re.search(r'\burgent\b', raw_text, re.I)),
        'Click': bool(re.search(r'\bclick\b', raw_text, re.I)),
    }

    found_spam = [w for w in processed_words if w in SPAM_WORDS]
    found_ham = [w for w in processed_words if w in HAM_WORDS]

    return {
        "urls": len(urls),
        "numbers": len(numbers),
        "spam_patterns": spam_patterns,
        "found_spam_words": found_spam,
        "found_ham_words": found_ham
    }

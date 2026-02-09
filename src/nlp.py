import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from typing import Optional, Set

ps = PorterStemmer()


def setup_nltk():
    """Ensure required NLTK resources are available. Download only if missing."""
    # stopwords
    try:
        stopwords.words("english")
    except LookupError:
        nltk.download("stopwords", quiet=True)

    # punkt tokenizer
    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        nltk.download("punkt", quiet=True)

    # punkt_tab (required by newer NLTK versions for sentence tokenization)
    try:
        nltk.data.find("tokenizers/punkt_tab")
    except LookupError:
        try:
            nltk.download("punkt_tab", quiet=True)
        except Exception:
            pass


def get_stopwords() -> Set[str]:
    """Return English stopwords set. Call after setup_nltk(); use st.cache_data in app."""
    try:
        return set(stopwords.words("english"))
    except LookupError:
        nltk.download("stopwords", quiet=True)
        return set(stopwords.words("english"))


def transformed_text(text: str, stop_words: Optional[Set[str]] = None) -> str:
    """Normalize and stem text; exclude stop words. Pass cached stop_words from app when possible."""
    if stop_words is None:
        stop_words = get_stopwords()
    text = text.lower()
    tokens = nltk.word_tokenize(text)
    words = [w for w in tokens if w.isalnum()]
    words = [w for w in words if w not in stop_words]
    words = [ps.stem(w) for w in words]
    return " ".join(words)

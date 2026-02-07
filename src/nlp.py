import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from typing import Optional, Set

ps = PorterStemmer()


def setup_nltk():
    nltk.download("stopwords")
    nltk.download("punkt")
    nltk.download("punkt_tab")


def get_stopwords() -> Set[str]:
    """Return English stopwords set. Call after setup_nltk(); use st.cache_data in app."""
    try:
        return set(stopwords.words("english"))
    except LookupError:
        nltk.download("stopwords")
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

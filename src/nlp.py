import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()

def setup_nltk():
    nltk.download("stopwords")
    nltk.download("punkt")
    nltk.download("punkt_tab")

def get_stopwords():
    try:
        return set(stopwords.words("english"))
    except LookupError:
        nltk.download("stopwords")
        return set(stopwords.words("english"))

STOP_WORDS = get_stopwords()

def transformed_text(text: str) -> str:
    text = text.lower()
    tokens = nltk.word_tokenize(text)

    words = [w for w in tokens if w.isalnum()]
    words = [w for w in words if w not in STOP_WORDS]
    words = [ps.stem(w) for w in words]

    return " ".join(words)

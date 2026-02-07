import pickle
from pathlib import Path


def _model_dir() -> Path:
    """Resolve model directory relative to project root (parent of src)."""
    return Path(__file__).resolve().parent.parent / "Models"


def load_model():
    """Load TF-IDF vectorizer and classifier from disk. Use with st.cache_data in app."""
    base = _model_dir()
    vec_path = base / "vectorizer.pkl"
    model_path = base / "model.pkl"
    if not vec_path.is_file() or not model_path.is_file():
        raise FileNotFoundError(
            f"Model files not found. Expected {vec_path} and {model_path}"
        )
    with open(vec_path, "rb") as f:
        tfidf = pickle.load(f)
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    return tfidf, model


def predict(text: str, tfidf, model):
    vector = tfidf.transform([text])
    prediction = model.predict(vector)[0]
    proba = model.predict_proba(vector)[0]
    return prediction, proba

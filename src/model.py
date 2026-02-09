import pickle
from pathlib import Path
from typing import List, Tuple, Optional, Dict

import numpy as np


def _model_dir() -> Path:
    """Resolve model directory relative to project root (parent of src)."""
    return Path(__file__).resolve().parent.parent / "Models"


def load_model(model_name: str = "default"):
    """Load TF-IDF vectorizer and classifier from disk. Use with st.cache_data in app.

    Naming convention:
      - default: Models/vectorizer.pkl and Models/model.pkl
      - custom:  Models/vectorizer_{name}.pkl and Models/model_{name}.pkl
    """
    base = _model_dir()
    if model_name == "default":
        vec_path = base / "vectorizer.pkl"
        model_path = base / "model.pkl"
    else:
        vec_path = base / f"vectorizer_{model_name}.pkl"
        model_path = base / f"model_{model_name}.pkl"
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
    # Not all models support predict_proba (e.g., LinearSVC). Guard accordingly.
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(vector)[0]
    else:
        # Fallback: produce a pseudo-probability vector centered at 0.5
        # based on decision_function if available; else neutral.
        if hasattr(model, "decision_function"):
            score = float(model.decision_function(vector)[0])
            # Squash to (0,1) and form [ham, spam] ordering
            spam_p = 1 / (1 + np.exp(-score))
            proba = np.array([1 - spam_p, spam_p])
        else:
            proba = np.array([0.5, 0.5])
    return prediction, proba


def list_available_models() -> List[str]:
    """List available model names based on files in Models directory.

    Returns names including 'default' plus any suffixes found in
    model_{name}.pkl and vectorizer_{name}.pkl pairs where both exist.
    """
    base = _model_dir()
    if not base.exists():
        return ["default"]
    names = {"default"}
    model_files = {p.name for p in base.glob("model_*.pkl")}
    vec_files = {p.name for p in base.glob("vectorizer_*.pkl")}

    def _suffix(fname: str, prefix: str) -> Optional[str]:
        if fname.startswith(prefix) and fname.endswith(".pkl"):
            return fname[len(prefix):-4]
        return None

    model_suffixes = {_suffix(f, "model_") for f in model_files}
    vec_suffixes = {_suffix(f, "vectorizer_") for f in vec_files}

    for s in (model_suffixes & vec_suffixes):
        if s:
            names.add(s)
    return sorted(names)


def explain_prediction(
    transformed_text: str,
    tfidf,
    model,
    top_k: int = 10
) -> Dict[str, List[Tuple[str, float]]]:
    """Return word impact explanation for linear models and MultinomialNB.

    Returns a dict with keys:
      - positive: list of (word, contribution)
      - negative: list of (word, contribution)
    Contributions are approximated as (feature_value * weight_diff).
    """
    try:
        feature_names = tfidf.get_feature_names_out()
    except Exception:
        # Legacy support
        feature_names = np.array(tfidf.get_feature_names())

    vec = tfidf.transform([transformed_text])  # 1 x n_features (sparse)
    vec_coo = vec.tocoo()

    pos_list: List[Tuple[str, float]] = []
    neg_list: List[Tuple[str, float]] = []

    weight_diff: Optional[np.ndarray] = None

    # Linear models (LogReg, LinearSVC (if coef_), SGDClassifier, etc.)
    if hasattr(model, "coef_"):
        coef = getattr(model, "coef_")  # shape: (1, n_features) for binary
        if coef is not None:
            if coef.ndim == 2 and coef.shape[0] == 1:
                weight_diff = coef[0]
            elif coef.ndim == 2 and coef.shape[0] == 2:
                weight_diff = coef[1] - coef[0]
    # MultinomialNB
    elif hasattr(model, "feature_log_prob_") and hasattr(model, "classes_"):
        flp = getattr(model, "feature_log_prob_")  # (n_classes, n_features)
        classes = list(getattr(model, "classes_"))
        try:
            spam_idx = classes.index(1)
            ham_idx = classes.index(0)
        except ValueError:
            spam_idx, ham_idx = 1, 0
        weight_diff = flp[spam_idx] - flp[ham_idx]

    if weight_diff is None:
        return {"positive": [], "negative": []}

    # Compute contributions only for non-zero terms in the vector
    for idx, value in zip(vec_coo.col, vec_coo.data):
        contrib = float(value * weight_diff[idx])
        word = str(feature_names[idx])
        if contrib > 0:
            pos_list.append((word, contrib))
        elif contrib < 0:
            neg_list.append((word, contrib))

    pos_list.sort(key=lambda x: x[1], reverse=True)
    neg_list.sort(key=lambda x: x[1])  # most negative first

    return {
        "positive": pos_list[:top_k],
        "negative": neg_list[:top_k],
    }

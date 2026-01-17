import pickle

def load_model():
    tfidf = pickle.load(open("Models/vectorizer.pkl", "rb"))
    model = pickle.load(open("Models/model.pkl", "rb"))
    return tfidf, model

def predict(text: str, tfidf, model):
    vector = tfidf.transform([text])
    prediction = model.predict(vector)[0]
    proba = model.predict_proba(vector)[0]
    return prediction, proba

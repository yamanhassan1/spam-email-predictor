import streamlit as st
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# Download stopwords if missing (allowed at runtime)
import os
nltk_data_path = os.path.join(os.path.expanduser("~"), "nltk_data")
os.makedirs(nltk_data_path, exist_ok=True)
nltk.data.path.append(nltk_data_path)

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords", download_dir=nltk_data_path)

ps = PorterStemmer()
stop_words = set(stopwords.words('english'))

def transformed_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    words = [w for w in text if w.isalnum()]
    words = [w for w in words if w not in stop_words]
    words = [ps.stem(w) for w in words]

    return " ".join(words)

# LOAD TRAINED OBJECTS
tfidf = pickle.load(open("Models/vectorizer.pkl", "rb"))
model = pickle.load(open("Models/model.pkl", "rb"))

st.title("Email / SMS Spam Classifier")

input_sms = st.text_area("Enter your message")

if st.button("Predict"):
    # PREPROCESS
    transformed_sms = transformed_text(input_sms)
    # VECTORIZE
    vector_input = tfidf.transform([transformed_sms])
    # PREDICT
    result = model.predict(vector_input)[0]
    # DISPLAY
    if result == 1:
        st.header("Spam")
    else:
        st.header("Not Spam")

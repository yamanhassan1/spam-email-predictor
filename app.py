import streamlit as st
from src.design import setup_page, render_header
from src.nlp import setup_nltk, transformed_text
from src.model import load_model, predict
from src.analysis import analyze_message
from src.visualization import confidence_gauge, probability_bar

setup_page()
setup_nltk()

tfidf, model = load_model()

render_header()

input_sms = st.text_area("Message", height=220)

if st.button("Analyze"):
    processed = transformed_text(input_sms)
    result, proba = predict(processed, tfidf, model)

    analysis = analyze_message(input_sms, processed.split())

    st.plotly_chart(confidence_gauge(max(proba)*100, result == 1))
    st.plotly_chart(probability_bar(proba[0]*100, proba[1]*100))

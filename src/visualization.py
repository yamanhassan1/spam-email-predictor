import plotly.graph_objects as go

def confidence_gauge(confidence, is_spam):
    return go.Figure(go.Indicator(
        mode="gauge+number",
        value=confidence,
        gauge={'axis': {'range': [0, 100]},
               'bar': {'color': "#f5576c" if is_spam else "#4facfe"}}
    ))

def probability_bar(ham, spam):
    return go.Figure(data=[
        go.Bar(x=['Safe', 'Spam'], y=[ham, spam])
    ])

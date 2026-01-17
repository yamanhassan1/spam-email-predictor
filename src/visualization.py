import plotly.graph_objects as go
import plotly.express as px
from typing import Sequence, List, Tuple, Optional, Dict
from collections import Counter
import base64
import io

# Shared layout defaults for a consistent look
_DEFAULT_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="white", family="Inter, system-ui, -apple-system, 'Segoe UI', Roboto"),
    margin=dict(l=20, r=20, t=40, b=20),
)


def _norm_pct(value: float) -> float:
    """Normalize a probability given either as 0-1 or 0-100 into 0-100 range."""
    v = float(value)
    return v * 100.0 if v <= 1.001 else v


def confidence_gauge(confidence: float, is_spam: bool, height: int = 360, show_threshold: bool = True) -> go.Figure:
    """
    Enhanced gauge with gradient-like steps, clearer number formatting and annotation.
    - confidence: 0-100 (or 0-1)
    - is_spam: whether classification is spam to influence color tone
    - show_threshold: display a 90% threshold marker
    """
    value = max(0.0, min(100.0, _norm_pct(confidence)))
    tone = "#ff6b6b" if is_spam else "#4facfe"
    steps = [
        {'range': [0, 40], 'color': '#2b3340'},
        {'range': [40, 70], 'color': '#223046'},
        {'range': [70, 100], 'color': '#16202b'}
    ]

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        number={'suffix': '%', 'font': {'size': 32, 'color': 'white'}},
        delta={'reference': 50, 'increasing': {'color': tone}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#aab6d6"},
            'bar': {'color': tone, 'thickness': 0.25},
            'bgcolor': "rgba(255,255,255,0.02)",
            'steps': steps,
            'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 90} if show_threshold else None
        },
        domain={'x': [0, 1], 'y': [0, 1]}
    ))

    fig.update_layout(height=height, title={'text': "Model Confidence", 'x': 0.5}, **_DEFAULT_LAYOUT)
    if show_threshold:
        fig.add_annotation(
            x=0.5, y=0.05,
            text=f"<b>Threshold</b>: 90%",
            showarrow=False,
            font=dict(size=11, color="rgba(255,255,255,0.8)")
        )
    return fig


def probability_bar(ham_prob: float, spam_prob: float, height: int = 360, show_annotations: bool = True) -> go.Figure:
    """
    Bar chart showing Safe vs Spam probabilities. Accepts 0-1 or 0-100 inputs.
    Improves hover info, coloring, and includes optional annotation callouts.
    """
    ham = max(0.0, min(100.0, _norm_pct(ham_prob)))
    spam = max(0.0, min(100.0, _norm_pct(spam_prob)))

    colors = ['#4facfe', '#ff6b6b']
    labels = ['Safe (Ham)', 'Spam']
    values = [ham, spam]

    fig = go.Figure(
        data=[
            go.Bar(
                x=labels,
                y=values,
                marker_color=colors,
                text=[f"{v:.1f}%" for v in values],
                textposition='auto',
                hovertemplate="%{x}<br><b>%{y:.1f}%</b><extra></extra>"
            )
        ]
    )
    fig.update_layout(title={'text': "Classification Probabilities", 'x': 0.5}, yaxis_title="Probability (%)", height=height, **_DEFAULT_LAYOUT)
    fig.update_yaxes(range=[0, 100], gridcolor="rgba(255,255,255,0.04)")
    if show_annotations:
        # annotate the dominant class
        dominant = labels[0] if values[0] >= values[1] else labels[1]
        dom_val = max(values)
        fig.add_annotation(x=dominant, y=dom_val + 6, text=f"Predicted: <b>{dominant.split()[0]}</b>", showarrow=False, font=dict(size=12, color="white"))
    return fig


def top_words_bar(words: Sequence[str], freqs: Sequence[int], spam_wordset: Optional[set] = None, height: int = 380) -> go.Figure:
    """
    Horizontal bar for top words.
    - spam_wordset: optional set of spam-indicative words; words present there are highlighted.
    """
    if not words or not freqs:
        fig = go.Figure()
        fig.update_layout(title={"text": "Top Words", "x": 0.5}, height=height, **_DEFAULT_LAYOUT)
        return fig

    spam_wordset = spam_wordset or set()
    colors = ['#7a86ff' if w not in spam_wordset else '#ff8a8a' for w in words]

    fig = go.Figure(
        data=[
            go.Bar(
                x=list(freqs),
                y=list(words),
                orientation='h',
                marker_color=colors,
                text=list(freqs),
                textposition='auto',
                hovertemplate="%{y}: %{x}<extra></extra>"
            )
        ]
    )
    fig.update_layout(title={'text': "Top Words in Message", 'x': 0.5}, height=height, **_DEFAULT_LAYOUT)
    fig.update_xaxes(title_text="Frequency", gridcolor="rgba(255,255,255,0.04)")
    fig.update_yaxes(autorange='reversed')  # show largest on top
    return fig


def characters_pie(labels: Sequence[str], values: Sequence[int], height: int = 320) -> go.Figure:
    """
    Pie chart with center annotation and subtle shadow to display character distribution.
    """
    fig = go.Figure(data=[go.Pie(labels=list(labels), values=list(values), hole=0.45,
                                 marker_colors=['#667eea', '#764ba2'],
                                 hovertemplate="%{label}: %{value}<extra></extra>")])
    total = sum(values) if values else 0
    fig.update_layout(title={'text': "Message Character Distribution", 'x': 0.5}, height=height, **_DEFAULT_LAYOUT)
    fig.add_annotation(x=0.5, y=0.5, text=f"<b>{total}</b> chars", showarrow=False, font=dict(size=12, color="rgba(255,255,255,0.9)"))
    return fig


def word_length_line(lengths: Sequence[int], counts: Sequence[int], height: int = 320) -> go.Figure:
    """
    Smooth line for word length distribution with shaded fill.
    """
    if not lengths or not counts:
        fig = go.Figure()
        fig.update_layout(title={'text': "Word Length Distribution", 'x': 0.5}, height=height, **_DEFAULT_LAYOUT)
        return fig

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(lengths),
        y=list(counts),
        mode='lines+markers',
        marker=dict(color='#ff7b88', size=8),
        line=dict(color='#ff7b88', width=3),
        fill='tozeroy',
        fillcolor='rgba(255,123,136,0.12)',
        hovertemplate='Length %{x}<br>Count %{y}<extra></extra>'
    ))
    fig.update_layout(title={'text': "Word Length Distribution", 'x': 0.5}, height=height, **_DEFAULT_LAYOUT)
    fig.update_xaxes(title_text="Word Length", gridcolor="rgba(255,255,255,0.04)")
    fig.update_yaxes(title_text="Frequency", gridcolor="rgba(255,255,255,0.04)")
    return fig


def wordcloud_figure(words_freq: Dict[str, int], height: int = 360, fallback_to_bar: bool = True) -> go.Figure:
    """
    Try to create a wordcloud. If WordCloud is not available, fallback to the horizontal bar.
    Returns a Plotly figure (image embedded).
    """
    # Lazy import to avoid adding hard deps at import-time
    try:
        from wordcloud import WordCloud
    except Exception:
        # fallback
        if fallback_to_bar:
            words, freqs = zip(*sorted(words_freq.items(), key=lambda x: x[1], reverse=True)[:10]) if words_freq else ([], [])
            return top_words_bar(list(words), list(freqs), height=height)
        fig = go.Figure()
        fig.update_layout(title={'text': "Word Cloud Not Available", 'x': 0.5}, height=height, **_DEFAULT_LAYOUT)
        return fig

    if not words_freq:
        fig = go.Figure()
        fig.update_layout(title={'text': "No Words to Render", 'x': 0.5}, height=height, **_DEFAULT_LAYOUT)
        return fig

    wc = WordCloud(width=800, height=400, background_color=None, mode='RGBA', colormap='viridis')
    wc.generate_from_frequencies(words_freq)

    img = wc.to_image()
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode('utf-8')
    # Render in a Plotly figure as image
    fig = go.Figure()
    fig.add_layout_image(
        dict(
            source="data:image/png;base64," + encoded,
            xref="paper", yref="paper",
            x=0, y=1,
            sizex=1, sizey=1,
            xanchor="left", yanchor="top"
        )
    )
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.update_layout(title={'text': "Word Cloud", 'x': 0.5}, height=height, **_DEFAULT_LAYOUT)
    return fig


def annotated_message_html(raw_text: str, spam_words: Optional[set] = None, ham_words: Optional[set] = None) -> str:
    """
    Return an HTML string where words present in spam_words are highlighted in a red tint
    and ham_words in a green tint. Useful to embed into Streamlit via st.markdown(..., unsafe_allow_html=True).
    """
    import html
    spam_words = spam_words or set()
    ham_words = ham_words or set()

    def _wrap_token(tok: str) -> str:
        lower = tok.lower()
        # Only highlight word tokens (letters/digits)
        if lower in spam_words:
            return f'<span style="background: rgba(255,90,90,0.15); color: #ffdfe0; padding: 2px 6px; border-radius:6px; margin:1px;">{html.escape(tok)}</span>'
        if lower in ham_words:
            return f'<span style="background: rgba(75,199,139,0.12); color: #eafff0; padding: 2px 6px; border-radius:6px; margin:1px;">{html.escape(tok)}</span>'
        return html.escape(tok)

    # Split into tokens but keep punctuation
    import re
    tokens = re.findall(r"\\w+|[^\\w\\s]+|\\s+", raw_text)
    highlighted = "".join(_wrap_token(t) if t.strip() and re.match(r"\\w+", t) else html.escape(t) for t in tokens)
    # Wrap in a container that's responsive
    html_out = f'<div style="line-height:1.6; font-size:0.98rem; color: #eaf0ff;">{highlighted}</div>'
    return html_out


def figure_to_image_bytes(fig: go.Figure, fmt: str = "png") -> Optional[bytes]:
    """
    Return image bytes for a Plotly figure using kaleido if available.
    Returns None if export is not available.
    """
    try:
        img_bytes = fig.to_image(format=fmt)
        return img_bytes
    except Exception:
        return None
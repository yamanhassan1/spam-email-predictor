import plotly.graph_objects as go
import plotly.express as px
from typing import Sequence, List, Tuple, Optional, Dict
from collections import Counter
import base64
import io

# Shared layout defaults for a consistent look and smoother animations
_DEFAULT_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="white", family="Inter, system-ui, -apple-system, 'Segoe UI', Roboto"),
    margin=dict(l=12, r=12, t=36, b=12),
    autosize=True,
    transition={'duration': 420, 'easing': 'cubic-in-out'},
)


def _norm_pct(value: float) -> float:
    """Normalize a probability given either as 0-1 or 0-100 into 0-100 range."""
    v = float(value)
    return v * 100.0 if v <= 1.001 else v


def _apply_responsive(fig: go.Figure, height: Optional[int] = None) -> go.Figure:
    """Apply common responsive settings and optional height to a figure."""
    if height:
        fig.update_layout(height=height)
    fig.update_layout(**_DEFAULT_LAYOUT)
    # smooth entry animation configuration for Plotly; Streamlit animates on update
    fig.layout.transition = dict(duration=420, easing="cubic-in-out")
    return fig


def confidence_gauge(confidence: float, is_spam: bool, height: int = 220, show_threshold: bool = True) -> go.Figure:
    """
    Professional gauge indicating confidence (0-100).
    Default height reduced for more compact layout.
    """
    value = max(0.0, min(100.0, _norm_pct(confidence)))
    bar_color = "#ff6b6b" if is_spam else "#4facfe"

    fig = go.Figure()

    # Primary gauge indicator (compact)
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=value,
        number={'suffix': '%', 'font': {'size': 22, 'color': 'white'}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': 'rgba(255,255,255,0.6)', 'tickfont': {'size': 10}},
            'bar': {'color': bar_color, 'thickness': 0.28},
            'bgcolor': "rgba(255,255,255,0.02)",
            'steps': [
                {'range': [0, 40], 'color': '#2b3340'},
                {'range': [40, 70], 'color': '#223046'},
                {'range': [70, 100], 'color': '#16202b'}
            ],
            'threshold': {'line': {'color': "red", 'width': 3}, 'thickness': 0.7, 'value': 90} if show_threshold else None
        },
        domain={'x': [0, 1], 'y': [0, 1]}
    ))

    # Add subtle ring for visual weight (small donut)
    fig.add_trace(go.Pie(values=[value, 100 - value], hole=0.75,
                         marker_colors=[bar_color, 'rgba(255,255,255,0.02)'],
                         textinfo='none', sort=False, hoverinfo='none', showlegend=False))
    # Ensure indicator sits above the pie
    fig.data = (fig.data[0], fig.data[1])
    fig.update_traces(selector=dict(type='pie'), marker_line_width=0)

    fig.update_layout(title={'text': "Confidence", 'x': 0.5})
    _apply_responsive(fig, height=height)
    return fig


def probability_bar(ham_prob: float, spam_prob: float, height: int = 220, show_annotations: bool = True) -> go.Figure:
    """
    Compact bar chart showing Safe vs Spam probabilities with percent labels and hover info.
    Default height reduced for compact layout.
    """
    ham = max(0.0, min(100.0, _norm_pct(ham_prob)))
    spam = max(0.0, min(100.0, _norm_pct(spam_prob)))

    labels = ['Safe (Ham)', 'Spam']
    values = [ham, spam]
    colors = ['#4facfe', '#ff6b6b']

    fig = go.Figure(
        data=[
            go.Bar(
                x=labels,
                y=values,
                marker_color=colors,
                text=[f"{v:.1f}%" for v in values],
                textposition='auto',
                hovertemplate="%{x}<br><b>%{y:.1f}%</b><extra></extra>",
                marker=dict(line=dict(color='rgba(255,255,255,0.02)', width=1)),
            )
        ]
    )

    fig.update_layout(title={'text': "Classification Probabilities", 'x': 0.5}, yaxis_title="Probability (%)", bargap=0.35)
    fig.update_yaxes(range=[0, 100], gridcolor="rgba(255,255,255,0.04)")
    if show_annotations:
        dominant = labels[0] if values[0] >= values[1] else labels[1]
        dom_val = max(values)
        fig.add_annotation(x=dominant, y=min(dom_val + 6, 100), text=f"Predicted: <b>{dominant.split()[0]}</b>",
                           showarrow=False, font=dict(size=11, color="white"))
    _apply_responsive(fig, height=height)
    return fig


def top_words_bar(words: Sequence[str], freqs: Sequence[int], spam_wordset: Optional[set] = None,
                  height: int = 260) -> go.Figure:
    """
    Horizontal bar for top words. Highlights spam-indicative words.
    Only a single 'Top Words' visualization is provided (wordcloud removed).
    """
    if not words or not freqs:
        fig = go.Figure()
        fig.update_layout(title={"text": "Top Words", "x": 0.5}, height=height, **_DEFAULT_LAYOUT)
        return fig

    spam_wordset = spam_wordset or set()
    colors = ['#7a86ff' if w not in spam_wordset else '#ff8a8a' for w in words]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=list(freqs),
        y=list(words),
        orientation='h',
        marker_color=colors,
        text=list(freqs),
        textposition='auto',
        hovertemplate="%{y}: %{x}<extra></extra>",
    ))
    fig.update_layout(title={'text': "Top Words in Message", 'x': 0.5})
    fig.update_xaxes(title_text="Frequency", gridcolor="rgba(255,255,255,0.04)")
    fig.update_yaxes(autorange='reversed')  # largest on top
    _apply_responsive(fig, height=height)
    return fig


def characters_pie(labels: Sequence[str], values: Sequence[int], height: int = 200) -> go.Figure:
    """
    Compact pie chart for character / space distribution with center annotation.
    """
    total = sum(values) if values else 0
    colors = ['#667eea', '#764ba2']
    fig = go.Figure(data=[go.Pie(labels=list(labels), values=list(values), hole=0.5,
                                 marker_colors=colors,
                                 hovertemplate="%{label}: %{value}<extra></extra>")])
    fig.update_layout(title={'text': "Message Character Distribution", 'x': 0.5})
    fig.add_annotation(x=0.5, y=0.5, text=f"<b>{total}</b> chars", showarrow=False,
                       font=dict(size=11, color="rgba(255,255,255,0.9)"))
    _apply_responsive(fig, height=height)
    return fig


def word_length_line(lengths: Sequence[int], counts: Sequence[int], height: int = 200) -> go.Figure:
    """
    Compact smooth line for word length distribution with shaded fill.
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
        marker=dict(color='#ff7b88', size=6),
        line=dict(color='#ff7b88', width=2.5),
        fill='tozeroy',
        fillcolor='rgba(255,123,136,0.12)',
        hovertemplate='Length %{x}<br>Count %{y}<extra></extra>'
    ))
    fig.update_layout(title={'text': "Word Length Distribution", 'x': 0.5})
    fig.update_xaxes(title_text="Word Length", gridcolor="rgba(255,255,255,0.04)")
    fig.update_yaxes(title_text="Frequency", gridcolor="rgba(255,255,255,0.04)")
    _apply_responsive(fig, height=height)
    return fig


def annotated_message_html(raw_text: str, spam_words: Optional[set] = None, ham_words: Optional[set] = None) -> str:
    """
    Return HTML with inline highlights for spam/ham indicative words.
    Words from spam_words are highlighted with a soft red gradient,
    ham_words with a soft green gradient. Returns a markup-safe, responsive block.
    """
    import html
    spam_words = spam_words or set()
    ham_words = ham_words or set()

    def _wrap_token(tok: str) -> str:
        lower = tok.lower()
        if lower in spam_words:
            return f'<span style="background: linear-gradient(90deg, rgba(255,90,90,0.16), rgba(255,70,70,0.06)); color: #ffdfe0; padding: 6px 10px; border-radius: 999px; margin: 0 4px; display:inline-block;">{html.escape(tok)}</span>'
        if lower in ham_words:
            return f'<span style="background: linear-gradient(90deg, rgba(75,199,139,0.12), rgba(60,180,115,0.04)); color: #eafff0; padding: 6px 10px; border-radius: 999px; margin: 0 4px; display:inline-block;">{html.escape(tok)}</span>'
        return html.escape(tok)

    import re
    tokens = re.findall(r"\w+|[^\w\s]+|\s+", raw_text)
    highlighted = "".join(_wrap_token(t) if t.strip() and re.match(r"\w+", t) else html.escape(t) for t in tokens)
    html_out = f'<div style="line-height:1.7; font-size:0.98rem; color: #eaf0ff;">{highlighted}</div>'
    return html_out


def figure_to_image_bytes(fig: go.Figure, fmt: str = "png") -> Optional[bytes]:
    """
    Return image bytes for a Plotly figure using kaleido if available; otherwise return None.
    """
    try:
        img_bytes = fig.to_image(format=fmt)
        return img_bytes
    except Exception:
        return None
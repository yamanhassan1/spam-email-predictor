import plotly.graph_objects as go
import plotly.express as px
from typing import Sequence, List, Tuple, Optional, Dict
from collections import Counter
import base64
import io

# Premium glassmorphic theme with advanced styling
_PREMIUM_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(10, 14, 39, 0.4)",
    plot_bgcolor="rgba(255, 255, 255, 0.02)",
    font=dict(
        color="#f8fafc",
        family="Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        size=13
    ),
    margin=dict(l=40, r=40, t=60, b=40),
    autosize=True,
    hoverlabel=dict(
        bgcolor="rgba(15, 20, 51, 0.95)",
        font_size=13,
        font_family="Inter",
        bordercolor="rgba(255, 255, 255, 0.1)"
    ),
    title=dict(
        font=dict(size=18, color="#f8fafc", family="Inter"),
        x=0.5,
        xanchor="center",
        y=0.98,
        yanchor="top"
    )
)

# Premium color palette
_COLORS = {
    'primary_blue': '#3b82f6',
    'primary_cyan': '#06b6d4',
    'primary_purple': '#8b5cf6',
    'success_green': '#10b981',
    'success_emerald': '#34d399',
    'danger_red': '#ef4444',
    'danger_rose': '#fb7185',
    'text_muted': '#94a3b8',
    'glass_border': 'rgba(255, 255, 255, 0.08)',
    'gradient_blue': ['#3b82f6', '#06b6d4', '#8b5cf6'],
    'gradient_danger': ['#ef4444', '#fb7185', '#f87171'],
    'gradient_success': ['#10b981', '#34d399', '#6ee7b7']
}


def _norm_pct(value: float) -> float:
    """Normalize a probability given either as 0-1 or 0-100 into 0-100 range."""
    v = float(value)
    return v * 100.0 if v <= 1.001 else v


def _apply_responsive(fig: go.Figure, height: Optional[int] = None) -> go.Figure:
    """Apply premium responsive settings with glassmorphic styling."""
    if height:
        fig.update_layout(height=height)
    
    fig.update_layout(**_PREMIUM_LAYOUT)
    
    # Grid styling for premium look
    fig.update_xaxes(
        gridcolor="rgba(255, 255, 255, 0.04)",
        gridwidth=1,
        zeroline=False,
        showline=True,
        linewidth=1,
        linecolor="rgba(255, 255, 255, 0.08)"
    )
    fig.update_yaxes(
        gridcolor="rgba(255, 255, 255, 0.04)",
        gridwidth=1,
        zeroline=False,
        showline=True,
        linewidth=1,
        linecolor="rgba(255, 255, 255, 0.08)"
    )
    
    return fig


def confidence_gauge(
    confidence: float,
    is_spam: bool,
    height: int = 400,
    show_threshold: bool = True
) -> go.Figure:
    """
    Premium animated gauge with gradient fills and glassmorphic design.
    """
    value = max(0.0, min(100.0, _norm_pct(confidence)))
    
    # Gradient colors based on classification
    if is_spam:
        bar_color = _COLORS['danger_red']
        gradient_colors = _COLORS['gradient_danger']
    else:
        bar_color = _COLORS['success_green']
        gradient_colors = _COLORS['gradient_success']
    
    fig = go.Figure()

    # Main gauge indicator with premium styling
    fig.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        number={
            'suffix': '%',
            'font': {'size': 48, 'color': '#f8fafc', 'family': 'Inter'},
            'valueformat': '.1f'
        },
        delta={
            'reference': 50,
            'increasing': {'color': _COLORS['success_green']},
            'decreasing': {'color': _COLORS['danger_red']}
        },
        gauge={
            'axis': {
                'range': [0, 100],
                'tickwidth': 2,
                'tickcolor': 'rgba(255, 255, 255, 0.3)',
                'tickfont': {'size': 12, 'color': _COLORS['text_muted']},
                'tickmode': 'linear',
                'tick0': 0,
                'dtick': 20
            },
            'bar': {
                'color': bar_color,
                'thickness': 0.3,
                'line': {'color': 'rgba(255, 255, 255, 0.2)', 'width': 2}
            },
            'bgcolor': "rgba(255, 255, 255, 0.02)",
            'borderwidth': 2,
            'bordercolor': "rgba(255, 255, 255, 0.08)",
            'steps': [
                {'range': [0, 33], 'color': 'rgba(59, 130, 246, 0.1)'},
                {'range': [33, 66], 'color': 'rgba(139, 92, 246, 0.1)'},
                {'range': [66, 100], 'color': 'rgba(239, 68, 68, 0.15)'}
            ],
            'threshold': {
                'line': {'color': _COLORS['danger_red'], 'width': 4},
                'thickness': 0.8,
                'value': 85
            } if show_threshold else None
        },
        domain={'x': [0, 1], 'y': [0.15, 1]}
    ))

    # Decorative subtitle
    fig.add_annotation(
        text=f"{'High Risk' if is_spam else 'Low Risk'} Classification",
        x=0.5,
        y=0.05,
        xref="paper",
        yref="paper",
        showarrow=False,
        font=dict(size=14, color=_COLORS['text_muted'], family="Inter"),
        xanchor="center"
    )

    fig.update_layout(
        title={'text': "🎯 Model Confidence Score"},
        height=height
    )
    
    _apply_responsive(fig, height=height)
    return fig


def probability_bar(
    ham_prob: float,
    spam_prob: float,
    height: int = 380,
    show_annotations: bool = True
) -> go.Figure:
    """
    Premium horizontal bar chart with gradient fills and smooth animations.
    """
    ham = max(0.0, min(100.0, _norm_pct(ham_prob)))
    spam = max(0.0, min(100.0, _norm_pct(spam_prob)))

    labels = ['Safe Message', 'Spam Message']
    values = [ham, spam]
    
    fig = go.Figure()

    # Gradient-styled bars
    for idx, (label, val) in enumerate(zip(labels, values)):
        color = _COLORS['success_green'] if idx == 0 else _COLORS['danger_red']
        
        fig.add_trace(go.Bar(
            x=[val],
            y=[label],
            orientation='h',
            name=label,
            marker=dict(
                color=color,
                line=dict(color='rgba(255, 255, 255, 0.1)', width=2),
                opacity=0.9
            ),
            text=f"{val:.1f}%",
            textposition='inside',
            textfont=dict(size=16, color='white', family='Inter', weight=700),
            hovertemplate=f"<b>{label}</b><br>Probability: %{{x:.2f}}%<extra></extra>",
            showlegend=False
        ))

    fig.update_layout(
        title={'text': "📊 Classification Probabilities"},
        xaxis=dict(
            title="Probability (%)",
            range=[0, 105],
            tickfont=dict(size=12)
        ),
        yaxis=dict(
            tickfont=dict(size=14, color='#f8fafc')
        ),
        bargap=0.3,
        height=height
    )
    
    if show_annotations:
        dominant_idx = 0 if values[0] >= values[1] else 1
        dominant_val = max(values)
        
        fig.add_annotation(
            x=dominant_val + 3,
            y=dominant_idx,
            text=f"✓ Predicted",
            showarrow=True,
            arrowhead=2,
            arrowcolor=_COLORS['primary_cyan'],
            arrowwidth=2,
            font=dict(size=13, color=_COLORS['primary_cyan'], family="Inter", weight=600),
            bgcolor="rgba(6, 182, 212, 0.1)",
            bordercolor=_COLORS['primary_cyan'],
            borderwidth=1,
            borderpad=6
        )
    
    _apply_responsive(fig, height=height)
    return fig


def top_words_bar(
    words: Sequence[str],
    freqs: Sequence[int],
    spam_wordset: Optional[set] = None,
    height: int = 420
) -> go.Figure:
    """
    Premium word frequency chart with gradient coloring and smooth animations.
    """
    if not words or not freqs:
        fig = go.Figure()
        fig.update_layout(
            title={"text": "📝 Top Words Analysis"},
            height=height
        )
        _apply_responsive(fig, height=height)
        return fig

    spam_wordset = spam_wordset or set()
    
    # Color words based on spam/safe classification
    colors = [
        _COLORS['danger_red'] if w.lower() in spam_wordset else _COLORS['primary_blue']
        for w in words
    ]
    
    # Create gradient effect for bars
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=list(freqs),
        y=list(words),
        orientation='h',
        marker=dict(
            color=colors,
            line=dict(color='rgba(255, 255, 255, 0.1)', width=1.5),
            opacity=0.85
        ),
        text=list(freqs),
        textposition='outside',
        textfont=dict(size=12, color='#f8fafc', family='Inter'),
        hovertemplate="<b>%{y}</b><br>Frequency: %{x}<extra></extra>",
    ))
    
    fig.update_layout(
        title={'text': "📝 Top Words in Message"},
        xaxis=dict(title="Frequency"),
        yaxis=dict(autorange='reversed', tickfont=dict(size=13)),
        height=height
    )
    
    # Add legend for color coding
    if spam_wordset:
        fig.add_annotation(
            text="🔴 Spam Indicator  🔵 Neutral Word",
            x=0.5,
            y=-0.12,
            xref="paper",
            yref="paper",
            showarrow=False,
            font=dict(size=11, color=_COLORS['text_muted']),
            xanchor="center"
        )
    
    _apply_responsive(fig, height=height)
    return fig


def characters_pie(
    labels: Sequence[str],
    values: Sequence[int],
    height: int = 360
) -> go.Figure:
    """
    Premium donut chart with gradient colors and center annotation.
    """
    total = sum(values) if values else 0
    
    # Gradient color scheme
    colors = ['#3b82f6', '#8b5cf6', '#06b6d4', '#10b981']
    
    fig = go.Figure(data=[go.Pie(
        labels=list(labels),
        values=list(values),
        hole=0.5,
        marker=dict(
            colors=colors,
            line=dict(color='rgba(255, 255, 255, 0.1)', width=2)
        ),
        textfont=dict(size=13, color='white', family='Inter'),
        hovertemplate="<b>%{label}</b><br>Count: %{value}<br>%{percent}<extra></extra>",
        pull=[0.05] * len(labels)  # Slight separation for modern look
    )])
    
    # Center annotation with total
    fig.add_annotation(
        text=f"<b>{total:,}</b>",
        x=0.5,
        y=0.55,
        font=dict(size=32, color='#f8fafc', family='Inter'),
        showarrow=False
    )
    fig.add_annotation(
        text="Total Characters",
        x=0.5,
        y=0.45,
        font=dict(size=12, color=_COLORS['text_muted']),
        showarrow=False
    )
    
    fig.update_layout(
        title={'text': "📊 Character Distribution"},
        height=height,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(size=12, color='#cbd5e1')
        )
    )
    
    _apply_responsive(fig, height=height)
    return fig


def word_length_line(
    lengths: Sequence[int],
    counts: Sequence[int],
    height: int = 360
) -> go.Figure:
    """
    Premium area chart with gradient fill and smooth curves.
    """
    if not lengths or not counts:
        fig = go.Figure()
        fig.update_layout(
            title={'text': "📏 Word Length Distribution"},
            height=height
        )
        _apply_responsive(fig, height=height)
        return fig

    fig = go.Figure()
    
    # Main line with gradient fill
    fig.add_trace(go.Scatter(
        x=list(lengths),
        y=list(counts),
        mode='lines+markers',
        name='Frequency',
        line=dict(
            color=_COLORS['primary_purple'],
            width=3,
            shape='spline',  # Smooth curves
            smoothing=1.0
        ),
        marker=dict(
            color=_COLORS['primary_cyan'],
            size=10,
            line=dict(color='white', width=2)
        ),
        fill='tozeroy',
        fillcolor='rgba(139, 92, 246, 0.15)',
        hovertemplate="<b>Length:</b> %{x} chars<br><b>Count:</b> %{y}<extra></extra>"
    ))
    
    # Add mean line
    if lengths and counts:
        mean_length = sum(l * c for l, c in zip(lengths, counts)) / sum(counts)
        fig.add_shape(
            type="line",
            x0=mean_length,
            y0=0,
            x1=mean_length,
            y1=max(counts),
            line=dict(
                color=_COLORS['primary_cyan'],
                width=2,
                dash="dash"
            )
        )
        fig.add_annotation(
            x=mean_length,
            y=max(counts) * 1.05,
            text=f"Mean: {mean_length:.1f}",
            showarrow=False,
            font=dict(size=11, color=_COLORS['primary_cyan']),
            bgcolor="rgba(6, 182, 212, 0.1)",
            bordercolor=_COLORS['primary_cyan'],
            borderwidth=1,
            borderpad=4
        )
    
    fig.update_layout(
        title={'text': "📏 Word Length Distribution"},
        xaxis=dict(title="Word Length (characters)"),
        yaxis=dict(title="Frequency"),
        height=height
    )
    
    _apply_responsive(fig, height=height)
    return fig


def wordcloud_figure(
    words_freq: Dict[str, int],
    height: int = 400,
    fallback_to_bar: bool = True
) -> go.Figure:
    """
    Premium word cloud with custom styling or fallback to bar chart.
    """
    try:
        from wordcloud import WordCloud
    except Exception:
        if fallback_to_bar:
            items = sorted(words_freq.items(), key=lambda x: x[1], reverse=True)[:15]
            words, freqs = zip(*items) if items else ([], [])
            return top_words_bar(list(words), list(freqs), height=height)
        
        fig = go.Figure()
        fig.update_layout(
            title={'text': "☁️ Word Cloud (Library Not Available)"},
            height=height
        )
        _apply_responsive(fig, height=height)
        return fig

    if not words_freq:
        fig = go.Figure()
        fig.update_layout(
            title={'text': "☁️ Word Cloud (No Data)"},
            height=height
        )
        _apply_responsive(fig, height=height)
        return fig

    # Generate word cloud with premium colors
    wc = WordCloud(
        width=1200,
        height=600,
        background_color=None,
        mode='RGBA',
        colormap='cool',  # Blue/purple gradient
        relative_scaling=0.5,
        min_font_size=10,
        max_font_size=100,
        prefer_horizontal=0.7
    )
    wc.generate_from_frequencies(words_freq)

    img = wc.to_image()
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode('utf-8')

    fig = go.Figure()
    fig.add_layout_image(
        dict(
            source="data:image/png;base64," + encoded,
            xref="paper",
            yref="paper",
            x=0,
            y=1,
            sizex=1,
            sizey=1,
            xanchor="left",
            yanchor="top",
            layer="below"
        )
    )
    
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.update_layout(
        title={'text': "☁️ Word Cloud Visualization"},
        height=height
    )
    
    _apply_responsive(fig, height=height)
    return fig


def annotated_message_html(
    raw_text: str,
    spam_words: Optional[set] = None,
    ham_words: Optional[set] = None
) -> str:
    """
    Premium HTML annotation with glassmorphic badges and gradient highlights.
    """
    import html
    import re
    
    spam_words = spam_words or set()
    ham_words = ham_words or set()

    def _wrap_token(tok: str) -> str:
        lower = tok.lower()
        if lower in spam_words:
            return f'''<span style="
                background: linear-gradient(135deg, rgba(239, 68, 68, 0.2), rgba(251, 113, 133, 0.1));
                color: #fecdd3;
                padding: 6px 12px;
                border-radius: 999px;
                margin: 0 4px 4px 0;
                display: inline-block;
                font-weight: 600;
                font-size: 0.9rem;
                border: 1px solid rgba(239, 68, 68, 0.3);
                box-shadow: 0 4px 12px rgba(239, 68, 68, 0.15);
                backdrop-filter: blur(10px);
                transition: all 0.3s ease;
            ">{html.escape(tok)}</span>'''
        if lower in ham_words:
            return f'''<span style="
                background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(52, 211, 153, 0.1));
                color: #d1fae5;
                padding: 6px 12px;
                border-radius: 999px;
                margin: 0 4px 4px 0;
                display: inline-block;
                font-weight: 600;
                font-size: 0.9rem;
                border: 1px solid rgba(16, 185, 129, 0.3);
                box-shadow: 0 4px 12px rgba(16, 185, 129, 0.15);
                backdrop-filter: blur(10px);
                transition: all 0.3s ease;
            ">{html.escape(tok)}</span>'''
        return html.escape(tok)

    tokens = re.findall(r"\w+|[^\w\s]+|\s+", raw_text)
    highlighted = "".join(
        _wrap_token(t) if t.strip() and re.match(r"\w+", t) else html.escape(t)
        for t in tokens
    )
    
    html_out = f'''
    <div style="
        line-height: 2;
        font-size: 1rem;
        color: #f8fafc;
        background: rgba(255, 255, 255, 0.02);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    ">
        {highlighted}
    </div>
    '''
    return html_out


def figure_to_image_bytes(fig: go.Figure, fmt: str = "png") -> Optional[bytes]:
    """
    Export Plotly figure to image bytes (requires kaleido).
    """
    try:
        img_bytes = fig.to_image(format=fmt, width=1200, height=800, scale=2)
        return img_bytes
    except Exception:
        return None


def create_metric_card(
    title: str,
    value: str,
    subtitle: str = "",
    icon: str = "📊"
) -> str:
    """
    Generate a premium metric card HTML for displaying statistics.
    """
    html = f'''
    <div style="
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.05), rgba(139, 92, 246, 0.03));
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
        height: 100%;
    " onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 12px 48px rgba(0, 0, 0, 0.3)';"
       onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 8px 32px rgba(0, 0, 0, 0.2)';">
        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
            <div style="font-size: 2rem;">{icon}</div>
            <div style="font-size: 0.9rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;">
                {title}
            </div>
        </div>
        <div style="font-size: 2.5rem; font-weight: 900; color: #f8fafc; line-height: 1; margin-bottom: 0.5rem;">
            {value}
        </div>
        {f'<div style="font-size: 0.9rem; color: #cbd5e1;">{subtitle}</div>' if subtitle else ''}
    </div>
    '''
    return html
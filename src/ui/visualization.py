"""
Visualization utilities for batch analysis results.
"""
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

from src.core.models import BatchAnalysisResult


def create_batch_summary_charts(batch_result: BatchAnalysisResult):
    """
    Create summary visualizations for batch analysis.
    
    Args:
        batch_result: BatchAnalysisResult object
    """
    st.markdown("""
    <h4 style='color: var(--text-primary); font-size: 1.25rem; font-weight: 700; 
               margin: 1.5rem 0 1rem 0; text-align: center;'>
        📈 Analysis Visualizations
    </h4>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Spam vs Ham pie chart
        fig_pie = go.Figure(data=[go.Pie(
            labels=['Spam', 'Safe'],
            values=[batch_result.spam_count, batch_result.ham_count],
            marker=dict(
                colors=['#ef4444', '#10b981'],
                line=dict(color='rgba(255, 255, 255, 0.2)', width=2)
            ),
            textinfo='label+percent',
            textfont=dict(size=14, color='white'),
            hole=0.4
        )])
        
        fig_pie.update_layout(
            title=dict(
                text="Message Distribution",
                font=dict(color='#f8fafc', size=16),
                x=0.5,
                xanchor='center'
            ),
            paper_bgcolor='rgba(10, 14, 39, 0.4)',
            plot_bgcolor='rgba(255, 255, 255, 0.02)',
            font=dict(color='#f8fafc'),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            ),
            height=350
        )
        
        st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})
    
    with col2:
        # Confidence distribution histogram
        confidences = [r.confidence for r in batch_result.results]
        
        fig_hist = go.Figure(data=[go.Histogram(
            x=confidences,
            nbinsx=20,
            marker=dict(
                color=confidences,
                colorscale=[[0, '#10b981'], [0.5, '#8b5cf6'], [1, '#ef4444']],
                line=dict(color='rgba(255, 255, 255, 0.2)', width=1)
            ),
            hovertemplate='Confidence: %{x:.1f}%<br>Count: %{y}<extra></extra>'
        )])
        
        fig_hist.update_layout(
            title=dict(
                text="Confidence Distribution",
                font=dict(color='#f8fafc', size=16),
                x=0.5,
                xanchor='center'
            ),
            xaxis_title="Confidence (%)",
            yaxis_title="Count",
            paper_bgcolor='rgba(10, 14, 39, 0.4)',
            plot_bgcolor='rgba(255, 255, 255, 0.02)',
            font=dict(color='#f8fafc'),
            xaxis=dict(
                gridcolor='rgba(255, 255, 255, 0.04)',
                showline=True,
                linecolor='rgba(255, 255, 255, 0.08)'
            ),
            yaxis=dict(
                gridcolor='rgba(255, 255, 255, 0.04)',
                showline=True,
                linecolor='rgba(255, 255, 255, 0.08)'
            ),
            height=350
        )
        
        st.plotly_chart(fig_hist, use_container_width=True, config={'displayModeBar': False})
    
    # Feature comparison
    _render_feature_comparison(batch_result)


def _render_feature_comparison(batch_result: BatchAnalysisResult):
    """Render average feature comparison between spam and safe messages."""
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <h4 style='color: var(--text-primary); font-size: 1.1rem; font-weight: 700; 
               margin: 1rem 0; text-align: center;'>
        🔍 Feature Comparison: Spam vs Safe
    </h4>
    """, unsafe_allow_html=True)
    
    # Calculate averages
    spam_results = [r for r in batch_result.results if r.is_spam]
    ham_results = [r for r in batch_result.results if not r.is_spam]
    
    if not spam_results or not ham_results:
        st.info("ℹ️ Need both spam and safe messages for comparison")
        return
    
    # Average features
    features_to_compare = [
        ('url_count', 'URLs'),
        ('spam_keyword_frequency', 'Spam Keywords'),
        ('exclamation_count', 'Exclamations'),
        ('urgency_word_count', 'Urgency Words'),
        ('all_caps_word_count', 'All Caps Words')
    ]
    
    spam_avgs = []
    ham_avgs = []
    labels = []
    
    for feat, label in features_to_compare:
        spam_avg = sum(getattr(r.features, feat) for r in spam_results) / len(spam_results)
        ham_avg = sum(getattr(r.features, feat) for r in ham_results) / len(ham_results)
        spam_avgs.append(spam_avg)
        ham_avgs.append(ham_avg)
        labels.append(label)
    
    # Create grouped bar chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Spam',
        x=labels,
        y=spam_avgs,
        marker=dict(color='#ef4444', line=dict(color='rgba(255, 255, 255, 0.2)', width=1)),
        hovertemplate='%{x}<br>Spam Avg: %{y:.2f}<extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        name='Safe',
        x=labels,
        y=ham_avgs,
        marker=dict(color='#10b981', line=dict(color='rgba(255, 255, 255, 0.2)', width=1)),
        hovertemplate='%{x}<br>Safe Avg: %{y:.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        barmode='group',
        paper_bgcolor='rgba(10, 14, 39, 0.4)',
        plot_bgcolor='rgba(255, 255, 255, 0.02)',
        font=dict(color='#f8fafc'),
        xaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.04)',
            showline=True,
            linecolor='rgba(255, 255, 255, 0.08)'
        ),
        yaxis=dict(
            title="Average Count",
            gridcolor='rgba(255, 255, 255, 0.04)',
            showline=True,
            linecolor='rgba(255, 255, 255, 0.08)'
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
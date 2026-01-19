import streamlit as st
from collections import Counter
from src.visualization import (
    confidence_gauge,
    probability_bar,
    top_words_bar,
    characters_pie,
    word_length_line,
    wordcloud_figure,
    annotated_message_html,
    create_metric_card,
    message_complexity_radar,
)


def render_analysis_section(
    input_sms, transformed_sms, result, confidence, spam_prob, ham_prob,
    word_count, char_count, char_count_no_spaces, sentence_count,
    words, word_freq, words_list, freq_list, spam_words_set, ham_words_set
):
    """
    Render the complete analysis section including visualizations and pattern analysis.
    """
    # Import here to avoid circular imports
    from src.components.pattern_analysis import render_pattern_analysis
    
    # Statistics section
    render_statistics_section(word_count, char_count, sentence_count, words)
    
    # Visualizations
    render_visualization_section(
        confidence, result, spam_prob, ham_prob,
        words_list, freq_list, word_freq, spam_words_set,
        char_count_no_spaces, char_count, words, word_count, sentence_count
    )
    
    # Pattern analysis
    render_pattern_analysis(
        input_sms, result, confidence, spam_prob, ham_prob,
        words, spam_words_set, ham_words_set
    )


def render_statistics_section(word_count, char_count, sentence_count, words):
    """Render message statistics cards."""
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <h3 style='color: #f8fafc; margin: 2rem 0 1.5rem 0; font-size: 1.5rem; font-weight: 700; letter-spacing: -0.02em;'>
            📊 Message Analysis & Statistics
        </h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(create_metric_card("Words", f"{word_count:,}", "Total word count", "📝"), unsafe_allow_html=True)
    with col2:
        st.markdown(create_metric_card("Characters", f"{char_count:,}", "Including spaces", "🔤"), unsafe_allow_html=True)
    with col3:
        st.markdown(create_metric_card("Sentences", f"{sentence_count:,}", "Detected sentences", "📄"), unsafe_allow_html=True)
    with col4:
        st.markdown(create_metric_card("Unique", f"{len(set(words)):,}", "Unique words", "✨"), unsafe_allow_html=True)


def render_visualization_section(
    confidence, result, spam_prob, ham_prob, words_list, freq_list, word_freq,
    spam_words_set, char_count_no_spaces, char_count, words, word_count, sentence_count
):
    """Render all visualizations."""
    # Confidence and probability charts
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div style='margin-bottom: 0.75rem;'>
                <h4 style='color: #f8fafc; font-size: 1.1rem; font-weight: 700; margin: 0;'>
                    🎯 Prediction Confidence
                </h4>
            </div>
        """, unsafe_allow_html=True)
        fig_gauge = confidence_gauge(confidence, result == 1, show_threshold=True)
        st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})
    
    with col2:
        st.markdown("""
            <div style='margin-bottom: 0.75rem;'>
                <h4 style='color: #f8fafc; font-size: 1.1rem; font-weight: 700; margin: 0;'>
                    📈 Classification Probabilities
                </h4>
            </div>
        """, unsafe_allow_html=True)
        fig_prob = probability_bar(ham_prob, spam_prob)
        st.plotly_chart(fig_prob, use_container_width=True, config={'displayModeBar': False})
    
    # Word analysis
    if words_list:
        render_word_analysis(words_list, freq_list, word_freq, spam_words_set)
    
    # Message characteristics
    render_message_characteristics(char_count_no_spaces, char_count, words, word_count, sentence_count)


def render_word_analysis(words_list, freq_list, word_freq, spam_words_set):
    """Render word frequency analysis section."""
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <h4 style='color: #f8fafc; font-size: 1.25rem; font-weight: 700; margin: 1.5rem 0 1rem 0; letter-spacing: -0.02em;'>
            🔤 Word Frequency Analysis
        </h4>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            <div style='margin-bottom: 0.5rem;'>
                <h5 style='color: #cbd5e1; font-size: 0.95rem; font-weight: 600; margin: 0; text-align: center;'>
                    Top Words Frequency
                </h5>
            </div>
        """, unsafe_allow_html=True)
        fig_words = top_words_bar(words_list, freq_list, spam_wordset=spam_words_set)
        st.plotly_chart(fig_words, use_container_width=True, config={'displayModeBar': False})
    
    with col2:
        st.markdown("""
            <div style='margin-bottom: 0.5rem;'>
                <h5 style='color: #cbd5e1; font-size: 0.95rem; font-weight: 600; margin: 0; text-align: center;'>
                    Word Cloud Visualization
                </h5>
            </div>
        """, unsafe_allow_html=True)
        fig_wc = wordcloud_figure(dict(word_freq))
        # Convert the word cloud visualization to a horizontal bar plot of word frequencies
        import pandas as pd
        word_freq_pd = pd.DataFrame(list(word_freq.items()), columns=["word", "count"])
        top_n = 20
        word_freq_pd = word_freq_pd.sort_values("count", ascending=False).head(top_n)
        import plotly.graph_objects as go
        fig_wc_bar = go.Figure(
            go.Bar(
                x=word_freq_pd["count"][::-1],
                y=word_freq_pd["word"][::-1],
                orientation='h',
                marker=dict(
                    color="#8b5cf6"
                )
            )
        )
        fig_wc_bar.update_layout(
            title="Top Word Frequencies",
            yaxis_title="Word",
            xaxis_title="Frequency",
            plot_bgcolor='rgba(255,255,255,0.01)',
            paper_bgcolor='rgba(255,255,255,0.01)',
            font=dict(color="#f8fafc"),
            margin=dict(t=38, l=90, r=20, b=38),
            title_font_size=16
        )
        st.plotly_chart(fig_wc_bar, use_container_width=True, config={'displayModeBar': False})


def render_message_characteristics(char_count_no_spaces, char_count, words, word_count, sentence_count):
    """Render message characteristics charts."""
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <h4 style='color: #f8fafc; font-size: 1.25rem; font-weight: 700; margin: 1.5rem 0 1rem 0; letter-spacing: -0.02em;'>
            📊 Message Characteristics
        </h4>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        labels = ['Characters (no spaces)', 'Spaces']
        values = [char_count_no_spaces, char_count - char_count_no_spaces]
        fig_chars = characters_pie(labels, values)
        st.plotly_chart(fig_chars, use_container_width=True, config={'displayModeBar': False})
    
    with col2:
        word_lengths = [len(word) for word in words if word]
        if word_lengths:
            length_counts = Counter(word_lengths)
            lengths = sorted(length_counts.keys())
            counts = [length_counts[l] for l in lengths]
            fig_length = word_length_line(lengths, counts)
            st.plotly_chart(fig_length, use_container_width=True, config={'displayModeBar': False})
        else:
            st.markdown("""
                <div class="card" style="text-align: center; padding: 2rem;">
                    <div style="font-size: 2rem; margin-bottom: 1rem;">📊</div>
                    <div style="color: #cbd5e1;">No word data available</div>
                </div>
            """, unsafe_allow_html=True)
    
    with col3:
        avg_word_len = sum(word_lengths) / len(word_lengths) if word_lengths else 0
        fig_radar = message_complexity_radar(
            word_count=word_count,
            char_count=char_count,
            sentence_count=sentence_count,
            unique_word_count=len(set(words)),
            avg_word_length=avg_word_len
        )
        st.plotly_chart(fig_radar, use_container_width=True, config={'displayModeBar': False})
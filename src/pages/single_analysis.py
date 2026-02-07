"""
Prediction analysis page for single message results.
"""
import streamlit as st
from collections import Counter
import nltk

from src.core.models import PredictionResult


def render_single_prediction_analysis(result: PredictionResult, raw_text: str):
    """
    Render detailed analysis for a single prediction.
    
    Args:
        result: PredictionResult object
        raw_text: Original message text
    """
    # Import visualization functions
    from src.visualization import (
        confidence_gauge, probability_bar, create_metric_card
    )
    
    # Statistics section
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <h3 style='color: var(--text-primary); font-size: 1.5rem; font-weight: 700; 
               margin: 2rem 0 1rem 0; text-align: center;'>
        📊 Message Statistics
    </h3>
    """, unsafe_allow_html=True)
    
    sentence_count = len(nltk.sent_tokenize(raw_text))
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            create_metric_card(
                "Words",
                f"{result.features.word_count:,}",
                "Total word count",
                "📝"
            ),
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            create_metric_card(
                "Characters",
                f"{result.features.char_count:,}",
                "Including spaces",
                "🔤"
            ),
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            create_metric_card(
                "Sentences",
                f"{sentence_count:,}",
                "Detected sentences",
                "📄"
            ),
            unsafe_allow_html=True
        )
    
    with col4:
        st.markdown(
            create_metric_card(
                "Unique",
                f"{result.features.unique_word_count:,}",
                "Unique words",
                "✨"
            ),
            unsafe_allow_html=True
        )
    
    # Confidence charts
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <h4 style='color: var(--text-primary); font-size: 1.1rem; font-weight: 700; margin-bottom: 0.75rem;'>
            🎯 Prediction Confidence
        </h4>
        """, unsafe_allow_html=True)
        fig_gauge = confidence_gauge(result.confidence, result.is_spam, show_threshold=True)
        st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})
    
    with col2:
        st.markdown("""
        <h4 style='color: var(--text-primary); font-size: 1.1rem; font-weight: 700; margin-bottom: 0.75rem;'>
            📈 Classification Probabilities
        </h4>
        """, unsafe_allow_html=True)
        fig_prob = probability_bar(result.ham_probability, result.spam_probability)
        st.plotly_chart(fig_prob, use_container_width=True, config={'displayModeBar': False})
    
    # Pattern Analysis
    _render_pattern_analysis(result)
    
    # Advanced Features
    _render_advanced_features(result)


def _render_pattern_analysis(result: PredictionResult):
    """Render spam pattern analysis."""
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <h3 style='color: var(--text-primary); font-size: 1.5rem; font-weight: 700; 
               margin: 2rem 0 1rem 0; text-align: center;'>
        🔍 Spam Pattern Analysis
    </h3>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h4 style='color: var(--danger-red); font-weight: 700; margin-bottom: 1rem; font-size: 1.1rem;'>
                🚨 Spam Indicators
            </h4>
        """, unsafe_allow_html=True)
        
        detected_patterns = [k for k, v in result.spam_patterns.items() if v]
        
        if detected_patterns:
            for pattern in detected_patterns:
                st.markdown(f"""
                <div style='background: rgba(239, 68, 68, 0.1); padding: 0.75rem; 
                            border-radius: 8px; margin-bottom: 0.5rem; border-left: 3px solid var(--danger-red);'>
                    <div style='color: var(--text-primary); font-weight: 600;'>⚠️ {pattern}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='color: var(--text-secondary); text-align: center; padding: 1rem;'>
                No common spam patterns detected
            </div>
            """, unsafe_allow_html=True)
        
        if result.found_spam_words:
            st.markdown(f"""
            <div style='margin-top: 1rem;'>
                <div style='color: var(--text-secondary); font-size: 0.9rem; margin-bottom: 0.5rem;'>
                    Found Spam Keywords ({len(result.found_spam_words)}):
                </div>
                <div style='background: var(--glass-bg); padding: 0.75rem; border-radius: 8px;'>
                    <span style='color: var(--danger-red);'>{', '.join(result.found_spam_words[:10])}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h4 style='color: var(--success-green); font-weight: 700; margin-bottom: 1rem; font-size: 1.1rem;'>
                ✅ Safe Indicators
            </h4>
        """, unsafe_allow_html=True)
        
        if result.found_ham_words:
            st.markdown(f"""
            <div style='background: rgba(16, 185, 129, 0.1); padding: 0.75rem; 
                        border-radius: 8px; border-left: 3px solid var(--success-green);'>
                <div style='color: var(--text-primary); font-weight: 600;'>
                    ✓ {len(result.found_ham_words)} safe keywords found
                </div>
            </div>
            
            <div style='margin-top: 1rem;'>
                <div style='color: var(--text-secondary); font-size: 0.9rem; margin-bottom: 0.5rem;'>
                    Found Safe Keywords:
                </div>
                <div style='background: var(--glass-bg); padding: 0.75rem; border-radius: 8px;'>
                    <span style='color: var(--success-green);'>{', '.join(result.found_ham_words[:10])}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='color: var(--text-secondary); text-align: center; padding: 1rem;'>
                No specific safe keywords identified
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)


def _render_advanced_features(result: PredictionResult):
    """Render advanced feature analysis."""
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <h3 style='color: var(--text-primary); font-size: 1.5rem; font-weight: 700; 
               margin: 2rem 0 1rem 0; text-align: center;'>
        🔬 Advanced Feature Analysis
    </h3>
    """, unsafe_allow_html=True)
    
    features = result.features
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h4 style='color: var(--primary-blue); font-weight: 700; margin-bottom: 1rem; font-size: 1rem;'>
                📝 Content Features
            </h4>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style='font-size: 0.9rem;'>
            <div style='display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid var(--glass-border);'>
                <span style='color: var(--text-secondary);'>Avg Word Length</span>
                <strong style='color: var(--text-primary);'>{features.avg_word_length}</strong>
            </div>
            <div style='display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid var(--glass-border);'>
                <span style='color: var(--text-secondary);'>Text Entropy</span>
                <strong style='color: var(--text-primary);'>{features.text_entropy}</strong>
            </div>
            <div style='display: flex; justify-content: space-between; padding: 0.5rem 0;'>
                <span style='color: var(--text-secondary);'>Repeated Words</span>
                <strong style='color: var(--text-primary);'>{features.repeated_word_ratio*100:.1f}%</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h4 style='color: var(--primary-purple); font-weight: 700; margin-bottom: 1rem; font-size: 1rem;'>
                🎨 Format Features
            </h4>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style='font-size: 0.9rem;'>
            <div style='display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid var(--glass-border);'>
                <span style='color: var(--text-secondary);'>Capital Ratio</span>
                <strong style='color: var(--text-primary);'>{features.capital_letter_ratio*100:.1f}%</strong>
            </div>
            <div style='display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid var(--glass-border);'>
                <span style='color: var(--text-secondary);'>Exclamations</span>
                <strong style='color: var(--text-primary);'>{features.exclamation_count}</strong>
            </div>
            <div style='display: flex; justify-content: space-between; padding: 0.5rem 0;'>
                <span style='color: var(--text-secondary);'>All Caps Words</span>
                <strong style='color: var(--text-primary);'>{features.all_caps_word_count}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card">
            <h4 style='color: var(--primary-cyan); font-weight: 700; margin-bottom: 1rem; font-size: 1rem;'>
                🔗 URL Features
            </h4>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style='font-size: 0.9rem;'>
            <div style='display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid var(--glass-border);'>
                <span style='color: var(--text-secondary);'>Total URLs</span>
                <strong style='color: var(--text-primary);'>{features.url_count}</strong>
            </div>
            <div style='display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid var(--glass-border);'>
                <span style='color: var(--text-secondary);'>Shorteners</span>
                <strong style='color: var(--danger-red);'>{features.url_shortener_count}</strong>
            </div>
            <div style='display: flex; justify-content: space-between; padding: 0.5rem 0;'>
                <span style='color: var(--text-secondary);'>Suspicious URLs</span>
                <strong style='color: var(--danger-red);'>{features.suspicious_ip_url_count}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
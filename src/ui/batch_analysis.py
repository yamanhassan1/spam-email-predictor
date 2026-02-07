"""
Batch analysis UI component for multiple message analysis.
"""
import streamlit as st
from typing import List

from src.core.models import BatchAnalysisResult, PredictionResult
from src.ui.visualization import create_batch_summary_charts


def render_batch_analysis_results(batch_result: BatchAnalysisResult):
    """
    Render batch analysis results with summary and individual message details.
    
    Args:
        batch_result: BatchAnalysisResult object
    """
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <div style="font-size: 3.5rem; margin-bottom: 0.5rem;">📊</div>
        <h2 style='color: var(--text-primary); font-size: 2rem; font-weight: 800; margin-bottom: 0.5rem;'>
            Batch Analysis Complete
        </h2>
        <p style='color: var(--text-secondary); font-size: 1rem;'>
            {batch_result.total_messages} messages analyzed in {batch_result.processing_time:.2f}s
        </p>
    </div>
    """.format(batch_result=batch_result), unsafe_allow_html=True)
    
    # Summary statistics
    _render_batch_summary(batch_result)
    
    # Visualization
    st.markdown("<br>", unsafe_allow_html=True)
    create_batch_summary_charts(batch_result)
    
    # Individual results
    st.markdown("<br>", unsafe_allow_html=True)
    _render_individual_results(batch_result.results)
    
    # Export option
    st.markdown("<br>", unsafe_allow_html=True)
    _render_export_option(batch_result)


def _render_batch_summary(batch_result: BatchAnalysisResult):
    """Render summary statistics cards."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="card animate" style="text-align: center; background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(6, 182, 212, 0.05));">
            <div style="font-size: 2.5rem; font-weight: 900; color: var(--primary-blue); margin-bottom: 0.5rem;">
                {batch_result.total_messages}
            </div>
            <p style="color: var(--text-secondary); font-size: 0.9rem; margin: 0;">
                Total Messages
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        spam_pct = batch_result.spam_percentage
        color = "var(--danger-red)" if spam_pct > 50 else "var(--primary-purple)"
        st.markdown(f"""
        <div class="card animate" style="text-align: center; background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(220, 38, 38, 0.05));">
            <div style="font-size: 2.5rem; font-weight: 900; color: {color}; margin-bottom: 0.5rem;">
                {batch_result.spam_count}
            </div>
            <p style="color: var(--text-secondary); font-size: 0.9rem; margin: 0;">
                Spam ({spam_pct:.1f}%)
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        ham_pct = batch_result.ham_percentage
        st.markdown(f"""
        <div class="card animate" style="text-align: center; background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(5, 150, 105, 0.05));">
            <div style="font-size: 2.5rem; font-weight: 900; color: var(--success-green); margin-bottom: 0.5rem;">
                {batch_result.ham_count}
            </div>
            <p style="color: var(--text-secondary); font-size: 0.9rem; margin: 0;">
                Safe ({ham_pct:.1f}%)
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="card animate" style="text-align: center; background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(124, 58, 237, 0.05));">
            <div style="font-size: 2.5rem; font-weight: 900; color: var(--primary-purple); margin-bottom: 0.5rem;">
                {batch_result.average_confidence:.1f}%
            </div>
            <p style="color: var(--text-secondary); font-size: 0.9rem; margin: 0;">
                Avg Confidence
            </p>
        </div>
        """, unsafe_allow_html=True)


def _render_individual_results(results: List[PredictionResult]):
    """Render individual message results in an expandable list."""
    
    st.markdown("""
    <h3 style='color: var(--text-primary); font-size: 1.25rem; font-weight: 700; 
               margin: 2rem 0 1rem 0; text-align: center;'>
        📋 Individual Message Results
    </h3>
    """, unsafe_allow_html=True)
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_type = st.selectbox(
            "Filter by Type",
            ["All Messages", "Spam Only", "Safe Only"],
            key="batch_filter_type"
        )
    
    with col2:
        sort_by = st.selectbox(
            "Sort by",
            ["Order", "Confidence (High to Low)", "Confidence (Low to High)"],
            key="batch_sort"
        )
    
    with col3:
        limit = st.selectbox(
            "Show",
            [10, 25, 50, 100, "All"],
            key="batch_limit"
        )
    
    # Filter results
    filtered_results = results
    
    if filter_type == "Spam Only":
        filtered_results = [r for r in results if r.is_spam]
    elif filter_type == "Safe Only":
        filtered_results = [r for r in results if not r.is_spam]
    
    # Sort results
    if sort_by == "Confidence (High to Low)":
        filtered_results = sorted(filtered_results, key=lambda x: x.confidence, reverse=True)
    elif sort_by == "Confidence (Low to High)":
        filtered_results = sorted(filtered_results, key=lambda x: x.confidence)
    
    # Limit results
    if limit != "All":
        filtered_results = filtered_results[:int(limit)]
    
    # Display count
    st.markdown(f"""
    <p style='color: var(--text-secondary); text-align: center; margin-bottom: 1rem;'>
        Showing {len(filtered_results)} of {len(results)} messages
    </p>
    """, unsafe_allow_html=True)
    
    # Display results
    for i, result in enumerate(filtered_results, 1):
        _render_message_card(i, result)


def _render_message_card(index: int, result: PredictionResult):
    """Render individual message result card."""
    
    # Determine colors and icons
    if result.is_spam:
        border_color = "var(--danger-red)"
        bg_gradient = "linear-gradient(135deg, rgba(239, 68, 68, 0.08), rgba(220, 38, 38, 0.04))"
        icon = "🚨"
        label = "SPAM"
        label_color = "var(--danger-red)"
    else:
        border_color = "var(--success-green)"
        bg_gradient = "linear-gradient(135deg, rgba(16, 185, 129, 0.08), rgba(5, 150, 105, 0.04))"
        icon = "✅"
        label = "SAFE"
        label_color = "var(--success-green)"
    
    # Message preview (first 150 chars)
    message_preview = result.processed_text[:150]
    if len(result.processed_text) > 150:
        message_preview += "..."
    
    with st.expander(f"{icon} Message #{index} - {label} ({result.confidence:.1f}%)", expanded=False):
        st.markdown(f"""
        <div class="card" style="background: {bg_gradient}; border-left: 3px solid {border_color};">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
                <div>
                    <span style="background: {label_color}; color: white; padding: 0.25rem 0.75rem; 
                                border-radius: 12px; font-size: 0.75rem; font-weight: 700;">
                        {label}
                    </span>
                </div>
                <div style="text-align: right;">
                    <div style="color: var(--text-primary); font-weight: 700; font-size: 1.1rem;">
                        {result.confidence:.2f}%
                    </div>
                    <div style="color: var(--text-secondary); font-size: 0.85rem;">
                        {result.confidence_level.value.replace('_', ' ').title()}
                    </div>
                </div>
            </div>
            
            <div style="background: var(--glass-bg); padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
                <div style="color: var(--text-secondary); font-size: 0.85rem; margin-bottom: 0.5rem; font-weight: 600;">
                    Preview:
                </div>
                <div style="color: var(--text-primary); font-size: 0.9rem; line-height: 1.6; font-family: monospace;">
                    {message_preview}
                </div>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 0.75rem;">
                <div style="background: var(--glass-bg); padding: 0.75rem; border-radius: 6px;">
                    <div style="color: var(--text-secondary); font-size: 0.8rem;">Words</div>
                    <div style="color: var(--text-primary); font-weight: 700;">{result.features.word_count}</div>
                </div>
                <div style="background: var(--glass-bg); padding: 0.75rem; border-radius: 6px;">
                    <div style="color: var(--text-secondary); font-size: 0.8rem;">URLs</div>
                    <div style="color: var(--text-primary); font-weight: 700;">{result.features.url_count}</div>
                </div>
                <div style="background: var(--glass-bg); padding: 0.75rem; border-radius: 6px;">
                    <div style="color: var(--text-secondary); font-size: 0.8rem;">Spam Keywords</div>
                    <div style="color: var(--danger-red); font-weight: 700;">{result.features.spam_keyword_frequency}</div>
                </div>
                <div style="background: var(--glass-bg); padding: 0.75rem; border-radius: 6px;">
                    <div style="color: var(--text-secondary); font-size: 0.8rem;">Risk Level</div>
                    <div style="color: {label_color}; font-weight: 700;">{result.get_risk_level()}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def _render_export_option(batch_result: BatchAnalysisResult):
    """Render export options for batch results."""
    import json
    
    st.markdown("""
    <h4 style='color: var(--text-primary); font-size: 1.1rem; font-weight: 700; 
               margin: 2rem 0 1rem 0; text-align: center;'>
        💾 Export Results
    </h4>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Prepare export data
        export_data = batch_result.to_dict()
        json_str = json.dumps(export_data, indent=2)
        
        st.download_button(
            label="📥 Download Results (JSON)",
            data=json_str,
            file_name=f"spam_analysis_{batch_result.results[0].analysis_timestamp.strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )
"""
File upload component for batch message analysis.
"""
import streamlit as st
from typing import List, Optional

from src.core.file_handler import SecureFileHandler, FileValidationError
from src.core.models import FileUploadResult


def render_file_upload_section() -> Optional[List[FileUploadResult]]:
    """
    Render file upload interface with validation and preview.
    
    Returns:
        List of FileUploadResult objects if files processed, else None
    """
    st.markdown("""
    <div class="card" style="margin-bottom: 2rem;">
        <div style="text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📁</div>
            <h3 style='color: #f8fafc; margin-bottom: 0.75rem; font-size: 1.1rem; font-weight: 700;'>
                Upload Message Files
            </h3>
            <p style='color: #cbd5e1; margin-bottom: 1rem; line-height: 1.6; font-size: 0.95rem;'>
                Upload email files (.txt, .eml, .csv) for batch analysis. 
                Maximum 10MB per file, up to 1000 messages per file.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Choose files",
        type=['txt', 'eml', 'csv', 'msg'],
        accept_multiple_files=True,
        help="Supported formats: .txt (plain text), .eml (email), .csv (with 'message' column)",
        label_visibility="collapsed"
    )
    
    if not uploaded_files:
        return None
    
    # Initialize file handler
    file_handler = SecureFileHandler()
    
    # Process button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        process_button = st.button(
            f"📤 Process {len(uploaded_files)} File(s)",
            use_container_width=True,
            type="primary"
        )
    
    if not process_button:
        # Show file preview
        with st.expander("📋 Files Ready for Processing", expanded=True):
            for i, file in enumerate(uploaded_files, 1):
                file_size_kb = file.size / 1024
                st.markdown(f"""
                <div style="background: var(--glass-bg); border: 1px solid var(--glass-border); 
                            border-radius: 8px; padding: 0.75rem; margin-bottom: 0.5rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong style="color: var(--text-primary);">{i}. {file.name}</strong>
                            <div style="color: var(--text-secondary); font-size: 0.85rem; margin-top: 0.25rem;">
                                Size: {file_size_kb:.1f} KB
                            </div>
                        </div>
                        <div style="color: var(--success-green); font-size: 1.5rem;">✓</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        return None
    
    # Process files
    with st.spinner(f"🔍 Processing {len(uploaded_files)} file(s)..."):
        results = file_handler.process_multiple_files(uploaded_files)
    
    # Display results
    _display_upload_results(results)
    
    return results


def _display_upload_results(results: List[FileUploadResult]):
    """Display file upload processing results."""
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <h4 style='color: var(--text-primary); font-size: 1.25rem; font-weight: 700; 
               margin: 1.5rem 0 1rem 0; text-align: center;'>
        📊 Upload Results
    </h4>
    """, unsafe_allow_html=True)
    
    # Summary statistics
    total_files = len(results)
    successful = sum(1 for r in results if r.success)
    failed = total_files - successful
    total_messages = sum(r.messages_extracted for r in results if r.success)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="card" style="text-align: center; background: var(--glass-bg);">
            <div style="font-size: 2rem; font-weight: 900; color: var(--primary-blue); margin-bottom: 0.5rem;">
                {successful}
            </div>
            <p style="color: var(--text-secondary); font-size: 0.9rem; margin: 0;">
                Files Processed
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="card" style="text-align: center; background: var(--glass-bg);">
            <div style="font-size: 2rem; font-weight: 900; color: var(--success-green); margin-bottom: 0.5rem;">
                {total_messages}
            </div>
            <p style="color: var(--text-secondary); font-size: 0.9rem; margin: 0;">
                Messages Extracted
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        color = "var(--danger-red)" if failed > 0 else "var(--text-muted)"
        st.markdown(f"""
        <div class="card" style="text-align: center; background: var(--glass-bg);">
            <div style="font-size: 2rem; font-weight: 900; color: {color}; margin-bottom: 0.5rem;">
                {failed}
            </div>
            <p style="color: var(--text-secondary); font-size: 0.9rem; margin: 0;">
                Failed
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Detailed results
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Successful files
    if successful > 0:
        with st.expander(f"✅ Successfully Processed ({successful})", expanded=True):
            for result in results:
                if result.success:
                    st.markdown(f"""
                    <div class="card" style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.05), rgba(5, 150, 105, 0.03)); 
                                border-left: 3px solid var(--success-green); margin-bottom: 0.75rem;">
                        <div style="display: flex; justify-content: space-between; align-items: start;">
                            <div style="flex: 1;">
                                <div style="color: var(--text-primary); font-weight: 700; margin-bottom: 0.5rem;">
                                    📄 {result.filename}
                                </div>
                                <div style="color: var(--text-secondary); font-size: 0.9rem;">
                                    Format: <strong>{result.file_type}</strong> • 
                                    Messages: <strong style="color: var(--success-green);">{result.messages_extracted}</strong>
                                </div>
                            </div>
                            <div style="color: var(--success-green); font-size: 1.5rem;">✓</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Failed files
    if failed > 0:
        with st.expander(f"❌ Failed Files ({failed})", expanded=True):
            for result in results:
                if not result.success:
                    st.markdown(f"""
                    <div class="card" style="background: linear-gradient(135deg, rgba(239, 68, 68, 0.05), rgba(220, 38, 38, 0.03)); 
                                border-left: 3px solid var(--danger-red); margin-bottom: 0.75rem;">
                        <div>
                            <div style="color: var(--text-primary); font-weight: 700; margin-bottom: 0.5rem;">
                                📄 {result.filename}
                            </div>
                            <div style="color: var(--danger-red); font-size: 0.9rem; background: rgba(239, 68, 68, 0.1); 
                                        padding: 0.5rem; border-radius: 6px; margin-top: 0.5rem;">
                                ⚠️ Error: {result.error_message}
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)


def render_batch_mode_selector() -> str:
    """
    Render mode selector for single vs batch analysis.
    
    Returns:
        Selected mode: 'single' or 'batch'
    """
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h3 style='color: var(--text-primary); font-size: 1.2rem; font-weight: 700; margin-bottom: 1rem;'>
            🎯 Analysis Mode
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(
            "📝 Single Message\nAnalyze one message",
            use_container_width=True,
            key="mode_single"
        ):
            st.session_state.analysis_mode = 'single'
    
    with col2:
        if st.button(
            "📁 Batch Upload\nAnalyze multiple files",
            use_container_width=True,
            key="mode_batch"
        ):
            st.session_state.analysis_mode = 'batch'
    
    # Initialize mode if not set
    if 'analysis_mode' not in st.session_state:
        st.session_state.analysis_mode = 'single'
    
    return st.session_state.analysis_mode
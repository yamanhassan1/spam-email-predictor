# ============================================
# src/components/__init__.py
# ============================================
"""
Components module for the spam detector application.
Contains reusable UI components.

This module provides modular, reusable components:
- input_section: Styled text input area for message analysis
- pattern_analysis: Pattern detection and indicator analysis
"""

from . import input_section
from . import pattern_analysis

__all__ = [
    'input_section',
    'pattern_analysis',
]
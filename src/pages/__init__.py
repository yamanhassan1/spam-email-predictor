# ============================================
# src/pages/__init__.py
# ============================================
"""
Pages module for the spam detector application.
Contains all page-level rendering logic.

This module organizes the application into distinct pages:
- home: Main prediction and input interface
- prediction_analysis: Visualization and analysis components
- info_sections: Static informational content
"""

from . import home
from . import prediction_analysis
from . import info_sections

__all__ = [
    'home',
    'prediction_analysis',
    'info_sections',
]

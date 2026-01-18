# src/pages/__init__.py
"""
Page-level modules for the Spam Detector app.
Each page must be safe to import (no Streamlit execution at import time).
"""

from . import home
from . import prediction_analysis
from . import info_sections

__all__ = [
    "home",
    "prediction_analysis",
    "info_sections",
]

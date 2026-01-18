# src/pages/__init__.py

"""
Page-level modules for the Spam Detector app.
"""

try:
    from . import home
except Exception as e:
    raise ImportError("Failed to import home page") from e

try:
    from . import prediction_analysis
except Exception as e:
    raise ImportError("Failed to import prediction_analysis page") from e

try:
    from . import info_sections
except Exception as e:
    raise ImportError("Failed to import info_sections page") from e


__all__ = [
    "home",
    "prediction_analysis",
    "info_sections",
]

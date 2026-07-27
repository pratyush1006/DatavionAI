"""
Telemedicine selectors module.
"""

from __future__ import annotations

from apps.telemedicine.selectors.recording import RecordingSelector
from apps.telemedicine.selectors.session import SessionSelector

__all__ = [
    "RecordingSelector",
    "SessionSelector",
]

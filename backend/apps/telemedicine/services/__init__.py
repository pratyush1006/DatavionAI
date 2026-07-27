"""
Telemedicine services module.
"""

from __future__ import annotations

from apps.telemedicine.services.recording import RecordingService
from apps.telemedicine.services.session import SessionService

__all__ = [
    "RecordingService",
    "SessionService",
]

"""
Telemedicine models module.
"""

from __future__ import annotations

from apps.telemedicine.models.participant import Participant
from apps.telemedicine.models.recording import Recording
from apps.telemedicine.models.session import TelemedicineSession

__all__ = [
    "Participant",
    "Recording",
    "TelemedicineSession",
]

"""
Patient Preference models.
"""

from .communication_preference import (
    PatientCommunicationPreference,
)
from .preference import (
    PatientPreference,
)

__all__ = [
    "PatientCommunicationPreference",
    "PatientPreference",
]

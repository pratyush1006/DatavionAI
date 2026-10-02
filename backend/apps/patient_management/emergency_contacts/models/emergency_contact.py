"""Legacy compatibility alias for EmergencyContact.

The canonical EmergencyContact Django model lives in:

    apps.patient_management.emergency.models.emergency
"""

from apps.patient_management.emergency.models.emergency import (
    EmergencyContact,
)

__all__ = ("EmergencyContact",)

"""Factories for patient emergency tests."""

from __future__ import annotations

from apps.patient_management.emergency.constants import (
    EmergencyContactPriority,
    EmergencyContactType,
)


def emergency_contact_payload() -> dict:
    """Return a valid emergency contact payload for tests."""

    return {
        "name": "Emergency Contact",
        "relationship": EmergencyContactType.FAMILY,
        "phone": "+91 9000000000",
        "priority": EmergencyContactPriority.SECONDARY,
        "notes": "",
    }


__all__ = ("emergency_contact_payload",)

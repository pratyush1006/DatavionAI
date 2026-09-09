"""
Patient Registration permissions.

Public permission API for the Patient Registration bounded context.
"""

from __future__ import annotations

from apps.patient_management.registration.permissions.registration import (
    CanCancelRegistration,
    CanCheckInRegistration,
    CanCompleteRegistration,
    CanCreateRegistration,
    CanDeleteRegistration,
    CanNoShowRegistration,
    CanRejectRegistration,
    CanUpdateRegistration,
    CanVerifyRegistration,
    CanViewRegistration,
)

__all__ = (
    "CanCancelRegistration",
    "CanCheckInRegistration",
    "CanCompleteRegistration",
    "CanCreateRegistration",
    "CanDeleteRegistration",
    "CanNoShowRegistration",
    "CanRejectRegistration",
    "CanUpdateRegistration",
    "CanVerifyRegistration",
    "CanViewRegistration",
)

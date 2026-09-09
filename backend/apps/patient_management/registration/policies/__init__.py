"""
Authorization policies for Patient Registration.

Public policy API for the Patient Registration bounded context.
"""

from __future__ import annotations

from apps.patient_management.registration.policies.registration import (
    RegistrationPolicy,
)

__all__ = ("RegistrationPolicy",)

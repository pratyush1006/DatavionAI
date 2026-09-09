"""Business validators for medical history."""

from __future__ import annotations

from django.core.exceptions import ValidationError

from apps.patient_management.medical_history.constants import (
    AlcoholUse,
    ClinicalStatus,
    MedicalHistoryType,
)


def validate_history_type(value: str) -> None:
    """Validate history type."""
    if value not in MedicalHistoryType.values:
        raise ValidationError("Invalid medical history type.")


def validate_clinical_status(value: str) -> None:
    """Validate clinical status."""
    if value not in ClinicalStatus.values:
        raise ValidationError("Invalid clinical status.")


def validate_alcohol_use(value: str | None) -> None:
    """Validate alcohol use."""
    if value and value not in AlcoholUse.values:
        raise ValidationError("Invalid alcohol-use value.")


def validate_title(value: str) -> None:
    """Validate title."""
    if not value or not value.strip():
        raise ValidationError("Title is required.")


__all__ = (
    "validate_history_type",
    "validate_clinical_status",
    "validate_alcohol_use",
    "validate_title",
)

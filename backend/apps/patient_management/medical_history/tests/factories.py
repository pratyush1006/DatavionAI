"""Factories."""

from __future__ import annotations

from apps.patient_management.medical_history.models import PatientMedicalHistory


def medical_history_defaults(**overrides):
    """Medical history defaults."""
    data = {
        "history_type": "condition",
        "title": "Hypertension",
        "description": "Test history",
        "clinical_status": "active",
    }
    data.update(overrides)
    return data


def build_medical_history(**overrides):
    """Build medical history."""
    return PatientMedicalHistory(**medical_history_defaults(**overrides))


__all__ = (
    "medical_history_defaults",
    "build_medical_history",
)

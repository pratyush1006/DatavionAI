"""Architecture tests for Patient Preferences."""

from __future__ import annotations

from apps.patient_management.patients.models import Patient
from apps.patient_management.preferences.models import PatientPreference


def test_canonical_patient_is_used():
    """Ensure Patient Preferences reference the canonical Patient model."""

    assert PatientPreference._meta.get_field("patient").remote_field.model is Patient


def test_patient_preference_is_soft_deletable():
    """Ensure Patient Preferences use the platform lifecycle contract."""

    assert hasattr(PatientPreference, "all_objects")
    assert hasattr(PatientPreference, "deleted_objects")


def test_patient_preference_is_organization_scoped():
    """Ensure the organization relationship exists."""

    assert PatientPreference._meta.get_field("organization") is not None

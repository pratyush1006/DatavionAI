"""Querysets for Patient Preferences."""

from __future__ import annotations

from apps.core.models import SoftDeleteQuerySet


class PatientPreferenceQuerySet(SoftDeleteQuerySet):
    """Provide reusable patient preference query helpers."""

    def for_organization(self, organization_id):
        """Restrict preferences to one organization."""

        return self.filter(organization_id=organization_id)

    def for_patient(self, patient_id):
        """Restrict preferences to one patient."""

        return self.filter(patient_id=patient_id)


class PatientCommunicationPreferenceQuerySet(SoftDeleteQuerySet):
    """Provide reusable communication preference query helpers."""

    def for_preference(self, preference_id):
        """Restrict channel preferences to one parent preference."""

        return self.filter(preference_id=preference_id)


__all__ = (
    "PatientCommunicationPreferenceQuerySet",
    "PatientPreferenceQuerySet",
)

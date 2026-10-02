"""Selectors for Patient Communication Preferences."""

from __future__ import annotations

from apps.patient_management.preferences.models import PatientCommunicationPreference


class PatientCommunicationPreferenceSelector:
    """Read communication preferences through scoped selectors."""

    @staticmethod
    def list(*, preference_id, organization_id, tenant_id):
        """Return channel preferences inside the current tenant boundary."""

        return PatientCommunicationPreference.objects.select_related(
            "preference", "preference__patient"
        ).filter(
            preference_id=preference_id,
            preference__organization_id=organization_id,
            preference__organization__tenant_id=tenant_id,
        )

    @staticmethod
    def get(*, communication_preference_id, organization_id, tenant_id):
        """Return one scoped communication preference."""

        return PatientCommunicationPreference.objects.select_related(
            "preference", "preference__patient"
        ).get(
            id=communication_preference_id,
            preference__organization_id=organization_id,
            preference__organization__tenant_id=tenant_id,
        )


__all__ = ("PatientCommunicationPreferenceSelector",)

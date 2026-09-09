"""Selectors for organization-scoped Patient Preferences."""

from __future__ import annotations

from apps.patient_management.preferences.models import PatientPreference


class PatientPreferenceSelector:
    """Read Patient Preferences through scoped selectors."""

    @staticmethod
    def list(*, organization_id, tenant_id):
        """Return alive preferences inside one tenant and organization."""

        return PatientPreference.objects.select_related(
            "patient", "organization"
        ).filter(
            organization_id=organization_id,
            organization__tenant_id=tenant_id,
        )

    @staticmethod
    def get(*, preference_id, organization_id, tenant_id):
        """Return one scoped preference."""

        return PatientPreference.objects.select_related("patient", "organization").get(
            id=preference_id,
            organization_id=organization_id,
            organization__tenant_id=tenant_id,
        )


__all__ = ("PatientPreferenceSelector",)

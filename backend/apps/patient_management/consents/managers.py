"""
Managers and querysets for Patient Consents.
"""

from __future__ import annotations

from apps.core.models import (
    BaseManager,
    BaseQuerySet,
)


class ConsentQuerySet(
    BaseQuerySet["PatientConsent"],
):
    """
    Query helpers for Patient Consent records.
    """

    def for_patient(
        self,
        patient_id,
    ) -> ConsentQuerySet:
        """
        Return consent records belonging to a patient.
        """
        return self.filter(
            patient_id=patient_id,
        )

    def for_organization(
        self,
        organization_id,
    ) -> ConsentQuerySet:
        """
        Return consent records belonging to an organization.
        """
        return self.filter(
            organization_id=organization_id,
        )

    def active(
        self,
    ) -> ConsentQuerySet:
        """
        Return active, non-deleted consent records.
        """
        return self.filter(
            is_active=True,
            is_deleted=False,
        )

    def granted(
        self,
    ) -> ConsentQuerySet:
        """
        Return currently granted consent records.
        """
        return self.filter(
            status="granted",
            is_deleted=False,
        )


class ConsentManager(
    BaseManager.from_queryset(ConsentQuerySet),
):
    """
    Default manager for Patient Consent records.
    """


__all__ = (
    "ConsentManager",
    "ConsentQuerySet",
)

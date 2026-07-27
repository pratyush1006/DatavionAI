"""
Managers for the Patient Consents module.
"""

from __future__ import annotations

from django.db import models

__all__ = [
    "ConsentManager",
    "ConsentQuerySet",
]


class ConsentQuerySet(
    models.QuerySet,
):
    """
    QuerySet for Consent.
    """

    def active(self):
        return self.filter(
            is_active=True,
        )

    def granted(self):
        return self.filter(
            status="GRANTED",
        )

    def pending(self):
        return self.filter(
            status="PENDING",
        )

    def revoked(self):
        return self.filter(
            status="REVOKED",
        )

    def expired(self):
        return self.filter(
            status="EXPIRED",
        )

    def for_patient(
        self,
        patient_id,
    ):
        return self.filter(
            patient_id=patient_id,
        )

    def for_organization(
        self,
        organization_id,
    ):
        return self.filter(
            organization_id=organization_id,
        )

    def by_type(
        self,
        consent_type,
    ):
        return self.filter(
            consent_type=consent_type,
        )


class ConsentManager(
    models.Manager,
):
    """
    Default manager for Consent.
    """

    def get_queryset(self):
        return ConsentQuerySet(
            self.model,
            using=self._db,
        )

    def active(self):
        return self.get_queryset().active()

    def granted(self):
        return self.get_queryset().granted()

    def pending(self):
        return self.get_queryset().pending()

    def revoked(self):
        return self.get_queryset().revoked()

    def expired(self):
        return self.get_queryset().expired()

    def for_patient(
        self,
        patient_id,
    ):
        return self.get_queryset().for_patient(
            patient_id,
        )

    def for_organization(
        self,
        organization_id,
    ):
        return self.get_queryset().for_organization(
            organization_id,
        )

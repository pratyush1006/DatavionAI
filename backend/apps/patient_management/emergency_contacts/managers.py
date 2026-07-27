"""
Managers for the Emergency Contacts module.
"""

from __future__ import annotations

from django.db import models


class EmergencyContactQuerySet(
    models.QuerySet,
):
    """
    Emergency contact queryset.
    """

    def active(self):
        return self.filter(status="ACTIVE")

    def inactive(self):
        return self.filter(status="INACTIVE")

    def verified(self):
        return self.filter(is_verified=True)

    def unverified(self):
        return self.filter(is_verified=False)

    def primary(self):
        return self.filter(is_primary=True)

    def legal_guardians(self):
        return self.filter(is_legal_guardian=True)

    def medical_power_of_attorney(self):
        return self.filter(
            has_medical_power_of_attorney=True,
        )

    def for_patient(
        self,
        patient,
    ):
        return self.filter(patient=patient)

    def for_organization(
        self,
        organization,
    ):
        return self.filter(
            organization=organization,
        )

    def search(
        self,
        query: str,
    ):
        return self.filter(
            models.Q(first_name__icontains=query)
            | models.Q(last_name__icontains=query)
            | models.Q(mobile_number__icontains=query)
            | models.Q(email__icontains=query)
            | models.Q(
                emergency_contact_number__icontains=query,
            )
        )


class EmergencyContactManager(
    models.Manager,
):
    """
    Emergency contact manager.
    """

    def get_queryset(
        self,
    ):
        return EmergencyContactQuerySet(
            self.model,
            using=self._db,
        ).select_related(
            "organization",
            "patient",
            "verified_by",
        )

    def active(self):
        return self.get_queryset().active()

    def primary(self):
        return self.get_queryset().primary()

    def verified(self):
        return self.get_queryset().verified()

    def search(
        self,
        query: str,
    ):
        return self.get_queryset().search(query)

"""
Managers for the Patient Preferences module.
"""

from __future__ import annotations

from django.db import models

from apps.patient_management.preferences.constants import (
    PreferenceStatus,
)


class PatientPreferenceQuerySet(
    models.QuerySet,
):
    """
    QuerySet for PatientPreference.
    """

    def active(
        self,
    ):
        return self.filter(
            status=PreferenceStatus.ACTIVE,
        )

    def inactive(
        self,
    ):
        return self.filter(
            status=PreferenceStatus.INACTIVE,
        )

    def by_organization(
        self,
        organization_id: int,
    ):
        return self.filter(
            organization_id=organization_id,
        )

    def by_patient(
        self,
        patient_id: int,
    ):
        return self.filter(
            patient_id=patient_id,
        )


class PatientPreferenceManager(
    models.Manager.from_queryset(
        PatientPreferenceQuerySet,
    ),
):
    """
    Manager for PatientPreference.
    """


class PatientCommunicationPreferenceQuerySet(
    models.QuerySet,
):
    """
    QuerySet for PatientCommunicationPreference.
    """

    def enabled(
        self,
    ):
        return self.filter(
            enabled=True,
        )

    def disabled(
        self,
    ):
        return self.filter(
            enabled=False,
        )

    def by_organization(
        self,
        organization_id: int,
    ):
        return self.filter(
            organization_id=organization_id,
        )

    def by_patient(
        self,
        patient_id: int,
    ):
        return self.filter(
            patient_id=patient_id,
        )

    def by_channel(
        self,
        channel: str,
    ):
        return self.filter(
            channel=channel,
        )

    def ordered(
        self,
    ):
        return self.order_by(
            "priority",
        )


class PatientCommunicationPreferenceManager(
    models.Manager.from_queryset(
        PatientCommunicationPreferenceQuerySet,
    ),
):
    """
    Manager for PatientCommunicationPreference.
    """


__all__ = [
    "PatientCommunicationPreferenceManager",
    "PatientCommunicationPreferenceQuerySet",
    "PatientPreferenceManager",
    "PatientPreferenceQuerySet",
]

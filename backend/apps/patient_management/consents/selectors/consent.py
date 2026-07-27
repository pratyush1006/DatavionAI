"""
Selectors for the Patient Consents module.
"""

from __future__ import annotations

from django.db.models import QuerySet

from apps.patient_management.consents.models import Consent

__all__ = [
    "count_patient_consents",
    "get_active_consent",
    "get_consent_by_id",
    "list_consents",
    "list_organization_consents",
    "list_patient_consents",
]


def get_consent_by_id(
    consent_id,
) -> Consent:
    """
    Return a consent by ID.
    """

    return Consent.objects.get(
        id=consent_id,
    )


def list_consents() -> QuerySet[Consent]:
    """
    Return all consents.
    """

    return Consent.objects.all()


def list_patient_consents(
    patient_id,
) -> QuerySet[Consent]:
    """
    Return consents for a patient.
    """

    return Consent.objects.for_patient(
        patient_id,
    )


def list_organization_consents(
    organization_id,
) -> QuerySet[Consent]:
    """
    Return consents for an organization.
    """

    return Consent.objects.for_organization(
        organization_id,
    )


def get_active_consent(
    patient_id,
    consent_type,
) -> Consent | None:
    """
    Return the active consent for a patient and type.
    """

    return (
        Consent.objects.active().for_patient(patient_id).by_type(consent_type).first()
    )


def count_patient_consents(
    patient_id,
) -> int:
    """
    Count patient consents.
    """

    return Consent.objects.for_patient(
        patient_id,
    ).count()

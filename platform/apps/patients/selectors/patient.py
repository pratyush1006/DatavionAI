"""
Patient selectors.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.organizations.models import Organization
from apps.patients.models import Patient


def get_patients() -> QuerySet[Patient]:
    """
    Return all patients.
    """

    return Patient.objects.select_related(
        "organization",
    ).all()


def get_patient_by_id(
    *,
    patient_id: UUID,
) -> Patient:
    """
    Return a patient by ID.
    """

    return get_object_or_404(
        Patient.objects.select_related(
            "organization",
        ),
        id=patient_id,
    )


def get_organization_patients(
    *,
    organization: Organization,
) -> QuerySet[Patient]:
    """
    Return all patients belonging to an organization.
    """

    return Patient.objects.select_related(
        "organization",
    ).filter(
        organization=organization,
    )


__all__ = [
    "get_organization_patients",
    "get_patient_by_id",
    "get_patients",
]

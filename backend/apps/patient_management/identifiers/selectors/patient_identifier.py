"""
Selectors for Patient Identifiers.

Selectors are read-only query infrastructure. They enforce tenant and
organization boundaries but do not perform authorization; authorization
belongs to policies and RBAC.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from django.db.models import QuerySet

from apps.patient_management.identifiers.models import PatientIdentifier

if TYPE_CHECKING:
    from apps.platform.organizations.models import Organization


def get_identifier_by_id(
    *,
    identifier_id: UUID,
    organization: Organization,
) -> PatientIdentifier:
    """
    Return an identifier scoped to an organization.
    """
    return PatientIdentifier.objects.get(
        pk=identifier_id,
        organization_id=organization.pk,
    )


def get_identifier_by_value(
    *,
    organization: Organization,
    identifier_type: str,
    identifier_value: str,
) -> PatientIdentifier:
    """
    Return an identifier by type and value within an organization.

    Identifier values are intentionally never queried outside the
    organization boundary.
    """
    return PatientIdentifier.objects.get(
        organization_id=organization.pk,
        identifier_type=identifier_type,
        identifier_value=identifier_value,
    )


def get_patient_identifiers(
    *,
    organization: Organization,
    patient_id: UUID,
) -> QuerySet[PatientIdentifier]:
    """
    Return identifiers belonging to a patient within an organization.
    """
    return PatientIdentifier.objects.for_patient(
        organization_id=organization.pk,
        patient_id=patient_id,
    ).ordered()


def get_primary_identifier(
    *,
    organization: Organization,
    patient_id: UUID,
    identifier_type: str,
) -> PatientIdentifier | None:
    """
    Return the primary identifier for a patient and identifier type
    within an organization.
    """
    return (
        PatientIdentifier.objects.for_patient(
            organization_id=organization.pk,
            patient_id=patient_id,
        )
        .filter(
            identifier_type=identifier_type,
            is_primary=True,
        )
        .first()
    )


__all__ = (
    "get_identifier_by_id",
    "get_identifier_by_value",
    "get_patient_identifiers",
    "get_primary_identifier",
)

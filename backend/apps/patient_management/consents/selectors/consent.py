"""
Selectors for Patient Consents.

Selectors own read-side tenant and organization filtering.
"""

from __future__ import annotations

from uuid import UUID

from apps.common.exceptions import ResourceNotFoundException
from apps.patient_management.consents.models import (
    PatientConsent,
)


def get_consent(
    *,
    tenant_id: UUID,
    consent_id: UUID,
) -> PatientConsent:
    """
    Retrieve one consent within the requested tenant.
    """
    try:
        return PatientConsent.objects.select_related(
            "organization",
            "patient",
            "granted_by",
        ).get(
            pk=consent_id,
            organization__tenant_id=tenant_id,
        )
    except PatientConsent.DoesNotExist as exc:
        raise ResourceNotFoundException(
            "Patient consent was not found.",
        ) from exc


def list_patient_consents(
    *,
    tenant_id: UUID,
    patient_id: UUID,
):
    """
    Return non-deleted consents for one patient in the tenant.
    """
    return (
        PatientConsent.objects.select_related(
            "organization",
            "patient",
            "granted_by",
        )
        .filter(
            patient_id=patient_id,
            organization__tenant_id=tenant_id,
            is_deleted=False,
        )
        .order_by(
            "-created_at",
        )
    )


def list_organization_consents(
    *,
    tenant_id: UUID,
    organization_id: UUID,
):
    """
    Return non-deleted consents for one organization in the tenant.
    """
    return (
        PatientConsent.objects.select_related(
            "patient",
            "granted_by",
        )
        .filter(
            organization_id=organization_id,
            organization__tenant_id=tenant_id,
            is_deleted=False,
        )
        .order_by(
            "-created_at",
        )
    )


__all__ = (
    "get_consent",
    "list_organization_consents",
    "list_patient_consents",
)

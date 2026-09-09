"""Read-only selectors for Patient Medical History."""

from __future__ import annotations

from uuid import UUID

from apps.patient_management.medical_history.models import PatientMedicalHistory


def list_medical_history(
    *,
    tenant_id: UUID,
    patient_id=None,
    organization_id=None,
    include_inactive: bool = False,
):
    """List medical history."""
    queryset = PatientMedicalHistory.objects.with_relations().filter(
        organization__tenant_id=tenant_id
    )
    if patient_id:
        queryset = queryset.filter(patient_id=patient_id)
    if organization_id:
        queryset = queryset.filter(organization_id=organization_id)
    if not include_inactive:
        queryset = queryset.filter(is_active=True)
    return queryset


def get_medical_history(*, tenant_id: UUID, history_id: UUID):
    """Get medical history."""
    return PatientMedicalHistory.objects.with_relations().get(
        id=history_id, organization__tenant_id=tenant_id
    )


def get_deleted_medical_history(*, tenant_id: UUID, history_id: UUID):
    """Get deleted medical history."""
    return PatientMedicalHistory.deleted_objects.select_related(
        "organization", "patient", "verified_by"
    ).get(
        id=history_id,
        organization__tenant_id=tenant_id,
        is_deleted=True,
    )


__all__ = (
    "list_medical_history",
    "get_medical_history",
    "get_deleted_medical_history",
)

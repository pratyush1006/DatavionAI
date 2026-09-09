"""Read selectors for Patient Communication."""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet

from apps.patient_management.communication.models import PatientCommunication


def list_communications(
    *,
    tenant_id: UUID,
    patient_id: UUID | None = None,
    organization_id: UUID | None = None,
) -> QuerySet[PatientCommunication]:
    """Return alive communications inside the tenant boundary."""
    queryset = PatientCommunication.objects.filter(organization__tenant_id=tenant_id)
    if patient_id is not None:
        queryset = queryset.filter(patient_id=patient_id)
    if organization_id is not None:
        queryset = queryset.filter(organization_id=organization_id)
    return queryset.select_related("organization", "patient", "created_by")


def get_communication(
    *, tenant_id: UUID, communication_id: UUID, include_deleted: bool = False
) -> PatientCommunication:
    """Return one communication inside the tenant boundary."""
    manager = (
        PatientCommunication.all_objects
        if include_deleted
        else PatientCommunication.objects
    )
    return (
        manager.filter(
            pk=communication_id,
            organization__tenant_id=tenant_id,
        )
        .select_related("organization", "patient", "created_by")
        .get()
    )


__all__ = ("get_communication", "list_communications")

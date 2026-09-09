"""
Read-side selectors for the Master Patient Index.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet

from apps.patient_management.mpi.models import (
    MPIMatchCandidate,
    MPIRecord,
)


def list_mpi_records(
    *,
    tenant_id: UUID,
    organization_id: UUID,
) -> QuerySet[MPIRecord]:
    """Return tenant- and organization-scoped alive MPI records."""

    return (
        MPIRecord.objects.select_related(
            "organization",
            "patient",
            "merged_into",
        )
        .filter(
            organization_id=organization_id,
            organization__tenant_id=tenant_id,
        )
        .order_by("enterprise_identifier")
    )


def get_mpi_record(
    *,
    tenant_id: UUID,
    organization_id: UUID,
    record_id: UUID,
) -> MPIRecord:
    """Return one tenant- and organization-scoped alive MPI record."""

    return list_mpi_records(
        tenant_id=tenant_id,
        organization_id=organization_id,
    ).get(pk=record_id)


def list_mpi_candidates(
    *,
    tenant_id: UUID,
    organization_id: UUID,
) -> QuerySet[MPIMatchCandidate]:
    """Return tenant- and organization-scoped alive match candidates."""

    return (
        MPIMatchCandidate.objects.select_related(
            "organization",
            "left_record",
            "right_record",
        )
        .filter(
            organization_id=organization_id,
            organization__tenant_id=tenant_id,
        )
        .order_by("-score", "-created_at")
    )


__all__ = (
    "get_mpi_record",
    "list_mpi_candidates",
    "list_mpi_records",
)

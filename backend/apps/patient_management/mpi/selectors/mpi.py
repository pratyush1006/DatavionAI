"""
Selectors for the Master Patient Index.
"""

from __future__ import annotations

from django.db.models import QuerySet

from apps.patient_management.mpi.models import (
    MasterPatientIndex,
)


def get_mpi_by_id(
    mpi_record_id: int,
) -> MasterPatientIndex:
    """
    Return an MPI record by its primary key.
    """
    return MasterPatientIndex.objects.get(
        pk=mpi_record_id,
    )


def get_mpi_by_mpi_id(
    mpi_id: str,
) -> MasterPatientIndex:
    """
    Return an MPI record by its MPI identifier.
    """
    return MasterPatientIndex.objects.get(
        mpi_id=mpi_id,
    )


def get_patient_mpi(
    *,
    patient_id: int,
) -> MasterPatientIndex | None:
    """
    Return the MPI record for a patient.
    """
    return (
        MasterPatientIndex.objects.select_related(
            "organization",
            "patient",
            "merged_into",
        )
        .filter(
            patient_id=patient_id,
        )
        .first()
    )


def get_organization_mpi_records(
    *,
    organization_id: int,
) -> QuerySet[MasterPatientIndex]:
    """
    Return all MPI records for an organization.
    """
    return (
        MasterPatientIndex.objects.select_related(
            "organization",
            "patient",
            "merged_into",
        )
        .filter(
            organization_id=organization_id,
        )
        .order_by(
            "-created_at",
        )
    )


__all__ = [
    "get_mpi_by_id",
    "get_mpi_by_mpi_id",
    "get_organization_mpi_records",
    "get_patient_mpi",
]

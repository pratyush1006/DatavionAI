"""
Services for the Master Patient Index.
"""

from __future__ import annotations

from django.db import transaction

from apps.patient_management.mpi.models import (
    MasterPatientIndex,
)


@transaction.atomic
def create_mpi_record(
    **validated_data: object,
) -> MasterPatientIndex:
    """
    Create an MPI record.
    """
    return MasterPatientIndex.objects.create(
        **validated_data,
    )


@transaction.atomic
def update_mpi_record(
    *,
    mpi_record: MasterPatientIndex,
    **validated_data: object,
) -> MasterPatientIndex:
    """
    Update an MPI record.
    """
    for field, value in validated_data.items():
        setattr(
            mpi_record,
            field,
            value,
        )

    mpi_record.save()

    return mpi_record


@transaction.atomic
def verify_mpi_record(
    *,
    mpi_record: MasterPatientIndex,
) -> MasterPatientIndex:
    """
    Verify an MPI record.
    """
    mpi_record.verify()

    return mpi_record


@transaction.atomic
def merge_mpi_records(
    *,
    source: MasterPatientIndex,
    target: MasterPatientIndex,
) -> MasterPatientIndex:
    """
    Merge one MPI record into another.
    """
    source.merge(
        target=target,
    )

    return source


@transaction.atomic
def unmerge_mpi_record(
    *,
    mpi_record: MasterPatientIndex,
) -> MasterPatientIndex:
    """
    Restore a merged MPI record.
    """
    mpi_record.unmerge()

    return mpi_record


@transaction.atomic
def delete_mpi_record(
    *,
    mpi_record: MasterPatientIndex,
) -> None:
    """
    Delete an MPI record.
    """
    mpi_record.delete()


__all__ = [
    "create_mpi_record",
    "delete_mpi_record",
    "merge_mpi_records",
    "unmerge_mpi_record",
    "update_mpi_record",
    "verify_mpi_record",
]

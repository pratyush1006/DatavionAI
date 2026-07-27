"""
Background tasks for the Master Patient Index module.
"""

from __future__ import annotations


def verify_mpi_record(
    mpi_id: int,
) -> None:
    """
    Verify an MPI record.
    """
    _ = mpi_id


def synchronize_mpi_record(
    mpi_id: int,
) -> None:
    """
    Synchronize an MPI record with external systems.
    """
    _ = mpi_id


def detect_duplicate_patients(
    organization_id: int,
) -> None:
    """
    Detect potential duplicate patients.
    """
    _ = organization_id


__all__ = [
    "detect_duplicate_patients",
    "synchronize_mpi_record",
    "verify_mpi_record",
]

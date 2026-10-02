"""
Architecture tests for the Master Patient Index.
"""

from __future__ import annotations

from decimal import Decimal

from apps.patient_management.mpi.constants import (
    ALLOWED_RECORD_TRANSITIONS,
    MPI_MATCH_CLASS_NO_MATCH,
    MPIRecordStatus,
)
from apps.patient_management.mpi.matching import calculate_match
from apps.patient_management.mpi.models import MPIRecord
from apps.patient_management.patients.models import Patient


def test_mpi_uses_canonical_patient() -> None:
    """Verify MPIRecord points to the canonical Patient model."""

    patient_field = MPIRecord._meta.get_field("patient")
    assert patient_field.remote_field.model is Patient


def test_mpi_has_strict_terminal_states() -> None:
    """Verify merged and retired records have no outgoing lifecycle transitions."""

    assert ALLOWED_RECORD_TRANSITIONS[MPIRecordStatus.MERGED] == set()
    assert ALLOWED_RECORD_TRANSITIONS[MPIRecordStatus.RETIRED] == set()


def test_mpi_has_single_patient_owner() -> None:
    """Verify every canonical Patient can have only one MPI record."""

    patient_field = MPIRecord._meta.get_field("patient")
    assert patient_field.one_to_one is True


def test_mpi_match_score_is_absolute() -> None:
    """Verify missing attributes cannot inflate a partial match to 1.0000."""

    result = calculate_match(
        left={"first_name": "Ada"},
        right={"first_name": "Ada"},
    )

    assert result.score == Decimal("0.2000")
    assert result.classification == MPI_MATCH_CLASS_NO_MATCH


__all__ = ()

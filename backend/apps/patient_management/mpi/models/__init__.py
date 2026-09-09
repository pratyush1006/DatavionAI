"""
Master Patient Index model exports.
"""

from __future__ import annotations

from apps.patient_management.mpi.models.match import MPIMatchCandidate
from apps.patient_management.mpi.models.record import MPIRecord

__all__ = (
    "MPIMatchCandidate",
    "MPIRecord",
)

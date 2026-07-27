"""
Selectors for the Master Patient Index module.
"""

from .mpi import (
    get_mpi_by_id,
    get_mpi_by_mpi_id,
    get_organization_mpi_records,
    get_patient_mpi,
)

__all__ = [
    "get_mpi_by_id",
    "get_mpi_by_mpi_id",
    "get_organization_mpi_records",
    "get_patient_mpi",
]

"""
Prescription permissions.
"""

from .prescription import (
    CanCreatePrescription,
    CanDeletePrescription,
    CanUpdatePrescription,
    CanViewPrescription,
)

__all__ = [
    "CanCreatePrescription",
    "CanDeletePrescription",
    "CanUpdatePrescription",
    "CanViewPrescription",
]
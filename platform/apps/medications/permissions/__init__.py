"""
Medication permissions.
"""

from .medication import (
    CanCreateMedication,
    CanDeleteMedication,
    CanUpdateMedication,
    CanViewMedication,
)

__all__ = [
    "CanCreateMedication",
    "CanDeleteMedication",
    "CanUpdateMedication",
    "CanViewMedication",
]

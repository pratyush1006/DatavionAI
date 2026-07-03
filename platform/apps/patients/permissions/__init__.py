"""
Patient permission exports.
"""

from .patient import (
    CanCreatePatient,
    CanDeletePatient,
    CanUpdatePatient,
    CanViewPatient,
)

__all__ = [
    "CanCreatePatient",
    "CanDeletePatient",
    "CanUpdatePatient",
    "CanViewPatient",
]

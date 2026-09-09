"""
Patient Core RBAC permissions.
"""

from .patient import (
    CanActivatePatient,
    CanArchivePatient,
    CanCreatePatient,
    CanDeactivatePatient,
    CanDeletePatient,
    CanRestorePatient,
    CanUpdatePatient,
    CanViewPatient,
)

__all__ = (
    "CanViewPatient",
    "CanCreatePatient",
    "CanUpdatePatient",
    "CanDeletePatient",
    "CanActivatePatient",
    "CanDeactivatePatient",
    "CanArchivePatient",
    "CanRestorePatient",
)

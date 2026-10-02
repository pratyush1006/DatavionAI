"""
Patient Identifier API permission exports.
"""

from apps.patient_management.identifiers.permissions.identifier import (
    CanActivateIdentifier,
    CanCreateIdentifier,
    CanDeactivateIdentifier,
    CanDeleteIdentifier,
    CanRevokeIdentifier,
    CanSetPrimaryIdentifier,
    CanUpdateIdentifier,
    CanVerifyIdentifier,
    CanViewIdentifier,
    CanViewPatientIdentifier,
)

__all__ = (
    "CanActivateIdentifier",
    "CanCreateIdentifier",
    "CanDeactivateIdentifier",
    "CanDeleteIdentifier",
    "CanRevokeIdentifier",
    "CanSetPrimaryIdentifier",
    "CanUpdateIdentifier",
    "CanVerifyIdentifier",
    "CanViewIdentifier",
    "CanViewPatientIdentifier",
)

"""
Patient Address API permissions.
"""

from apps.patient_management.addresses.permissions.address import (
    CanActivateAddress,
    CanCreateAddress,
    CanDeactivateAddress,
    CanDeleteAddress,
    CanSetPrimaryAddress,
    CanUpdateAddress,
    CanVerifyAddress,
    CanViewAddress,
)

__all__ = (
    "CanActivateAddress",
    "CanCreateAddress",
    "CanDeactivateAddress",
    "CanDeleteAddress",
    "CanSetPrimaryAddress",
    "CanUpdateAddress",
    "CanVerifyAddress",
    "CanViewAddress",
)

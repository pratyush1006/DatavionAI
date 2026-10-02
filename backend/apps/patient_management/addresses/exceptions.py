"""Patient Address domain exceptions."""

from __future__ import annotations


class AddressError(Exception):
    """Base Address exception."""


class AddressScopeError(AddressError):
    """Tenant, organization, or patient scope mismatch."""


class AddressGeographyError(AddressError):
    """Platform Geography integration failure."""

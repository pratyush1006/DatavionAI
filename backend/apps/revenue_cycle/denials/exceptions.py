"""Denial domain exceptions."""

from __future__ import annotations


class DenialDomainError(Exception):
    """Base denial domain error."""


class InvalidDenialTransition(DenialDomainError):
    """Raised for an invalid lifecycle transition."""


__all__ = ("DenialDomainError", "InvalidDenialTransition")

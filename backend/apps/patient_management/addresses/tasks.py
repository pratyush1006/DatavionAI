"""
Background tasks for the Addresses module.
"""

from __future__ import annotations


def verify_address(
    address_id: int,
) -> None:
    """
    Verify an address.
    """
    _ = address_id


def synchronize_address(
    address_id: int,
) -> None:
    """
    Synchronize an address with external systems.
    """
    _ = address_id


__all__ = [
    "synchronize_address",
    "verify_address",
]

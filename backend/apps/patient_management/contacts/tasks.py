"""
Background tasks for the Contacts module.
"""

from __future__ import annotations


def verify_contact(
    contact_id: int,
) -> None:
    """
    Verify a patient contact.
    """
    _ = contact_id


def synchronize_contact(
    contact_id: int,
) -> None:
    """
    Synchronize a patient contact with external systems.
    """
    _ = contact_id


__all__ = [
    "synchronize_contact",
    "verify_contact",
]

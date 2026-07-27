# apps/patient_management/identifiers/tasks.py

"""
Background tasks for the Identifiers module.
"""

from __future__ import annotations


def verify_identifier(
    identifier_id: int,
) -> None:
    """
    Placeholder for asynchronous identifier verification.
    """
    _ = identifier_id


def sync_identifier(
    identifier_id: int,
) -> None:
    """
    Placeholder for external identifier synchronization.
    """
    _ = identifier_id


__all__ = [
    "sync_identifier",
    "verify_identifier",
]

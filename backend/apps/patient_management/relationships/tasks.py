"""
Background tasks for the Patient Relationships module.
"""

from __future__ import annotations


def verify_relationship(
    relationship_id: int,
) -> None:
    """
    Verify a patient relationship.
    """
    _ = relationship_id


def synchronize_relationship(
    relationship_id: int,
) -> None:
    """
    Synchronize a relationship with external systems.
    """
    _ = relationship_id


def notify_relationship_change(
    relationship_id: int,
) -> None:
    """
    Notify downstream systems of relationship changes.
    """
    _ = relationship_id


__all__ = [
    "notify_relationship_change",
    "synchronize_relationship",
    "verify_relationship",
]

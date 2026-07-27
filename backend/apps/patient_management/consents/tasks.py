"""
Background tasks for the Patient Consents module.
"""

from __future__ import annotations


def expire_consents() -> None:
    """
    Expire patient consents.
    """
    return


def notify_consent_expiration(
    consent_id: int,
) -> None:
    """
    Notify patient about consent expiration.
    """
    _ = consent_id


def synchronize_consents(
    consent_id: int,
) -> None:
    """
    Synchronize consent with external systems.
    """
    _ = consent_id


__all__ = [
    "expire_consents",
    "notify_consent_expiration",
    "synchronize_consents",
]

"""
Patient Consent service exports.
"""

from __future__ import annotations

from .consent import (
    create_consent,
    delete_consent,
    grant_consent,
    restore_consent,
    revoke_consent,
    update_consent,
)

__all__ = (
    "create_consent",
    "delete_consent",
    "grant_consent",
    "restore_consent",
    "revoke_consent",
    "update_consent",
)

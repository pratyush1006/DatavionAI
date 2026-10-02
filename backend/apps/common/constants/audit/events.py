"""
DatavionAI Audit Event Constants.

Centralized audit event definitions used throughout the DatavionAI
platform.

This module defines generic audit event lifecycle semantics shared
across all applications.

Design Principles
-----------------
- Immutable constants
- Framework agnostic
- No business logic
- Domain agnostic
- Safe to import everywhere
"""

from __future__ import annotations

from enum import StrEnum
from typing import Final

###############################################################################
# Audit Event Types
###############################################################################


class AuditEvent(StrEnum):
    """
    Generic audit event lifecycle.
    """

    REQUESTED = "requested"

    RECEIVED = "received"

    VALIDATED = "validated"

    ACCEPTED = "accepted"

    REJECTED = "rejected"

    PROCESSING = "processing"

    COMPLETED = "completed"

    FAILED = "failed"

    CANCELLED = "cancelled"

    EXPIRED = "expired"

    RETRIED = "retried"

    ROLLED_BACK = "rolled_back"


SUPPORTED_AUDIT_EVENTS: Final[tuple[str, ...]] = tuple(
    event.value for event in AuditEvent
)

###############################################################################
# Event Groups
###############################################################################

REQUEST_EVENTS: Final[frozenset[str]] = frozenset(
    {
        AuditEvent.REQUESTED.value,
        AuditEvent.RECEIVED.value,
        AuditEvent.VALIDATED.value,
        AuditEvent.ACCEPTED.value,
    }
)

PROCESSING_EVENTS: Final[frozenset[str]] = frozenset(
    {
        AuditEvent.PROCESSING.value,
        AuditEvent.RETRIED.value,
    }
)

SUCCESS_EVENTS: Final[frozenset[str]] = frozenset(
    {
        AuditEvent.COMPLETED.value,
    }
)

FAILURE_EVENTS: Final[frozenset[str]] = frozenset(
    {
        AuditEvent.REJECTED.value,
        AuditEvent.FAILED.value,
        AuditEvent.CANCELLED.value,
        AuditEvent.EXPIRED.value,
        AuditEvent.ROLLED_BACK.value,
    }
)

TERMINAL_EVENTS: Final[frozenset[str]] = frozenset(
    {
        AuditEvent.COMPLETED.value,
        AuditEvent.REJECTED.value,
        AuditEvent.FAILED.value,
        AuditEvent.CANCELLED.value,
        AuditEvent.EXPIRED.value,
        AuditEvent.ROLLED_BACK.value,
    }
)

###############################################################################
# Public Exports
###############################################################################

__all__ = tuple(name for name, value in globals().items() if name.isupper()) + (
    "AuditEvent",
)

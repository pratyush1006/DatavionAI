"""Constants for the Revenue Cycle Charge Capture bounded context."""

from __future__ import annotations

from enum import StrEnum

__all__ = ("ChargeStatus",)


class ChargeStatus(StrEnum):
    """Lifecycle states for a captured charge."""

    DRAFT = "draft"
    READY = "ready"
    SUBMITTED = "submitted"
    VOIDED = "voided"

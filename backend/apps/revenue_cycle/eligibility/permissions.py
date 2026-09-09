"""Revenue Cycle Eligibility RBAC permission codes."""

from __future__ import annotations

from enum import StrEnum


class EligibilityPermission(StrEnum):
    """Exact platform RBAC codes."""

    VIEW = "revenue_cycle.eligibility.view"
    CREATE = "revenue_cycle.eligibility.create"
    UPDATE = "revenue_cycle.eligibility.update"
    DELETE = "revenue_cycle.eligibility.delete"
    RESTORE = "revenue_cycle.eligibility.restore"
    LIFECYCLE = "revenue_cycle.eligibility.lifecycle"


__all__ = ("EligibilityPermission",)

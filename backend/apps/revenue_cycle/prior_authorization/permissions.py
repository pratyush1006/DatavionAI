"""Revenue Cycle Prior Authorization RBAC permission codes."""

from __future__ import annotations

from enum import StrEnum


class PriorAuthorizationPermission(StrEnum):
    """Exact platform RBAC permission codes."""

    VIEW = "revenue_cycle.prior_authorization.view"
    CREATE = "revenue_cycle.prior_authorization.create"
    UPDATE = "revenue_cycle.prior_authorization.update"
    DELETE = "revenue_cycle.prior_authorization.delete"
    RESTORE = "revenue_cycle.prior_authorization.restore"
    LIFECYCLE = "revenue_cycle.prior_authorization.lifecycle"


__all__ = ("PriorAuthorizationPermission",)

"""RBAC permission identifiers for Accounts Receivable."""

from __future__ import annotations

from apps.platform.rbac.permissions.base import RBACPermissionBase


class ARPermission(RBACPermissionBase):
    """Define canonical Revenue Cycle AR permissions."""

    LIST = "revenue_cycle.accounts_receivable.list"
    CREATE = "revenue_cycle.accounts_receivable.create"
    UPDATE = "revenue_cycle.accounts_receivable.update"
    POST = "revenue_cycle.accounts_receivable.post"
    REVERSE = "revenue_cycle.accounts_receivable.reverse"
    WRITE_OFF = "revenue_cycle.accounts_receivable.write_off"
    HOLD = "revenue_cycle.accounts_receivable.hold"


__all__ = ("ARPermission",)

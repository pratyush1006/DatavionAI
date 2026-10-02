"""RBAC permissions for Revenue Analytics."""

from __future__ import annotations

from apps.platform.rbac.permissions.base import RBACPermissionBase


class RevenueAnalyticsPermission(RBACPermissionBase):
    """Define canonical Revenue Analytics permissions."""

    LIST = "revenue_cycle.revenue_analytics.list"
    VIEW = "revenue_cycle.revenue_analytics.view"
    GENERATE = "revenue_cycle.revenue_analytics.generate"


__all__ = ("RevenueAnalyticsPermission",)

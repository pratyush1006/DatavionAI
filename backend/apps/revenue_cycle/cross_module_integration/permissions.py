"""RBAC permissions for Revenue Cycle cross-module integration."""

from __future__ import annotations

from apps.platform.rbac.permissions.base import RBACPermissionBase


class CrossModuleIntegrationPermission(RBACPermissionBase):
    """Define canonical integration permissions."""

    LIST = "revenue_cycle.cross_module_integration.list"
    VIEW = "revenue_cycle.cross_module_integration.view"
    PROCESS = "revenue_cycle.cross_module_integration.process"


__all__ = ("CrossModuleIntegrationPermission",)

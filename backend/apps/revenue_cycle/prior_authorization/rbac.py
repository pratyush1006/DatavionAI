"""DRF RBAC adapters for Prior Authorization."""

from __future__ import annotations

from apps.platform.rbac.permissions.base import RBACPermissionBase
from apps.revenue_cycle.prior_authorization.permissions import (
    PriorAuthorizationPermission,
)


class CanViewPriorAuthorization(RBACPermissionBase):
    """Require Prior Authorization view permission."""

    permission_code = PriorAuthorizationPermission.VIEW
    message = "You do not have permission to view prior authorization records."


class CanCreatePriorAuthorization(RBACPermissionBase):
    """Require Prior Authorization creation permission."""

    permission_code = PriorAuthorizationPermission.CREATE
    message = "You do not have permission to create prior authorization records."


class CanUpdatePriorAuthorization(RBACPermissionBase):
    """Require Prior Authorization update permission."""

    permission_code = PriorAuthorizationPermission.UPDATE
    message = "You do not have permission to update prior authorization records."


class CanDeletePriorAuthorization(RBACPermissionBase):
    """Require Prior Authorization deletion permission."""

    permission_code = PriorAuthorizationPermission.DELETE
    message = "You do not have permission to delete prior authorization records."


class CanRestorePriorAuthorization(RBACPermissionBase):
    """Require Prior Authorization restoration permission."""

    permission_code = PriorAuthorizationPermission.RESTORE
    message = "You do not have permission to restore prior authorization records."


class CanTransitionPriorAuthorization(RBACPermissionBase):
    """Require Prior Authorization lifecycle permission."""

    permission_code = PriorAuthorizationPermission.LIFECYCLE
    message = "You do not have permission to change prior authorization lifecycle."


__all__ = (
    "CanCreatePriorAuthorization",
    "CanDeletePriorAuthorization",
    "CanRestorePriorAuthorization",
    "CanTransitionPriorAuthorization",
    "CanUpdatePriorAuthorization",
    "CanViewPriorAuthorization",
)

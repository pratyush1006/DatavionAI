"""Billing adapter for the canonical platform RBAC engine."""

from __future__ import annotations

from typing import Any

from apps.platform.rbac.engines import user_has_permission

from .exceptions import BillingPermissionError


def require_billing_permission(
    *, user: Any, permission: str, organization: Any
) -> None:
    """Require an exact Billing permission through platform RBAC."""
    if not user_has_permission(
        user=user, permission=permission, organization=organization
    ):
        raise BillingPermissionError(f"Missing Billing permission: {permission}")


__all__ = ["require_billing_permission"]

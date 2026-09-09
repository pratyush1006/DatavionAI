"""Canonical Revenue Cycle RBAC compatibility adapter."""

from __future__ import annotations

from typing import Any

from apps.platform.rbac.resolvers import resolve_permissions


def has_permission(*, user: Any, permission: str, organization: Any) -> bool:
    """Evaluate a Revenue Cycle permission through platform RBAC."""
    if user is None or not getattr(user, "is_authenticated", True):
        return False
    if organization is None:
        return False

    permissions = resolve_permissions(
        user=user,
        organization=organization,
    )
    return "*" in permissions or permission in permissions


__all__ = ("has_permission",)

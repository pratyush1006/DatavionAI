from __future__ import annotations

"""Canonical platform RBAC integration for Revenue Cycle Claim Scrubbing."""

from typing import Any

from apps.platform.rbac.resolvers import resolve_permissions


def has_permission(
    *,
    user: Any,
    permission: str,
    organization: Any,
) -> bool:
    """Evaluate a permission through the canonical platform resolver."""

    if user is None or organization is None:
        return False

    if not getattr(user, "is_authenticated", True):
        return False

    permissions = resolve_permissions(
        user=user,
        organization=organization,
    )

    return "*" in permissions or permission in permissions


__all__ = ("has_permission",)

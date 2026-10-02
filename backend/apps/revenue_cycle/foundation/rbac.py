"""Canonical Revenue Cycle RBAC adapter."""

from __future__ import annotations

from typing import Any

from apps.platform.rbac.resolvers import resolve_permissions


def has_permission(
    *,
    actor: Any,
    permission: str,
    organization: Any,
) -> bool:
    """Evaluate a Revenue Cycle permission through the platform RBAC resolver."""

    if actor is None or organization is None:
        return False

    if not getattr(actor, "is_authenticated", True):
        return False

    permissions = resolve_permissions(
        user=actor,
        organization=organization,
    )

    return "*" in permissions or permission in permissions


__all__ = ("has_permission",)

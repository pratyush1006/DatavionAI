from __future__ import annotations

"""Canonical platform RBAC integration for Coding."""

from typing import Any

from apps.platform.rbac.resolvers import resolve_permissions


def has_permission(*, user: Any, permission: str, organization: Any) -> bool:
    """Evaluate a Coding permission through the canonical platform resolver."""

    permissions = resolve_permissions(
        user=user,
        organization=organization,
    )
    return permission in permissions


__all__ = ("has_permission",)

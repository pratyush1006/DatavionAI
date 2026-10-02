"""
Canonical RBAC adapter for clinical transcription.
"""

from __future__ import annotations

from apps.platform.rbac.resolvers import resolve_permissions


def has_permission(*, user, organization, permission: str) -> bool:
    if user is None or not getattr(user, "is_authenticated", False):
        return False
    if organization is None:
        return False
    return permission in resolve_permissions(
        user=user,
        organization=organization,
    )

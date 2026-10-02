"""Canonical platform RBAC adapter for claim submission."""

from __future__ import annotations


def _has_permission(*, user, permission, organization):
    """Check a permission through the canonical platform RBAC engine."""

    return _has_permission(user=user, permission=permission, organization=organization)


__all__ = ("has_permission",)

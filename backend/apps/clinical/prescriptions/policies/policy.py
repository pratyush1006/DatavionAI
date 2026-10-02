"""Fail-closed RBAC policy for Prescription."""

from __future__ import annotations

from apps.platform.rbac.resolvers import resolve_permissions


class PrescriptionPolicy:
    permission_prefix = "prescription"

    @classmethod
    def allows(cls, *, user, organization, action: str) -> bool:
        if user is None or not getattr(user, "is_authenticated", False):
            return False
        if organization is None:
            return False
        return f"{cls.permission_prefix}.{action}" in resolve_permissions(
            user=user,
            organization=organization,
        )


__all__ = ("PrescriptionPolicy",)

"""Authorization policy boundary for Vitals."""

from __future__ import annotations

from typing import Any

from apps.platform.rbac.resolvers import resolve_permissions


class VitalPolicy:
    @staticmethod
    def allowed(*, user: Any, permission: str, organization: Any) -> bool:
        return permission in resolve_permissions(user=user, organization=organization)

    @classmethod
    def can_view(cls, *, user: Any, organization: Any) -> bool:
        return cls.allowed(
            user=user, permission="vitals.view", organization=organization
        )

    @classmethod
    def can_create(cls, *, user: Any, organization: Any) -> bool:
        return cls.allowed(
            user=user, permission="vitals.create", organization=organization
        )

    @classmethod
    def can_update(cls, *, user: Any, organization: Any) -> bool:
        return cls.allowed(
            user=user, permission="vitals.update", organization=organization
        )

    @classmethod
    def can_delete(cls, *, user: Any, organization: Any) -> bool:
        return cls.allowed(
            user=user, permission="vitals.delete", organization=organization
        )


__all__ = ("VitalPolicy",)

"""Authorization policy boundary for Clinical Allergies."""

from __future__ import annotations

from typing import Any

from apps.platform.rbac.resolvers import resolve_permissions


class AllergyPolicy:
    @staticmethod
    def allowed(*, user: Any, permission: str, organization: Any) -> bool:
        return permission in resolve_permissions(
            user=user,
            organization=organization,
        )

    @classmethod
    def can_view(cls, *, user: Any, organization: Any) -> bool:
        return cls.allowed(
            user=user,
            permission="allergies.view",
            organization=organization,
        )

    @classmethod
    def can_create(cls, *, user: Any, organization: Any) -> bool:
        return cls.allowed(
            user=user,
            permission="allergies.create",
            organization=organization,
        )

    @classmethod
    def can_update(cls, *, user: Any, organization: Any) -> bool:
        return cls.allowed(
            user=user,
            permission="allergies.update",
            organization=organization,
        )

    @classmethod
    def can_delete(cls, *, user: Any, organization: Any) -> bool:
        return cls.allowed(
            user=user,
            permission="allergies.delete",
            organization=organization,
        )


__all__ = ("AllergyPolicy",)

"""
Provider domain policies.

Encapsulates provider authorization
rules used by workflows.

Uses DatavionOS RBAC engine.
"""

from __future__ import annotations

from apps.platform.rbac.engines import (
    user_has_permission,
)


class ProviderPolicy:
    """
    Provider workflow authorization policy.

    Used by:

    - Provider creation workflow
    - Provider verification workflow
    - Provider activation workflow
    - Provider assignment workflow
    """

    def can_create(
        self,
        *,
        actor,
        organization,
    ) -> bool:
        return user_has_permission(
            user=actor,
            permission="providers.create",
            organization=organization,
        )

    def can_update(
        self,
        *,
        actor,
        organization,
    ) -> bool:
        return user_has_permission(
            user=actor,
            permission="providers.update",
            organization=organization,
        )

    def can_delete(
        self,
        *,
        actor,
        organization,
    ) -> bool:
        return user_has_permission(
            user=actor,
            permission="providers.delete",
            organization=organization,
        )

    def can_verify(
        self,
        *,
        actor,
        organization,
    ) -> bool:
        return user_has_permission(
            user=actor,
            permission="providers.verify",
            organization=organization,
        )

    def can_activate(
        self,
        *,
        actor,
        organization,
    ) -> bool:
        return user_has_permission(
            user=actor,
            permission="providers.activate",
            organization=organization,
        )

    def can_deactivate(
        self,
        *,
        actor,
        organization,
    ) -> bool:
        return user_has_permission(
            user=actor,
            permission="providers.deactivate",
            organization=organization,
        )

    def can_assign(
        self,
        *,
        actor,
        organization,
    ) -> bool:
        return user_has_permission(
            user=actor,
            permission="providers.assign",
            organization=organization,
        )


__all__ = [
    "ProviderPolicy",
]

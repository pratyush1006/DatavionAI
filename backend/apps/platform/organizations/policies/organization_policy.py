"""
Organization authorization policies.

Authorization rules for the Organizations bounded context.

Delegates permission evaluation to the RBAC engine.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization
from apps.platform.rbac.engines.permission import (
    user_has_permission,
)


@dataclass(
    frozen=True,
    slots=True,
)
class OrganizationPolicy:
    """
    Organization authorization policy.

    Responsibilities:

    - Decide whether an actor can perform an action.
    - Delegate permission resolution to RBAC.
    - Remain free of persistence logic.
    """

    def _check(
        self,
        *,
        actor: User,
        organization: Organization,
        permission: str,
    ) -> bool:
        """
        Central permission resolver.
        """

        return user_has_permission(
            user=actor,
            permission=permission,
            organization=organization,
        )

    def can_create(
        self,
        *,
        actor: User,
        organization: Organization | None = None,
    ) -> bool:
        return user_has_permission(
            user=actor,
            permission="organizations.create",
            organization=organization,
        )

    def can_update(
        self,
        *,
        actor: User,
        organization: Organization,
    ) -> bool:
        return self._check(
            actor=actor,
            organization=organization,
            permission="organizations.update",
        )

    def can_delete(
        self,
        *,
        actor: User,
        organization: Organization,
    ) -> bool:
        return self._check(
            actor=actor,
            organization=organization,
            permission="organizations.delete",
        )

    def can_activate(
        self,
        *,
        actor: User,
        organization: Organization,
    ) -> bool:
        return self._check(
            actor=actor,
            organization=organization,
            permission="organizations.activate",
        )

    def can_deactivate(
        self,
        *,
        actor: User,
        organization: Organization,
    ) -> bool:
        return self._check(
            actor=actor,
            organization=organization,
            permission="organizations.deactivate",
        )

    def can_suspend(
        self,
        *,
        actor: User,
        organization: Organization,
    ) -> bool:
        return self._check(
            actor=actor,
            organization=organization,
            permission="organizations.suspend",
        )

    def can_restore(
        self,
        *,
        actor: User,
        organization: Organization,
    ) -> bool:
        return self._check(
            actor=actor,
            organization=organization,
            permission="organizations.restore",
        )

    def can_verify(
        self,
        *,
        actor: User,
        organization: Organization,
    ) -> bool:
        return self._check(
            actor=actor,
            organization=organization,
            permission="organizations.verify",
        )

    def can_manage_branding(
        self,
        *,
        actor: User,
        organization: Organization,
    ) -> bool:
        return self._check(
            actor=actor,
            organization=organization,
            permission="organizations.update",
        )

    def can_manage_settings(
        self,
        *,
        actor: User,
        organization: Organization,
    ) -> bool:
        return self._check(
            actor=actor,
            organization=organization,
            permission="organizations.update",
        )

    def can_manage_features(
        self,
        *,
        actor: User,
        organization: Organization,
    ) -> bool:
        return self._check(
            actor=actor,
            organization=organization,
            permission="organizations.update",
        )

    def can_manage_modules(
        self,
        *,
        actor: User,
        organization: Organization,
    ) -> bool:
        return self._check(
            actor=actor,
            organization=organization,
            permission="organizations.update",
        )


__all__: tuple[str, ...] = ("OrganizationPolicy",)

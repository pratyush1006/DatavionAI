"""
Authorization policy for Patient Addresses.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.patient_management.addresses.models import Address
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization
from apps.platform.rbac.engines.permission import (
    user_has_permission,
)


@dataclass(
    frozen=True,
    slots=True,
)
class AddressPolicy:
    """
    Patient Address authorization policy.
    """

    @staticmethod
    def _check(
        *,
        actor: User,
        organization: Organization,
        permission: str,
    ) -> bool:
        return user_has_permission(
            user=actor,
            permission=permission,
            organization=organization,
        )

    def can_view(
        self,
        *,
        actor: User,
        address: Address,
    ) -> bool:
        return self._check(
            actor=actor,
            organization=address.organization,
            permission="addresses.view",
        )

    def can_create(
        self,
        *,
        actor: User,
        organization: Organization,
    ) -> bool:
        return self._check(
            actor=actor,
            organization=organization,
            permission="addresses.create",
        )

    def can_update(
        self,
        *,
        actor: User,
        address: Address,
    ) -> bool:
        return self._check(
            actor=actor,
            organization=address.organization,
            permission="addresses.update",
        )

    def can_delete(
        self,
        *,
        actor: User,
        address: Address,
    ) -> bool:
        return self._check(
            actor=actor,
            organization=address.organization,
            permission="addresses.delete",
        )

    def can_verify(
        self,
        *,
        actor: User,
        address: Address,
    ) -> bool:
        return self._check(
            actor=actor,
            organization=address.organization,
            permission="addresses.verify",
        )

    def can_activate(
        self,
        *,
        actor: User,
        address: Address,
    ) -> bool:
        return self._check(
            actor=actor,
            organization=address.organization,
            permission="addresses.activate",
        )

    def can_deactivate(
        self,
        *,
        actor: User,
        address: Address,
    ) -> bool:
        return self._check(
            actor=actor,
            organization=address.organization,
            permission="addresses.deactivate",
        )

    def can_set_primary(
        self,
        *,
        actor: User,
        address: Address,
    ) -> bool:
        return self._check(
            actor=actor,
            organization=address.organization,
            permission="addresses.set_primary",
        )


__all__ = ("AddressPolicy",)

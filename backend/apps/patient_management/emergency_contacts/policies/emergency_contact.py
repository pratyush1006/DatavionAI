"""
Authorization policy for patient emergency contacts.

Authorization belongs to the policy layer.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.patient_management.emergency_contacts.models import (
    EmergencyContact,
)
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization
from apps.platform.rbac.engines.permission import (
    user_has_permission,
)


@dataclass(frozen=True, slots=True)
class EmergencyContactPolicy:
    """
    Emergency Contact authorization policy.

    Policies are intentionally thin and delegate RBAC evaluation to the
    platform authorization engine.
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
        emergency_contact: EmergencyContact,
    ) -> bool:
        return self._check(
            actor=actor,
            organization=emergency_contact.organization,
            permission="emergency_contacts.view",
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
            permission="emergency_contacts.create",
        )

    def can_update(
        self,
        *,
        actor: User,
        emergency_contact: EmergencyContact,
    ) -> bool:
        return self._check(
            actor=actor,
            organization=emergency_contact.organization,
            permission="emergency_contacts.update",
        )

    def can_delete(
        self,
        *,
        actor: User,
        emergency_contact: EmergencyContact,
    ) -> bool:
        return self._check(
            actor=actor,
            organization=emergency_contact.organization,
            permission="emergency_contacts.delete",
        )

    def can_verify(
        self,
        *,
        actor: User,
        emergency_contact: EmergencyContact,
    ) -> bool:
        return self._check(
            actor=actor,
            organization=emergency_contact.organization,
            permission="emergency_contacts.verify",
        )

    def can_activate(
        self,
        *,
        actor: User,
        emergency_contact: EmergencyContact,
    ) -> bool:
        return self._check(
            actor=actor,
            organization=emergency_contact.organization,
            permission="emergency_contacts.activate",
        )

    def can_deactivate(
        self,
        *,
        actor: User,
        emergency_contact: EmergencyContact,
    ) -> bool:
        return self._check(
            actor=actor,
            organization=emergency_contact.organization,
            permission="emergency_contacts.deactivate",
        )

    def can_block(
        self,
        *,
        actor: User,
        emergency_contact: EmergencyContact,
    ) -> bool:
        return self._check(
            actor=actor,
            organization=emergency_contact.organization,
            permission="emergency_contacts.block",
        )

    def can_set_primary(
        self,
        *,
        actor: User,
        emergency_contact: EmergencyContact,
    ) -> bool:
        return self._check(
            actor=actor,
            organization=emergency_contact.organization,
            permission="emergency_contacts.set_primary",
        )


__all__ = ("EmergencyContactPolicy",)

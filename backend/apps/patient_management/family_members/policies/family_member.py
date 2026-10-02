"""
Patient Family Member authorization policy.

Delegates authorization decisions to the centralized DatavionOS
RBAC permission engine.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.patient_management.family_members.models import FamilyMember
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization
from apps.platform.rbac.engines.permission import user_has_permission


@dataclass(frozen=True, slots=True)
class FamilyMemberPolicy:
    """Authorization policy for Patient Family Members."""

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
        family_member: FamilyMember,
    ) -> bool:
        return self._check(
            actor=actor,
            organization=family_member.organization,
            permission="family_members.view",
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
            permission="family_members.create",
        )

    def can_update(
        self,
        *,
        actor: User,
        family_member: FamilyMember,
    ) -> bool:
        return self._check(
            actor=actor,
            organization=family_member.organization,
            permission="family_members.update",
        )

    def can_delete(
        self,
        *,
        actor: User,
        family_member: FamilyMember,
    ) -> bool:
        return self._check(
            actor=actor,
            organization=family_member.organization,
            permission="family_members.delete",
        )

    def can_restore(
        self,
        *,
        actor: User,
        family_member: FamilyMember,
    ) -> bool:
        return self._check(
            actor=actor,
            organization=family_member.organization,
            permission="family_members.restore",
        )

    def can_view_sensitive(
        self,
        *,
        actor: User,
        family_member: FamilyMember,
    ) -> bool:
        return self._check(
            actor=actor,
            organization=family_member.organization,
            permission="family_members.view_sensitive",
        )

    def can_manage_next_of_kin(
        self,
        *,
        actor: User,
        family_member: FamilyMember,
    ) -> bool:
        return self._check(
            actor=actor,
            organization=family_member.organization,
            permission="family_members.manage_next_of_kin",
        )

    def can_manage_emergency_contact(
        self,
        *,
        actor: User,
        family_member: FamilyMember,
    ) -> bool:
        return self._check(
            actor=actor,
            organization=family_member.organization,
            permission="family_members.manage_emergency_contact",
        )

    def can_activate(
        self,
        *,
        actor: User,
        family_member: FamilyMember,
    ) -> bool:
        return self.can_update(
            actor=actor,
            family_member=family_member,
        )

    def can_deactivate(
        self,
        *,
        actor: User,
        family_member: FamilyMember,
    ) -> bool:
        return self.can_update(
            actor=actor,
            family_member=family_member,
        )

    def can_restore_deleted(
        self,
        *,
        actor: User,
        family_member: FamilyMember,
    ) -> bool:
        return self.can_restore(
            actor=actor,
            family_member=family_member,
        )

    def can_export(
        self,
        *,
        actor: User,
        organization: Organization,
    ) -> bool:
        return self._check(
            actor=actor,
            organization=organization,
            permission="family_members.export",
        )

    def can_import(
        self,
        *,
        actor: User,
        organization: Organization,
    ) -> bool:
        return self._check(
            actor=actor,
            organization=organization,
            permission="family_members.import",
        )


__all__ = ("FamilyMemberPolicy",)

"""
Authorization policy for Patient Contacts.

Policies are domain authorization adapters over the platform RBAC engine.
They do not perform persistence or workflow orchestration.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.patient_management.contacts.models import Contact
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization
from apps.platform.rbac.engines.permission import user_has_permission


@dataclass(
    frozen=True,
    slots=True,
)
class ContactPolicy:
    """
    Authorization policy for Patient Contact operations.
    """

    def _check(
        self,
        *,
        actor: User,
        organization: Organization,
        permission: str,
    ) -> bool:
        """
        Resolve a permission through the platform RBAC engine.
        """
        return user_has_permission(
            user=actor,
            permission=permission,
            organization=organization,
        )

    def can_view(
        self,
        *,
        actor: User,
        contact: Contact,
    ) -> bool:
        """
        Check whether the actor can view a contact.
        """
        return self._check(
            actor=actor,
            organization=contact.organization,
            permission="contacts.view",
        )

    def can_create(
        self,
        *,
        actor: User,
        organization: Organization,
    ) -> bool:
        """
        Check whether the actor can create a contact.
        """
        return self._check(
            actor=actor,
            organization=organization,
            permission="contacts.create",
        )

    def can_update(
        self,
        *,
        actor: User,
        contact: Contact,
    ) -> bool:
        """
        Check whether the actor can update a contact.
        """
        return self._check(
            actor=actor,
            organization=contact.organization,
            permission="contacts.update",
        )

    def can_delete(
        self,
        *,
        actor: User,
        contact: Contact,
    ) -> bool:
        """
        Check whether the actor can delete a contact.
        """
        return self._check(
            actor=actor,
            organization=contact.organization,
            permission="contacts.delete",
        )

    def can_verify(
        self,
        *,
        actor: User,
        contact: Contact,
    ) -> bool:
        """
        Check whether the actor can verify a contact.
        """
        return self._check(
            actor=actor,
            organization=contact.organization,
            permission="contacts.verify",
        )

    def can_activate(
        self,
        *,
        actor: User,
        contact: Contact,
    ) -> bool:
        """
        Check whether the actor can activate a contact.
        """
        return self._check(
            actor=actor,
            organization=contact.organization,
            permission="contacts.activate",
        )

    def can_deactivate(
        self,
        *,
        actor: User,
        contact: Contact,
    ) -> bool:
        """
        Check whether the actor can deactivate a contact.
        """
        return self._check(
            actor=actor,
            organization=contact.organization,
            permission="contacts.deactivate",
        )

    def can_set_primary(
        self,
        *,
        actor: User,
        contact: Contact,
    ) -> bool:
        """
        Check whether the actor can make a contact primary.
        """
        return self._check(
            actor=actor,
            organization=contact.organization,
            permission="contacts.set_primary",
        )


__all__ = ("ContactPolicy",)

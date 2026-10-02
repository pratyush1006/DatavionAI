"""
Authorization policies for Patient Identifiers.

Authorization is delegated to the platform RBAC engine. The policy layer
contains no persistence mutation and does not implement HTTP behavior.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.patient_management.identifiers.models import PatientIdentifier
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization
from apps.platform.rbac.engines.permission import user_has_permission


@dataclass(frozen=True, slots=True)
class IdentifierPolicy:
    """Authorization policy for Patient Identifier operations."""

    @staticmethod
    def _check(
        *,
        actor: User,
        organization: Organization,
        permission: str,
    ) -> bool:
        """Evaluate an identifier permission through the RBAC engine."""
        return user_has_permission(
            user=actor,
            permission=permission,
            organization=organization,
        )

    def can_view(
        self,
        *,
        actor: User,
        organization: Organization,
    ) -> bool:
        """Return whether the actor may view identifiers."""
        return self._check(
            actor=actor,
            organization=organization,
            permission="identifiers.view",
        )

    def can_create(
        self,
        *,
        actor: User,
        organization: Organization,
    ) -> bool:
        """Return whether the actor may create identifiers."""
        return self._check(
            actor=actor,
            organization=organization,
            permission="identifiers.create",
        )

    def can_update(
        self,
        *,
        actor: User,
        identifier: PatientIdentifier,
    ) -> bool:
        """Return whether the actor may update an identifier."""
        return self._check(
            actor=actor,
            organization=identifier.organization,
            permission="identifiers.update",
        )

    def can_verify(
        self,
        *,
        actor: User,
        identifier: PatientIdentifier,
    ) -> bool:
        """Return whether the actor may verify an identifier."""
        return self._check(
            actor=actor,
            organization=identifier.organization,
            permission="identifiers.verify",
        )

    def can_activate(
        self,
        *,
        actor: User,
        identifier: PatientIdentifier,
    ) -> bool:
        """Return whether the actor may activate an identifier."""
        return self._check(
            actor=actor,
            organization=identifier.organization,
            permission="identifiers.activate",
        )

    def can_deactivate(
        self,
        *,
        actor: User,
        identifier: PatientIdentifier,
    ) -> bool:
        """Return whether the actor may deactivate an identifier."""
        return self._check(
            actor=actor,
            organization=identifier.organization,
            permission="identifiers.deactivate",
        )

    def can_revoke(
        self,
        *,
        actor: User,
        identifier: PatientIdentifier,
    ) -> bool:
        """Return whether the actor may revoke an identifier."""
        return self._check(
            actor=actor,
            organization=identifier.organization,
            permission="identifiers.revoke",
        )

    def can_set_primary(
        self,
        *,
        actor: User,
        identifier: PatientIdentifier,
    ) -> bool:
        """Return whether the actor may make an identifier primary."""
        return self._check(
            actor=actor,
            organization=identifier.organization,
            permission="identifiers.set_primary",
        )

    def can_delete(
        self,
        *,
        actor: User,
        identifier: PatientIdentifier,
    ) -> bool:
        """Return whether the actor may delete an identifier."""
        return self._check(
            actor=actor,
            organization=identifier.organization,
            permission="identifiers.delete",
        )


__all__ = ("IdentifierPolicy",)

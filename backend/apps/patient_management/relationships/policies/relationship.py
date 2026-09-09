"""
Authorization policy for Patient Relationships.

Policies are responsible only for authorization decisions. They do not
perform persistence or orchestration.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from apps.patient_management.relationships.permissions import (
    PatientRelationshipPermission,
)
from apps.platform.rbac.engines.permission import user_has_permission

if TYPE_CHECKING:
    from apps.patient_management.relationships.models import (
        PatientRelationship,
    )
    from apps.platform.accounts.models import User
    from apps.platform.organizations.models import Organization


class PatientRelationshipPolicy:
    """
    Authorization policy for PatientRelationship operations.

    Organization isolation is enforced by passing the relationship's
    organization into the RBAC permission resolver.
    """

    @staticmethod
    def _check(
        *,
        actor: User,
        permission: str,
        organization: Organization | None = None,
    ) -> bool:
        """
        Evaluate a platform RBAC permission.
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
        relationship: PatientRelationship,
    ) -> bool:
        """
        Determine whether the actor may view a relationship.
        """

        return self._check(
            actor=actor,
            permission=PatientRelationshipPermission.VIEW,
            organization=relationship.organization,
        )

    def can_list(
        self,
        *,
        actor: User,
        organization: Organization,
    ) -> bool:
        """
        Determine whether the actor may list relationships.
        """

        return self._check(
            actor=actor,
            permission=PatientRelationshipPermission.LIST,
            organization=organization,
        )

    def can_create(
        self,
        *,
        actor: User,
        organization: Organization,
    ) -> bool:
        """
        Determine whether the actor may create a relationship.
        """

        return self._check(
            actor=actor,
            permission=PatientRelationshipPermission.CREATE,
            organization=organization,
        )

    def can_update(
        self,
        *,
        actor: User,
        relationship: PatientRelationship,
    ) -> bool:
        """
        Determine whether the actor may update a relationship.
        """

        return self._check(
            actor=actor,
            permission=PatientRelationshipPermission.UPDATE,
            organization=relationship.organization,
        )

    def can_delete(
        self,
        *,
        actor: User,
        relationship: PatientRelationship,
    ) -> bool:
        """
        Determine whether the actor may delete a relationship.
        """

        return self._check(
            actor=actor,
            permission=PatientRelationshipPermission.DELETE,
            organization=relationship.organization,
        )

    def can_restore(
        self,
        *,
        actor: User,
        relationship: PatientRelationship,
    ) -> bool:
        """
        Determine whether the actor may restore a deleted relationship.
        """

        return self._check(
            actor=actor,
            permission=PatientRelationshipPermission.RESTORE,
            organization=relationship.organization,
        )

    def can_verify(
        self,
        *,
        actor: User,
        relationship: PatientRelationship,
    ) -> bool:
        """
        Determine whether the actor may verify a relationship.
        """

        return self._check(
            actor=actor,
            permission=PatientRelationshipPermission.VERIFY,
            organization=relationship.organization,
        )

    def can_terminate(
        self,
        *,
        actor: User,
        relationship: PatientRelationship,
    ) -> bool:
        """
        Determine whether the actor may terminate a relationship.
        """

        return self._check(
            actor=actor,
            permission=PatientRelationshipPermission.TERMINATE,
            organization=relationship.organization,
        )

    def can_set_primary(
        self,
        *,
        actor: User,
        relationship: PatientRelationship,
    ) -> bool:
        """
        Determine whether the actor may mark a relationship as primary.
        """

        return self._check(
            actor=actor,
            permission=PatientRelationshipPermission.SET_PRIMARY,
            organization=relationship.organization,
        )

    def can_export(
        self,
        *,
        actor: User,
        organization: Organization,
    ) -> bool:
        """
        Determine whether the actor may export relationships.
        """

        return self._check(
            actor=actor,
            permission=PatientRelationshipPermission.EXPORT,
            organization=organization,
        )

    def can_import(
        self,
        *,
        actor: User,
        organization: Organization,
    ) -> bool:
        """
        Determine whether the actor may import relationships.
        """

        return self._check(
            actor=actor,
            permission=PatientRelationshipPermission.IMPORT,
            organization=organization,
        )


__all__ = ("PatientRelationshipPolicy",)

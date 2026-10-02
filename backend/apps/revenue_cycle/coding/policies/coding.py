from __future__ import annotations

"""Authorization policies for Revenue Cycle Coding."""

from typing import Any

from ..permissions import CodingPermissions
from ..rbac import has_permission


class CodingPolicy:
    """Enforce RBAC and organization ownership boundaries."""

    @staticmethod
    def can_list(*, actor: Any, organization: Any) -> bool:
        """Check Coding list permission."""

        return has_permission(
            user=actor,
            permission=CodingPermissions.LIST,
            organization=organization,
        )

    @staticmethod
    def can_view(
        *,
        actor: Any,
        organization: Any,
        record: Any,
    ) -> bool:
        """Check record ownership and view permission."""

        return record.organization_id == organization.id and has_permission(
            user=actor,
            permission=CodingPermissions.VIEW,
            organization=organization,
        )

    @staticmethod
    def can_create(*, actor: Any, organization: Any) -> bool:
        """Check Coding creation permission."""

        return has_permission(
            user=actor,
            permission=CodingPermissions.CREATE,
            organization=organization,
        )

    @staticmethod
    def can_update(
        *,
        actor: Any,
        organization: Any,
        record: Any,
    ) -> bool:
        """Check Coding update permission and ownership."""

        return CodingPolicy.can_mutate(
            actor=actor,
            organization=organization,
            record=record,
            permission=CodingPermissions.UPDATE,
        )

    @staticmethod
    def can_delete(
        *,
        actor: Any,
        organization: Any,
        record: Any,
    ) -> bool:
        """Check Coding delete permission and ownership."""

        return CodingPolicy.can_mutate(
            actor=actor,
            organization=organization,
            record=record,
            permission=CodingPermissions.DELETE,
        )

    @staticmethod
    def can_restore(*, actor: Any, organization: Any) -> bool:
        """Check Coding restore permission."""

        return has_permission(
            user=actor,
            permission=CodingPermissions.RESTORE,
            organization=organization,
        )

    @staticmethod
    def can_transition(
        *,
        actor: Any,
        organization: Any,
        record: Any,
        permission: str,
    ) -> bool:
        """Check lifecycle permission and record ownership."""

        return CodingPolicy.can_mutate(
            actor=actor,
            organization=organization,
            record=record,
            permission=permission,
        )

    @staticmethod
    def can_mutate(
        *,
        actor: Any,
        organization: Any,
        record: Any,
        permission: str,
    ) -> bool:
        """Check a mutation permission and organization ownership."""

        return record.organization_id == organization.id and has_permission(
            user=actor,
            permission=permission,
            organization=organization,
        )


__all__ = ("CodingPolicy",)

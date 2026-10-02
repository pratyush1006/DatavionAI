"""Authorization policy for Patient Communication."""

from __future__ import annotations

from typing import Any

from apps.patient_management.communication.permissions.communication import (
    PatientCommunicationPermission,
)
from apps.platform.rbac.engines import user_has_permission


class PatientCommunicationPolicy:
    """Enforce RBAC decisions within an organization boundary."""

    @staticmethod
    def _allowed(actor: Any, permission: str, organization: Any) -> bool:
        """Return whether the actor has the requested permission."""
        return user_has_permission(
            user=actor, permission=permission, organization=organization
        )

    @classmethod
    def can_view(cls, *, actor: Any, organization: Any) -> bool:
        """Authorize viewing communications."""
        return cls._allowed(actor, PatientCommunicationPermission.VIEW, organization)

    @classmethod
    def can_create(cls, *, actor: Any, organization: Any) -> bool:
        """Authorize communication creation."""
        return cls._allowed(actor, PatientCommunicationPermission.CREATE, organization)

    @classmethod
    def can_update(cls, *, actor: Any, organization: Any) -> bool:
        """Authorize communication updates."""
        return cls._allowed(actor, PatientCommunicationPermission.UPDATE, organization)

    @classmethod
    def can_delete(cls, *, actor: Any, organization: Any) -> bool:
        """Authorize communication deletion."""
        return cls._allowed(actor, PatientCommunicationPermission.DELETE, organization)

    @classmethod
    def can_restore(cls, *, actor: Any, organization: Any) -> bool:
        """Authorize communication restoration."""
        return cls._allowed(actor, PatientCommunicationPermission.RESTORE, organization)

    @classmethod
    def can_status(cls, *, actor: Any, organization: Any, status: str) -> bool:
        """Authorize a status transition."""
        permission_map = {
            "queued": PatientCommunicationPermission.QUEUE,
            "sent": PatientCommunicationPermission.SEND,
            "delivered": PatientCommunicationPermission.DELIVER,
            "read": PatientCommunicationPermission.READ,
            "failed": PatientCommunicationPermission.FAIL,
            "cancelled": PatientCommunicationPermission.CANCEL,
            "archived": PatientCommunicationPermission.ARCHIVE,
        }
        permission = permission_map.get(status)
        return permission is not None and cls._allowed(actor, permission, organization)


__all__ = ("PatientCommunicationPolicy",)

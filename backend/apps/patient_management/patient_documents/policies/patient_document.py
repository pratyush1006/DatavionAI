"""Authorization policy for Patient Documents."""

from __future__ import annotations

from apps.patient_management.patient_documents.permissions import (
    PatientDocumentPermission,
)
from apps.platform.rbac.services import (
    user_has_permission,
)


class PatientDocumentPolicy:
    """Evaluate organization-scoped Patient Document permissions."""

    def can_list(
        self,
        *,
        actor,
        organization,
    ) -> bool:
        """Return whether the actor can list patient documents."""
        return user_has_permission(
            user=actor,
            permission=PatientDocumentPermission.LIST,
            organization=organization,
        )

    def can_view(
        self,
        *,
        actor,
        document,
    ) -> bool:
        """Return whether the actor can view a patient document."""
        return user_has_permission(
            user=actor,
            permission=PatientDocumentPermission.VIEW,
            organization=document.organization,
        )

    def can_create(
        self,
        *,
        actor,
        organization,
    ) -> bool:
        """Return whether the actor can create a patient document."""
        return user_has_permission(
            user=actor,
            permission=PatientDocumentPermission.CREATE,
            organization=organization,
        )

    def can_update(
        self,
        *,
        actor,
        document,
    ) -> bool:
        """Return whether the actor can update a patient document."""
        return user_has_permission(
            user=actor,
            permission=PatientDocumentPermission.UPDATE,
            organization=document.organization,
        )

    def can_delete(
        self,
        *,
        actor,
        document,
    ) -> bool:
        """Return whether the actor can delete a patient document."""
        return user_has_permission(
            user=actor,
            permission=PatientDocumentPermission.DELETE,
            organization=document.organization,
        )

    def can_restore(
        self,
        *,
        actor,
        document,
    ) -> bool:
        """Return whether the actor can restore a patient document."""
        return user_has_permission(
            user=actor,
            permission=PatientDocumentPermission.RESTORE,
            organization=document.organization,
        )

    def can_activate(
        self,
        *,
        actor,
        document,
    ) -> bool:
        """Return whether the actor can activate a patient document."""
        return user_has_permission(
            user=actor,
            permission=PatientDocumentPermission.ACTIVATE,
            organization=document.organization,
        )

    def can_archive(
        self,
        *,
        actor,
        document,
    ) -> bool:
        """Return whether the actor can archive a patient document."""
        return user_has_permission(
            user=actor,
            permission=PatientDocumentPermission.ARCHIVE,
            organization=document.organization,
        )

    def can_create_version(
        self,
        *,
        actor,
        document,
    ) -> bool:
        """Return whether the actor can create a document version."""
        return user_has_permission(
            user=actor,
            permission=PatientDocumentPermission.VERSION_CREATE,
            organization=document.organization,
        )

    def can_view_access_audit(
        self,
        *,
        actor,
        document,
    ) -> bool:
        """Return whether the actor can view access audit records."""
        return user_has_permission(
            user=actor,
            permission=PatientDocumentPermission.ACCESS_AUDIT,
            organization=document.organization,
        )


__all__ = ("PatientDocumentPolicy",)

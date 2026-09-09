"""
Authorization policy for Patient Consents.
"""

from __future__ import annotations

from apps.patient_management.consents.permissions.consent import (
    PatientConsentPermission,
)
from apps.platform.rbac.engines.permission import (
    user_has_permission,
)


class PatientConsentPolicy:
    """
    Authorize Patient Consent operations through platform RBAC.
    """

    @staticmethod
    def _check(
        *,
        actor,
        permission: str,
        organization,
    ) -> bool:
        """
        Check one RBAC permission within an organization.
        """
        return user_has_permission(
            user=actor,
            permission=permission,
            organization=organization,
        )

    def can_view(
        self,
        *,
        actor,
        consent,
    ) -> bool:
        """
        Determine whether the actor may view a consent.
        """
        return self._check(
            actor=actor,
            permission=PatientConsentPermission.VIEW,
            organization=consent.organization,
        )

    def can_list(
        self,
        *,
        actor,
        organization,
    ) -> bool:
        """
        Determine whether the actor may list consents.
        """
        return self._check(
            actor=actor,
            permission=PatientConsentPermission.LIST,
            organization=organization,
        )

    def can_create(
        self,
        *,
        actor,
        organization,
    ) -> bool:
        """
        Determine whether the actor may create a consent.
        """
        return self._check(
            actor=actor,
            permission=PatientConsentPermission.CREATE,
            organization=organization,
        )

    def can_update(
        self,
        *,
        actor,
        consent,
    ) -> bool:
        """
        Determine whether the actor may update a consent.
        """
        return self._check(
            actor=actor,
            permission=PatientConsentPermission.UPDATE,
            organization=consent.organization,
        )

    def can_delete(
        self,
        *,
        actor,
        consent,
    ) -> bool:
        """
        Determine whether the actor may delete a consent.
        """
        return self._check(
            actor=actor,
            permission=PatientConsentPermission.DELETE,
            organization=consent.organization,
        )

    def can_restore(
        self,
        *,
        actor,
        consent,
    ) -> bool:
        """
        Determine whether the actor may restore a consent.
        """
        return self._check(
            actor=actor,
            permission=PatientConsentPermission.RESTORE,
            organization=consent.organization,
        )

    def can_grant(
        self,
        *,
        actor,
        consent,
    ) -> bool:
        """
        Determine whether the actor may grant a consent.
        """
        return self._check(
            actor=actor,
            permission=PatientConsentPermission.GRANT,
            organization=consent.organization,
        )

    def can_revoke(
        self,
        *,
        actor,
        consent,
    ) -> bool:
        """
        Determine whether the actor may revoke a consent.
        """
        return self._check(
            actor=actor,
            permission=PatientConsentPermission.REVOKE,
            organization=consent.organization,
        )


__all__ = ("PatientConsentPolicy",)

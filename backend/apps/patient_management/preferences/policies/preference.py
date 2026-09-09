"""Authorization policy for Patient Preferences."""

from __future__ import annotations

from apps.patient_management.preferences.permissions import PatientPreferencePermission
from apps.platform.rbac.engines import user_has_permission


class PatientPreferencePolicy:
    """Evaluate organization-scoped preference permissions."""

    def _allowed(self, *, actor, organization, permission):
        """Evaluate one organization-scoped RBAC permission."""

        return user_has_permission(
            user=actor,
            permission=permission,
            organization=organization,
        )

    def can_list(self, *, actor, organization):
        """Return whether the actor can list preferences."""

        return self._allowed(
            actor=actor,
            organization=organization,
            permission=PatientPreferencePermission.LIST,
        )

    def can_view(self, *, actor, preference):
        """Return whether the actor can view a preference."""

        return self._allowed(
            actor=actor,
            organization=preference.organization,
            permission=PatientPreferencePermission.VIEW,
        )

    def can_create(self, *, actor, organization):
        """Return whether the actor can create preferences."""

        return self._allowed(
            actor=actor,
            organization=organization,
            permission=PatientPreferencePermission.CREATE,
        )

    def can_update(self, *, actor, preference):
        """Return whether the actor can update a preference."""

        return self._allowed(
            actor=actor,
            organization=preference.organization,
            permission=PatientPreferencePermission.UPDATE,
        )

    def can_delete(self, *, actor, preference):
        """Return whether the actor can delete a preference."""

        return self._allowed(
            actor=actor,
            organization=preference.organization,
            permission=PatientPreferencePermission.DELETE,
        )

    def can_restore(self, *, actor, preference):
        """Return whether the actor can restore a preference."""

        return self._allowed(
            actor=actor,
            organization=preference.organization,
            permission=PatientPreferencePermission.RESTORE,
        )

    def can_manage_communication(self, *, actor, preference):
        """Return whether the actor can manage communication preferences."""

        return self._allowed(
            actor=actor,
            organization=preference.organization,
            permission=PatientPreferencePermission.COMMUNICATION_MANAGE,
        )


__all__ = ("PatientPreferencePolicy",)

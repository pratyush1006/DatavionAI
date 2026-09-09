"""
Authorization policies for Patient Portal.
"""

from __future__ import annotations

from apps.platform.rbac.engines.permission import user_has_permission


class PatientPortalPolicy:
    """Evaluate organization-scoped portal permissions."""

    @staticmethod
    def _check(
        *,
        actor,
        permission: str,
        organization,
    ) -> bool:
        """Evaluate one RBAC permission."""

        return user_has_permission(
            user=actor,
            permission=permission,
            organization=organization,
        )

    def can_list(self, *, actor, organization) -> bool:
        """Return whether the actor may list portal accounts."""

        return self._check(
            actor=actor,
            permission="patient_portal.list",
            organization=organization,
        )

    def can_view(self, *, actor, account) -> bool:
        """Return whether the actor may view a portal account."""

        return self._check(
            actor=actor,
            permission="patient_portal.view",
            organization=account.organization,
        )

    def can_create(self, *, actor, organization) -> bool:
        """Return whether the actor may create a portal account."""

        return self._check(
            actor=actor,
            permission="patient_portal.create",
            organization=organization,
        )

    def can_update(self, *, actor, account) -> bool:
        """Return whether the actor may update a portal account."""

        return self._check(
            actor=actor,
            permission="patient_portal.update",
            organization=account.organization,
        )

    def can_delete(self, *, actor, account) -> bool:
        """Return whether the actor may delete a portal account."""

        return self._check(
            actor=actor,
            permission="patient_portal.delete",
            organization=account.organization,
        )

    def can_restore(self, *, actor, account) -> bool:
        """Return whether the actor may restore a portal account."""

        return self._check(
            actor=actor,
            permission="patient_portal.restore",
            organization=account.organization,
        )

    def can_transition(self, *, actor, account) -> bool:
        """Return whether the actor may transition account state."""

        return self._check(
            actor=actor,
            permission="patient_portal.transition",
            organization=account.organization,
        )

    def can_invite(self, *, actor, account) -> bool:
        """Return whether the actor may issue portal invitations."""

        return self._check(
            actor=actor,
            permission="patient_portal.invite",
            organization=account.organization,
        )


__all__ = ("PatientPortalPolicy",)

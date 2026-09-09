"""Authorization policy for medical history."""

from __future__ import annotations

from apps.platform.rbac.engines.permission import user_has_permission


class MedicalHistoryPolicy:
    """MedicalHistoryPolicy implementation."""

    @staticmethod
    def _check(*, actor, permission: str, organization) -> bool:
        """check."""
        return user_has_permission(
            user=actor, permission=permission, organization=organization
        )

    def can_view(self, *, actor, history) -> bool:
        """Can view."""
        return self._check(
            actor=actor,
            permission="patient_medical_history.view",
            organization=history.organization,
        )

    def can_list(self, *, actor, organization) -> bool:
        """Can list."""
        return self._check(
            actor=actor,
            permission="patient_medical_history.list",
            organization=organization,
        )

    def can_create(self, *, actor, organization) -> bool:
        """Can create."""
        return self._check(
            actor=actor,
            permission="patient_medical_history.create",
            organization=organization,
        )

    def can_update(self, *, actor, history) -> bool:
        """Can update."""
        return self._check(
            actor=actor,
            permission="patient_medical_history.update",
            organization=history.organization,
        )

    def can_delete(self, *, actor, history) -> bool:
        """Can delete."""
        return self._check(
            actor=actor,
            permission="patient_medical_history.delete",
            organization=history.organization,
        )

    def can_restore(self, *, actor, history) -> bool:
        """Can restore."""
        return self._check(
            actor=actor,
            permission="patient_medical_history.restore",
            organization=history.organization,
        )

    def can_activate(self, *, actor, history) -> bool:
        """Can activate."""
        return self._check(
            actor=actor,
            permission="patient_medical_history.activate",
            organization=history.organization,
        )

    def can_deactivate(self, *, actor, history) -> bool:
        """Can deactivate."""
        return self._check(
            actor=actor,
            permission="patient_medical_history.deactivate",
            organization=history.organization,
        )

    def can_verify(self, *, actor, history) -> bool:
        """Can verify."""
        return self._check(
            actor=actor,
            permission="patient_medical_history.verify",
            organization=history.organization,
        )


__all__ = ("MedicalHistoryPolicy",)

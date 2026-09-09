"""Authorization policies for patient emergency records."""

from __future__ import annotations

from apps.patient_management.emergency.exceptions import (
    EmergencyPolicyError,
)
from apps.platform.rbac.permissions.base import user_has_permission


class EmergencyPolicy:
    """Enforce organization-scoped emergency record authorization."""

    @staticmethod
    def can_view(*, actor, organization) -> bool:
        """Check permission to view emergency records."""

        return user_has_permission(
            user=actor,
            permission="patient_emergency.view",
            organization=organization,
        )

    @staticmethod
    def can_create(*, actor, organization) -> bool:
        """Check permission to create emergency records."""

        return user_has_permission(
            user=actor,
            permission="patient_emergency.create",
            organization=organization,
        )

    @staticmethod
    def can_update(*, actor, organization) -> bool:
        """Check permission to update emergency records."""

        return user_has_permission(
            user=actor,
            permission="patient_emergency.update",
            organization=organization,
        )

    @staticmethod
    def can_delete(*, actor, organization) -> bool:
        """Check permission to delete emergency records."""

        return user_has_permission(
            user=actor,
            permission="patient_emergency.delete",
            organization=organization,
        )

    @staticmethod
    def require(self, allowed: bool, message: str) -> None:
        """Raise a policy error when an operation is denied."""

        if not allowed:
            raise EmergencyPolicyError(message)


__all__ = ("EmergencyPolicy",)

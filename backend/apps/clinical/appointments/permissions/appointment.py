"""RBAC permissions for Clinical Appointments."""

from __future__ import annotations

from apps.platform.rbac.resolvers import resolve_permissions


class AppointmentPermission:
    """Resolve organization-scoped Appointment permissions."""

    code_prefix = "appointment"

    @staticmethod
    def has_permission(*, user, permission: str, organization=None) -> bool:
        """Return whether the actor has the requested permission."""

        return permission in resolve_permissions(
            user=user,
            organization=organization,
        )


PERMISSION_CODES = (
    "appointment.view",
    "appointment.create",
    "appointment.update",
    "appointment.delete",
    "appointment.transition",
)


__all__ = (
    "AppointmentPermission",
    "PERMISSION_CODES",
)

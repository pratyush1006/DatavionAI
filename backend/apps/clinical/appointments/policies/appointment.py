"""Authorization policies for Clinical Appointments."""

from __future__ import annotations

from apps.clinical.appointments.permissions import AppointmentPermission


class AppointmentPolicy:
    """Enforce Appointment permission boundaries."""

    @staticmethod
    def can_view(*, actor, organization) -> bool:
        """Check view permission."""

        return AppointmentPermission.has_permission(
            user=actor,
            permission="appointment.view",
            organization=organization,
        )

    @staticmethod
    def can_create(*, actor, organization) -> bool:
        """Check create permission."""

        return AppointmentPermission.has_permission(
            user=actor,
            permission="appointment.create",
            organization=organization,
        )

    @staticmethod
    def can_update(*, actor, organization) -> bool:
        """Check update permission."""

        return AppointmentPermission.has_permission(
            user=actor,
            permission="appointment.update",
            organization=organization,
        )

    @staticmethod
    def can_delete(*, actor, organization) -> bool:
        """Check delete permission."""

        return AppointmentPermission.has_permission(
            user=actor,
            permission="appointment.delete",
            organization=organization,
        )

    @staticmethod
    def can_transition(*, actor, organization) -> bool:
        """Check transition permission."""

        return AppointmentPermission.has_permission(
            user=actor,
            permission="appointment.transition",
            organization=organization,
        )


__all__ = ("AppointmentPolicy",)

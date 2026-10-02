"""Organization-scoped Clinical Appointment selectors."""

from __future__ import annotations

from uuid import UUID

from apps.clinical.appointments.models import Appointment


class AppointmentSelector:
    """Provide read-only organization-scoped appointment queries."""

    @staticmethod
    def queryset(*, organization):
        """Return active appointments for an organization."""

        return Appointment.objects.select_related(
            "organization",
            "patient",
            "provider",
        ).filter(
            organization=organization,
            is_deleted=False,
        )

    @classmethod
    def get(cls, *, organization, appointment_id: UUID) -> Appointment:
        """Return one appointment in organization scope."""

        return cls.queryset(
            organization=organization,
        ).get(
            id=appointment_id,
        )

    @classmethod
    def for_patient(cls, *, organization, patient_id: UUID):
        """Return appointments for one organization-scoped patient."""

        return cls.queryset(
            organization=organization,
        ).filter(
            patient_id=patient_id,
        )


__all__ = ("AppointmentSelector",)

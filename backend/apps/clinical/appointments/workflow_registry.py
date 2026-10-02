"""Workflow registration for Clinical Appointments."""

from __future__ import annotations

from apps.clinical.appointments.workflows import (
    AppointmentBookingWorkflow,
    AppointmentCancelWorkflow,
    AppointmentCheckInWorkflow,
    AppointmentCompleteWorkflow,
    AppointmentConfirmWorkflow,
    AppointmentDeleteWorkflow,
    AppointmentRescheduleWorkflow,
    AppointmentStartWorkflow,
    AppointmentTransitionWorkflow,
    AppointmentUpdateWorkflow,
)
from apps.core.workflows import workflow_registry


def register_workflows() -> None:
    """Register all Clinical Appointment workflows."""

    registrations = (
        ("appointment.create", AppointmentBookingWorkflow),
        ("appointment.update", AppointmentUpdateWorkflow),
        ("appointment.delete", AppointmentDeleteWorkflow),
        ("appointment.transition", AppointmentTransitionWorkflow),
        ("appointment.confirm", AppointmentConfirmWorkflow),
        ("appointment.reschedule", AppointmentRescheduleWorkflow),
        ("appointment.check_in", AppointmentCheckInWorkflow),
        ("appointment.start", AppointmentStartWorkflow),
        ("appointment.cancel", AppointmentCancelWorkflow),
        ("appointment.complete", AppointmentCompleteWorkflow),
    )

    for name, workflow in registrations:
        if not workflow_registry.is_registered(name):
            workflow_registry.register(
                name=name,
                workflow=workflow,
            )


__all__ = ("register_workflows",)

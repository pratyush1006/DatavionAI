"""Clinical Appointment contract tests."""

from django.test import SimpleTestCase

from apps.clinical.appointments.constants import AppointmentStatus
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
from apps.core.events import DomainEvent


class AppointmentContractTests(SimpleTestCase):
    """Validate the production application contracts."""

    def test_status_contract(self):
        """Validate the seven Appointment lifecycle states."""

        self.assertEqual(
            {
                "scheduled",
                "confirmed",
                "checked_in",
                "in_progress",
                "completed",
                "cancelled",
                "no_show",
            },
            {choice[0] for choice in AppointmentStatus.choices},
        )

    def test_mutation_workflows_exist(self):
        """Validate the full Appointment workflow surface."""

        workflows = (
            AppointmentBookingWorkflow,
            AppointmentUpdateWorkflow,
            AppointmentDeleteWorkflow,
            AppointmentTransitionWorkflow,
            AppointmentConfirmWorkflow,
            AppointmentRescheduleWorkflow,
            AppointmentCheckInWorkflow,
            AppointmentStartWorkflow,
            AppointmentCancelWorkflow,
            AppointmentCompleteWorkflow,
        )

        self.assertEqual(
            len({workflow.workflow_name for workflow in workflows}),
            len(workflows),
        )

        for workflow in workflows:
            self.assertTrue(
                hasattr(
                    workflow,
                    "execute",
                ),
            )

    def test_domain_events_extend_platform_domain_event(self):
        """Ensure Appointment events use the canonical event base."""

        from apps.clinical.appointments.events import (
            AppointmentCreated,
            AppointmentDeleted,
            AppointmentStatusChanged,
            AppointmentUpdated,
        )

        for event in (
            AppointmentCreated,
            AppointmentDeleted,
            AppointmentStatusChanged,
            AppointmentUpdated,
        ):
            self.assertTrue(
                issubclass(
                    event,
                    DomainEvent,
                ),
            )


__all__ = ("AppointmentContractTests",)

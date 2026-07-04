"""
Tests for appointment services.
"""

from __future__ import annotations

from datetime import timedelta

from django.utils import timezone

from apps.appointments.constants import (
    AppointmentPriority,
    AppointmentStatus,
    AppointmentType,
)
from apps.appointments.models import Appointment
from apps.appointments.services import (
    create_appointment,
    delete_appointment,
    update_appointment,
)
from apps.common.tests.base import BaseTestCase


class AppointmentServiceTestCase(BaseTestCase):
    """
    Test cases for appointment services.
    """

    def setUp(
        self,
    ) -> None:
        """
        Set up test data.
        """

        super().setUp()

        self.employee = self.create_employee(
            organization=self.organization,
        )

        self.provider = self.create_provider(
            organization=self.organization,
            employee=self.employee,
        )

        self.patient = self.create_patient(
            organization=self.organization,
        )

        self.appointment = Appointment.objects.create(
            organization=self.organization,
            patient=self.patient,
            provider=self.provider,
            appointment_number="APT000001",
            appointment_type=AppointmentType.CONSULTATION,
            status=AppointmentStatus.SCHEDULED,
            priority=AppointmentPriority.NORMAL,
            scheduled_start=timezone.now(),
            scheduled_end=timezone.now() + timedelta(
                minutes=30,
            ),
            duration_minutes=30,
            reason="General Consultation",
        )

    def test_create_appointment(
        self,
    ) -> None:
        """
        Appointment should be created successfully.
        """

        appointment = create_appointment(
            validated_data={
                "organization": self.organization,
                "patient": self.patient,
                "provider": self.provider,
                "appointment_number": "APT000002",
                "appointment_type": AppointmentType.FOLLOW_UP,
                "status": AppointmentStatus.CONFIRMED,
                "priority": AppointmentPriority.HIGH,
                "scheduled_start": timezone.now(),
                "scheduled_end": timezone.now()
                + timedelta(minutes=45),
                "duration_minutes": 45,
                "reason": "Follow-up Visit",
            },
        )

        self.assertIsInstance(
            appointment,
            Appointment,
        )

        self.assertEqual(
            appointment.appointment_number,
            "APT000002",
        )

        self.assertEqual(
            appointment.patient,
            self.patient,
        )

        self.assertEqual(
            appointment.provider,
            self.provider,
        )

    def test_update_appointment(
        self,
    ) -> None:
        """
        Appointment should be updated successfully.
        """

        updated = update_appointment(
            instance=self.appointment,
            validated_data={
                "status": AppointmentStatus.COMPLETED,
                "priority": AppointmentPriority.URGENT,
                "reason": "Consultation Completed",
            },
        )

        updated.refresh_from_db()

        self.assertEqual(
            updated.status,
            AppointmentStatus.COMPLETED,
        )

        self.assertEqual(
            updated.priority,
            AppointmentPriority.URGENT,
        )

        self.assertEqual(
            updated.reason,
            "Consultation Completed",
        )

    def test_delete_appointment(
        self,
    ) -> None:
        """
        Appointment should be deleted successfully.
        """

        appointment_id = self.appointment.id

        delete_appointment(
            instance=self.appointment,
        )

        self.assertFalse(
            Appointment.objects.filter(
                id=appointment_id,
            ).exists(),
        )

    def test_update_returns_same_instance(
        self,
    ) -> None:
        """
        Update service should return the same instance.
        """

        updated = update_appointment(
            instance=self.appointment,
            validated_data={
                "priority": AppointmentPriority.LOW,
            },
        )

        self.assertEqual(
            updated.pk,
            self.appointment.pk,
        )

        self.assertEqual(
            updated.priority,
            AppointmentPriority.LOW,
        )

    def test_create_persists_to_database(
        self,
    ) -> None:
        """
        Appointment should persist after creation.
        """

        initial_count = Appointment.objects.count()

        create_appointment(
            validated_data={
                "organization": self.organization,
                "patient": self.patient,
                "provider": self.provider,
                "appointment_number": "APT000003",
                "appointment_type": AppointmentType.SURGERY,
                "scheduled_start": timezone.now(),
                "scheduled_end": timezone.now()
                + timedelta(hours=2),
            },
        )

        self.assertEqual(
            Appointment.objects.count(),
            initial_count + 1,
        )


__all__ = [
    "AppointmentServiceTestCase",
]

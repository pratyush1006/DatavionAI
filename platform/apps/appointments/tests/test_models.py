"""
Tests for the Appointment model.
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
from apps.common.tests.base import BaseTestCase
from apps.providers.constants import ProviderType


class AppointmentModelTestCase(BaseTestCase):
    """
    Test cases for the Appointment model.
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
            provider_number="PRV000001",
            license_number="LIC000001",
            provider_type=ProviderType.PHYSICIAN,
        )

        self.patient = self.create_patient(
            organization=self.organization,
            mrn="MRN000001",
            first_name="John",
            last_name="Doe",
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
            scheduled_end=timezone.now()
            + timedelta(
                minutes=30,
            ),
            duration_minutes=30,
            reason="General Consultation",
        )

    def test_str(
        self,
    ) -> None:
        """
        String representation should be correct.
        """

        self.assertEqual(
            str(self.appointment),
            (
                f"{self.appointment.appointment_number} | "
                f"{self.patient.full_name} | "
                f"{self.provider.employee.full_name}"
            ),
        )

    def test_title_property(
        self,
    ) -> None:
        """
        Title property should return a readable title.
        """

        self.assertEqual(
            self.appointment.title,
            (
                f"{self.appointment.appointment_number} | "
                f"{self.patient.full_name} | "
                f"{self.provider.employee.full_name}"
            ),
        )

    def test_defaults(
        self,
    ) -> None:
        """
        Default values should be assigned.
        """

        appointment = Appointment.objects.create(
            organization=self.organization,
            patient=self.patient,
            provider=self.provider,
            appointment_number="APT000002",
            appointment_type=AppointmentType.FOLLOW_UP,
            scheduled_start=timezone.now(),
            scheduled_end=timezone.now()
            + timedelta(
                minutes=30,
            ),
        )

        self.assertEqual(
            appointment.status,
            AppointmentStatus.SCHEDULED,
        )

        self.assertEqual(
            appointment.priority,
            AppointmentPriority.NORMAL,
        )

        self.assertEqual(
            appointment.duration_minutes,
            30,
        )

        self.assertFalse(
            appointment.is_virtual,
        )


__all__ = [
    "AppointmentModelTestCase",
]

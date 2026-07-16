"""
Tests for appointment API endpoints.
"""

from __future__ import annotations

from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from apps.clinical.appointments.constants import (
    AppointmentPriority,
    AppointmentStatus,
    AppointmentType,
)
from apps.clinical.appointments.models import Appointment
from apps.common.tests.base import BaseAPITestCase


class AppointmentAPITestCase(BaseAPITestCase):
    """
    Test cases for appointment API endpoints.
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
            scheduled_end=timezone.now()
            + timedelta(
                minutes=30,
            ),
            duration_minutes=30,
            reason="General Consultation",
        )

        self.list_url = reverse(
            "appointments:list-create",
        )

        self.detail_url = reverse(
            "appointments:detail",
            kwargs={
                "appointment_id": self.appointment.id,
            },
        )

    def test_list_appointments(
        self,
    ) -> None:
        """
        List endpoint should return HTTP 200.
        """

        response = self.client.get(
            self.list_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_retrieve_appointment(
        self,
    ) -> None:
        """
        Detail endpoint should return HTTP 200.
        """

        response = self.client.get(
            self.detail_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_create_appointment(
        self,
    ) -> None:
        """
        Create endpoint should create an appointment.
        """

        payload = {
            "organization": str(self.organization.id),
            "patient": str(self.patient.id),
            "provider": str(self.provider.id),
            "appointment_number": "APT000002",
            "appointment_type": AppointmentType.FOLLOW_UP,
            "status": AppointmentStatus.CONFIRMED,
            "priority": AppointmentPriority.HIGH,
            "scheduled_start": timezone.now().isoformat(),
            "scheduled_end": (
                timezone.now()
                + timedelta(
                    minutes=45,
                )
            ).isoformat(),
            "duration_minutes": 45,
            "reason": "Follow-up",
        }

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_create_appointment_validation_error(
        self,
    ) -> None:
        """
        Invalid payload should return HTTP 400.
        """

        response = self.client.post(
            self.list_url,
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_update_appointment(
        self,
    ) -> None:
        """
        PUT endpoint should update the appointment.
        """

        response = self.client.put(
            self.detail_url,
            {
                "organization": str(self.organization.id),
                "patient": str(self.patient.id),
                "provider": str(self.provider.id),
                "appointment_number": "APT000001",
                "appointment_type": AppointmentType.CONSULTATION,
                "status": AppointmentStatus.COMPLETED,
                "priority": AppointmentPriority.URGENT,
                "scheduled_start": self.appointment.scheduled_start.isoformat(),
                "scheduled_end": self.appointment.scheduled_end.isoformat(),
                "duration_minutes": 30,
                "reason": "Completed",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_partial_update_appointment(
        self,
    ) -> None:
        """
        PATCH endpoint should update part of the appointment.
        """

        response = self.client.patch(
            self.detail_url,
            {
                "status": AppointmentStatus.CANCELLED,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_delete_appointment(
        self,
    ) -> None:
        """
        DELETE endpoint should remove the appointment.
        """

        response = self.client.delete(
            self.detail_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

    def test_requires_authentication(
        self,
    ) -> None:
        """
        Endpoints should require authentication.
        """

        self.client.force_authenticate(
            user=None,
        )

        response = self.client.get(
            self.list_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )


__all__ = [
    "AppointmentAPITestCase",
]

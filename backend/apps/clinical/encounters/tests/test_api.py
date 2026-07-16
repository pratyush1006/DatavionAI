"""
Tests for encounter API endpoints.
"""

from __future__ import annotations

from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from apps.clinical.encounters.constants import EncounterStatus
from apps.clinical.encounters.models import Encounter
from apps.common.tests.base import BaseAPITestCase


class EncounterAPITestCase(BaseAPITestCase):
    """
    Test cases for encounter API endpoints.
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

        self.appointment = self.create_appointment(
            organization=self.organization,
            patient=self.patient,
            provider=self.provider,
        )

        self.encounter = Encounter.objects.create(
            organization=self.organization,
            appointment=self.appointment,
            patient=self.patient,
            provider=self.provider,
            encounter_number="ENC000001",
            status=EncounterStatus.SCHEDULED,
            chief_complaint="Fever",
            started_at=timezone.now(),
            ended_at=timezone.now()
            + timedelta(
                minutes=30,
            ),
            duration_minutes=30,
        )

        self.list_url = reverse(
            "encounters:list-create",
        )

        self.detail_url = reverse(
            "encounters:detail",
            kwargs={
                "encounter_id": self.encounter.id,
            },
        )

    def test_list_encounters(
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

    def test_retrieve_encounter(
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

    def test_create_encounter(
        self,
    ) -> None:
        """
        Create endpoint should create an encounter.
        """

        payload = {
            "organization": str(self.organization.id),
            "appointment": str(
                self.create_appointment(
                    organization=self.organization,
                    patient=self.patient,
                    provider=self.provider,
                    appointment_number="APT000002",
                ).id,
            ),
            "patient": str(self.patient.id),
            "provider": str(self.provider.id),
            "encounter_number": "ENC000002",
            "status": EncounterStatus.SCHEDULED,
            "chief_complaint": "Headache",
            "history_of_present_illness": "Patient complains of headache.",
            "assessment": "Migraine",
            "plan": "Rest and medication",
            "clinical_notes": "Stable condition.",
            "started_at": timezone.now().isoformat(),
            "ended_at": (
                timezone.now()
                + timedelta(
                    minutes=30,
                )
            ).isoformat(),
            "duration_minutes": 30,
            "is_billable": True,
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

    def test_create_encounter_validation_error(
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

    def test_update_encounter(
        self,
    ) -> None:
        """
        PUT endpoint should update the encounter.
        """

        response = self.client.put(
            self.detail_url,
            {
                "organization": str(self.organization.id),
                "appointment": str(self.appointment.id),
                "patient": str(self.patient.id),
                "provider": str(self.provider.id),
                "encounter_number": self.encounter.encounter_number,
                "status": EncounterStatus.COMPLETED,
                "chief_complaint": "Updated Complaint",
                "history_of_present_illness": "Updated HPI",
                "assessment": "Recovered",
                "plan": "Discharge",
                "clinical_notes": "Patient recovered.",
                "started_at": self.encounter.started_at.isoformat(),
                "ended_at": self.encounter.ended_at.isoformat(),
                "duration_minutes": 30,
                "is_billable": True,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_partial_update_encounter(
        self,
    ) -> None:
        """
        PATCH endpoint should update part of the encounter.
        """

        response = self.client.patch(
            self.detail_url,
            {
                "status": EncounterStatus.COMPLETED,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_delete_encounter(
        self,
    ) -> None:
        """
        DELETE endpoint should remove the encounter.
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
    "EncounterAPITestCase",
]

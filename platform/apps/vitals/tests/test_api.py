"""
Tests for vital API endpoints.
"""

from __future__ import annotations

from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from apps.common.tests.base import BaseAPITestCase
from apps.providers.constants import ProviderType
from apps.vitals.constants import (
    TemperatureUnit,
    VitalStatus,
)
from apps.vitals.models import Vital


class VitalAPITestCase(BaseAPITestCase):
    """
    Test cases for vital API endpoints.
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

        self.appointment = self.create_appointment(
            organization=self.organization,
            patient=self.patient,
            provider=self.provider,
            appointment_number="APT000001",
        )

        self.encounter = self.create_encounter(
            organization=self.organization,
            appointment=self.appointment,
            patient=self.patient,
            provider=self.provider,
            encounter_number="ENC000001",
        )
        self.recorded_at = timezone.now()
        self.vital = Vital.objects.create(
            organization=self.organization,
            patient=self.patient,
            provider=self.provider,
            encounter=self.encounter,
            recorded_at=self.recorded_at,
            height_cm="175.00",
            weight_kg="70.00",
            bmi="22.86",
            temperature="98.6",
            temperature_unit=TemperatureUnit.FAHRENHEIT,
            pulse=72,
            respiratory_rate=18,
            systolic_bp=120,
            diastolic_bp=80,
            oxygen_saturation=98,
            pain_score=2,
            status=VitalStatus.FINAL,
            notes="Initial vital record.",
        )

        self.list_url = reverse(
            "vitals:list-create",
        )

        self.detail_url = reverse(
            "vitals:detail",
            kwargs={
                "vital_id": self.vital.id,
            },
        )

    def test_list_vitals(
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
            response.data,
        )

    def test_retrieve_vital(
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

    def test_create_vital(
        self,
    ) -> None:
        """
        Create endpoint should create a vital.
        """

        payload = {
            "organization": str(self.organization.id),
            "patient": str(self.patient.id),
            "provider": str(self.provider.id),
            "encounter": str(self.encounter.id),
            "recorded_at": (self.recorded_at + timedelta(minutes=1)).isoformat(),
            "height_cm": "180.00",
            "weight_kg": "75.00",
            "bmi": "23.15",
            "temperature": "99.1",
            "temperature_unit": TemperatureUnit.FAHRENHEIT,
            "pulse": 75,
            "respiratory_rate": 16,
            "systolic_bp": 118,
            "diastolic_bp": 78,
            "oxygen_saturation": 99,
            "pain_score": 1,
            "status": VitalStatus.FINAL,
            "notes": "Follow-up vital record.",
        }

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            response.data,
        )

    def test_create_vital_validation_error(
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

    def test_update_vital(
        self,
    ) -> None:
        """
        PUT endpoint should update the vital.
        """

        response = self.client.put(
            self.detail_url,
            {
                "organization": str(self.organization.id),
                "patient": str(self.patient.id),
                "provider": str(self.provider.id),
                "encounter": str(self.encounter.id),
                "recorded_at": self.vital.recorded_at.isoformat(),
                "height_cm": "175.00",
                "weight_kg": "70.00",
                "bmi": "22.86",
                "temperature": "98.6",
                "temperature_unit": TemperatureUnit.FAHRENHEIT,
                "pulse": 80,
                "respiratory_rate": 18,
                "systolic_bp": 122,
                "diastolic_bp": 82,
                "oxygen_saturation": 99,
                "pain_score": 1,
                "status": VitalStatus.FINAL,
                "notes": "Updated vital record.",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            response.data,
        )

    def test_partial_update_vital(
        self,
    ) -> None:
        """
        PATCH endpoint should update part of the vital.
        """

        response = self.client.patch(
            self.detail_url,
            {
                "pulse": 85,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            response.data,
        )

    def test_delete_vital(
        self,
    ) -> None:
        """
        DELETE endpoint should remove the vital.
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
    "VitalAPITestCase",
]

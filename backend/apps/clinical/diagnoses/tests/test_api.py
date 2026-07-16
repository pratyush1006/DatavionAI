"""
Tests for diagnosis API endpoints.
"""

from __future__ import annotations

from django.urls import reverse
from rest_framework import status

from apps.clinical.diagnoses.constants import (
    DiagnosisStatus,
    DiagnosisType,
)
from apps.clinical.diagnoses.models import Diagnosis
from apps.common.tests.base import BaseAPITestCase


class DiagnosisAPITestCase(BaseAPITestCase):
    """
    Test cases for diagnosis API endpoints.
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

        self.encounter = self.create_encounter(
            organization=self.organization,
            appointment=self.appointment,
            patient=self.patient,
            provider=self.provider,
        )

        self.diagnosis = Diagnosis.objects.create(
            organization=self.organization,
            encounter=self.encounter,
            diagnosis_code="J10.1",
            diagnosis_description="Influenza with pneumonia",
            diagnosis_type=DiagnosisType.PRIMARY,
            status=DiagnosisStatus.ACTIVE,
            is_primary=True,
            present_on_admission=True,
            notes="Initial diagnosis.",
        )

        self.list_url = reverse(
            "diagnoses:list-create",
        )

        self.detail_url = reverse(
            "diagnoses:detail",
            kwargs={
                "diagnosis_id": self.diagnosis.id,
            },
        )

    def test_list_diagnoses(
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

    def test_retrieve_diagnosis(
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

    def test_create_diagnosis(
        self,
    ) -> None:
        """
        Create endpoint should create a diagnosis.
        """

        payload = {
            "organization": str(self.organization.id),
            "encounter": str(self.encounter.id),
            "diagnosis_code": "R50.9",
            "diagnosis_description": "Fever, unspecified",
            "diagnosis_type": DiagnosisType.SECONDARY,
            "status": DiagnosisStatus.ACTIVE,
            "is_primary": False,
            "present_on_admission": False,
            "notes": "Secondary diagnosis",
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

    def test_create_diagnosis_validation_error(
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

    def test_update_diagnosis(
        self,
    ) -> None:
        """
        PUT endpoint should update the diagnosis.
        """

        response = self.client.put(
            self.detail_url,
            {
                "organization": str(self.organization.id),
                "encounter": str(self.encounter.id),
                "diagnosis_code": "J10.1",
                "diagnosis_description": "Influenza resolved",
                "diagnosis_type": DiagnosisType.PRIMARY,
                "status": DiagnosisStatus.RESOLVED,
                "is_primary": True,
                "present_on_admission": True,
                "notes": "Recovered",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_partial_update_diagnosis(
        self,
    ) -> None:
        """
        PATCH endpoint should update part of the diagnosis.
        """

        response = self.client.patch(
            self.detail_url,
            {
                "status": DiagnosisStatus.INACTIVE,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_delete_diagnosis(
        self,
    ) -> None:
        """
        DELETE endpoint should remove the diagnosis.
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
    "DiagnosisAPITestCase",
]

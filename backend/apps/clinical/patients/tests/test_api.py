"""
API tests for the Patients application.
"""

from __future__ import annotations

from datetime import date

from django.urls import reverse
from rest_framework import status

from apps.clinical.patients.constants import (
    PatientGender,
    PatientStatus,
)
from apps.clinical.patients.models import Patient
from apps.clinical.patients.tests.factories import PatientFactory
from apps.common.tests.base import BaseAPITestCase


class PatientAPITestCase(BaseAPITestCase):
    """
    API tests for patient endpoints.
    """

    def setUp(self) -> None:
        super().setUp()

        self.patient = PatientFactory(
            organization=self.organization,
            mrn="MRN000001",
            first_name="John",
            last_name="Doe",
            date_of_birth=date(
                1995,
                5,
                20,
            ),
            gender=PatientGender.MALE,
        )

        self.list_url = reverse(
            "patients:list-create",
        )

        self.detail_url = reverse(
            "patients:detail",
            kwargs={
                "patient_id": self.patient.pk,
            },
        )

    def test_list_patients(self) -> None:
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

    def test_retrieve_patient(self) -> None:
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

    def test_create_patient(self) -> None:
        """
        Create endpoint should create a patient.
        """

        payload = {
            "organization": str(self.organization.pk),
            "mrn": "MRN000002",
            "first_name": "Jane",
            "last_name": "Smith",
            "date_of_birth": "1998-08-15",
            "gender": PatientGender.FEMALE,
            "status": PatientStatus.ACTIVE,
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

        self.assertTrue(
            Patient.objects.filter(
                mrn="MRN000002",
            ).exists(),
        )

    def test_update_patient(self) -> None:
        """
        PUT should update the patient.
        """

        response = self.client.put(
            self.detail_url,
            {
                "first_name": "Jonathan",
                "last_name": "Doe",
                "date_of_birth": "1995-05-20",
                "gender": PatientGender.MALE,
                "status": PatientStatus.ACTIVE,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.patient.refresh_from_db()

        self.assertEqual(
            self.patient.first_name,
            "Jonathan",
        )

    def test_partial_update_patient(self) -> None:
        """
        PATCH should update selected fields.
        """

        response = self.client.patch(
            self.detail_url,
            {
                "last_name": "Williams",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.patient.refresh_from_db()

        self.assertEqual(
            self.patient.last_name,
            "Williams",
        )

    def test_delete_patient(self) -> None:
        """
        DELETE should remove the patient.
        """

        response = self.client.delete(
            self.detail_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Patient.objects.filter(
                pk=self.patient.pk,
            ).exists(),
        )

    def test_invalid_create_returns_bad_request(self) -> None:
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

    def test_duplicate_mrn_returns_bad_request(self) -> None:
        """
        Duplicate MRN should fail.
        """

        payload = {
            "organization": str(self.organization.pk),
            "mrn": "MRN000001",
            "first_name": "Jane",
            "last_name": "Smith",
            "date_of_birth": "1998-08-15",
            "gender": PatientGender.FEMALE,
        }

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_unknown_patient_returns_not_found(self) -> None:
        """
        Unknown patient should return HTTP 404.
        """

        response = self.client.get(
            reverse(
                "patients:detail",
                kwargs={
                    "patient_id": "00000000-0000-0000-0000-000000000000",
                },
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_requires_authentication(self) -> None:
        """
        API should require authentication.
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

    def test_list_contains_patient(self) -> None:
        """
        Patient should be present in the list response.
        """

        response = self.client.get(
            self.list_url,
        )

        self.assertContains(
            response,
            self.patient.mrn,
            status_code=status.HTTP_200_OK,
        )


__all__ = [
    "PatientAPITestCase",
]

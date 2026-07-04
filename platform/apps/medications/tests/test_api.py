"""
Tests for medication API endpoints.
"""

from __future__ import annotations

from django.urls import reverse
from rest_framework import status

from apps.common.tests.base import BaseAPITestCase
from apps.medications.constants import (
    MedicationDosageForm,
    MedicationRoute,
)
from apps.medications.models import Medication


class MedicationAPITestCase(BaseAPITestCase):
    """
    Test cases for medication API endpoints.
    """

    def setUp(
        self,
    ) -> None:
        """
        Set up test data.
        """

        super().setUp()

        self.medication = Medication.objects.create(
            organization=self.organization,
            medication_code="MED000001",
            generic_name="Paracetamol",
            brand_name="Crocin",
            strength="500",
            strength_unit="mg",
            dosage_form=MedicationDosageForm.TABLET,
            route=MedicationRoute.ORAL,
            manufacturer="ABC Pharma",
            description="Pain reliever and fever reducer.",
            is_controlled=False,
        )

        self.list_url = reverse(
            "medications:list-create",
        )

        self.detail_url = reverse(
            "medications:detail",
            kwargs={
                "medication_id": self.medication.id,
            },
        )

    def test_list_medications(
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

    def test_retrieve_medication(
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

    def test_create_medication(
        self,
    ) -> None:
        """
        Create endpoint should create a medication.
        """

        payload = {
            "organization": str(self.organization.id),
            "medication_code": "MED000002",
            "generic_name": "Metformin",
            "brand_name": "Glycomet",
            "strength": "500",
            "strength_unit": "mg",
            "dosage_form": MedicationDosageForm.TABLET,
            "route": MedicationRoute.ORAL,
            "manufacturer": "XYZ Pharma",
            "description": "Antidiabetic medication.",
            "is_controlled": False,
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

    def test_create_medication_validation_error(
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

    def test_update_medication(
        self,
    ) -> None:
        """
        PUT endpoint should update the medication.
        """

        response = self.client.put(
            self.detail_url,
            {
                "organization": str(self.organization.id),
                "medication_code": "MED000001",
                "generic_name": "Paracetamol",
                "brand_name": "Dolo 650",
                "strength": "650",
                "strength_unit": "mg",
                "dosage_form": MedicationDosageForm.TABLET,
                "route": MedicationRoute.ORAL,
                "manufacturer": "Micro Labs",
                "description": "Updated medication.",
                "is_controlled": False,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_partial_update_medication(
        self,
    ) -> None:
        """
        PATCH endpoint should update part of the medication.
        """

        response = self.client.patch(
            self.detail_url,
            {
                "manufacturer": "Sun Pharma",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_delete_medication(
        self,
    ) -> None:
        """
        DELETE endpoint should remove the medication.
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
    "MedicationAPITestCase",
]

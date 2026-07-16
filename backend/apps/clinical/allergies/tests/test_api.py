"""
Tests for allergy API endpoints.
"""

from __future__ import annotations

from datetime import date

from django.urls import reverse
from rest_framework import status

from apps.clinical.allergies.constants import (
    AllergyCategory,
    AllergySeverity,
    AllergyStatus,
)
from apps.clinical.allergies.models import Allergy
from apps.clinical.providers.constants import ProviderType
from apps.common.tests.base import BaseAPITestCase


class AllergyAPITestCase(BaseAPITestCase):
    """
    Test cases for allergy API endpoints.
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

        self.allergy = Allergy.objects.create(
            organization=self.organization,
            patient=self.patient,
            provider=self.provider,
            encounter=self.encounter,
            allergen="Penicillin",
            category=AllergyCategory.MEDICATION,
            severity=AllergySeverity.SEVERE,
            status=AllergyStatus.ACTIVE,
            reaction="Skin rash",
            onset_date=date.today(),
            notes="Initial allergy.",
        )

        self.list_url = reverse(
            "allergies:list-create",
        )

        self.detail_url = reverse(
            "allergies:detail",
            kwargs={
                "allergy_id": self.allergy.id,
            },
        )

    def test_list_allergies(
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

    def test_retrieve_allergy(
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

    def test_create_allergy(
        self,
    ) -> None:
        """
        Create endpoint should create an allergy.
        """

        payload = {
            "organization": str(self.organization.id),
            "patient": str(self.patient.id),
            "provider": str(self.provider.id),
            "encounter": str(self.encounter.id),
            "allergen": "Peanuts",
            "category": AllergyCategory.FOOD,
            "severity": AllergySeverity.MODERATE,
            "status": AllergyStatus.ACTIVE,
            "reaction": "Hives",
            "onset_date": date.today().isoformat(),
            "notes": "Food allergy.",
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

    def test_create_allergy_validation_error(
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

    def test_update_allergy(
        self,
    ) -> None:
        """
        PUT endpoint should update the allergy.
        """

        response = self.client.put(
            self.detail_url,
            {
                "organization": str(self.organization.id),
                "patient": str(self.patient.id),
                "provider": str(self.provider.id),
                "encounter": str(self.encounter.id),
                "allergen": "Penicillin",
                "category": AllergyCategory.MEDICATION,
                "severity": AllergySeverity.LIFE_THREATENING,
                "status": AllergyStatus.ACTIVE,
                "reaction": "Anaphylaxis",
                "onset_date": self.allergy.onset_date.isoformat(),
                "resolved_date": None,
                "notes": "Requires emergency treatment.",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_partial_update_allergy(
        self,
    ) -> None:
        """
        PATCH endpoint should update part of the allergy.
        """

        response = self.client.patch(
            self.detail_url,
            {
                "status": AllergyStatus.RESOLVED,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_delete_allergy(
        self,
    ) -> None:
        """
        DELETE endpoint should remove the allergy.
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
    "AllergyAPITestCase",
]

"""
Tests for the Allergy model.
"""

from __future__ import annotations

from datetime import date

from apps.allergies.constants import (
    DEFAULT_ALLERGY_CATEGORY,
    DEFAULT_ALLERGY_SEVERITY,
    DEFAULT_ALLERGY_STATUS,
    AllergyCategory,
    AllergySeverity,
    AllergyStatus,
)
from apps.allergies.models import Allergy
from apps.common.tests.base import BaseTestCase
from apps.providers.constants import ProviderType


class AllergyModelTestCase(BaseTestCase):
    """
    Test cases for the Allergy model.
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
            resolved_date=None,
            notes="Patient developed rash after medication.",
        )

    def test_str(
        self,
    ) -> None:
        """
        String representation should be correct.
        """

        self.assertEqual(
            str(self.allergy),
            self.allergy.title,
        )

    def test_title_property(
        self,
    ) -> None:
        """
        Title property should return a readable title.
        """

        self.assertEqual(
            self.allergy.title,
            "Penicillin | Severe",
        )

    def test_defaults(
        self,
    ) -> None:
        """
        Default values should be assigned.
        """

        allergy = Allergy.objects.create(
            organization=self.organization,
            patient=self.patient,
            provider=self.provider,
            encounter=self.encounter,
            allergen="Peanuts",
        )

        self.assertEqual(
            allergy.category,
            DEFAULT_ALLERGY_CATEGORY,
        )

        self.assertEqual(
            allergy.severity,
            DEFAULT_ALLERGY_SEVERITY,
        )

        self.assertEqual(
            allergy.status,
            DEFAULT_ALLERGY_STATUS,
        )

        self.assertEqual(
            allergy.reaction,
            "",
        )

        self.assertIsNone(
            allergy.onset_date,
        )

        self.assertIsNone(
            allergy.resolved_date,
        )

        self.assertEqual(
            allergy.notes,
            "",
        )


__all__ = [
    "AllergyModelTestCase",
]

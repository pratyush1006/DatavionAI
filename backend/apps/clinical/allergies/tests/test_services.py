"""
Tests for allergy services.
"""

from __future__ import annotations

from datetime import date

from apps.clinical.allergies.constants import (
    AllergyCategory,
    AllergySeverity,
    AllergyStatus,
)
from apps.clinical.allergies.models import Allergy
from apps.clinical.allergies.services import (
    create_allergy,
    delete_allergy,
    update_allergy,
)
from apps.clinical.providers.constants import ProviderType
from apps.common.tests.base import BaseTestCase


class AllergyServiceTestCase(BaseTestCase):
    """
    Test cases for allergy services.
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

    def test_create_allergy(
        self,
    ) -> None:
        """
        Allergy should be created successfully.
        """

        allergy = create_allergy(
            validated_data={
                "organization": self.organization,
                "patient": self.patient,
                "provider": self.provider,
                "encounter": self.encounter,
                "allergen": "Peanuts",
                "category": AllergyCategory.FOOD,
                "severity": AllergySeverity.MODERATE,
                "status": AllergyStatus.ACTIVE,
                "reaction": "Hives",
                "onset_date": date.today(),
                "notes": "Food allergy.",
            },
        )

        self.assertIsInstance(
            allergy,
            Allergy,
        )

        self.assertEqual(
            allergy.allergen,
            "Peanuts",
        )

        self.assertEqual(
            allergy.patient,
            self.patient,
        )

        self.assertEqual(
            allergy.category,
            AllergyCategory.FOOD,
        )

    def test_update_allergy(
        self,
    ) -> None:
        """
        Allergy should be updated successfully.
        """

        updated = update_allergy(
            instance=self.allergy,
            validated_data={
                "severity": AllergySeverity.LIFE_THREATENING,
                "reaction": "Anaphylaxis",
                "notes": "Requires EpiPen.",
            },
        )

        updated.refresh_from_db()

        self.assertEqual(
            updated.severity,
            AllergySeverity.LIFE_THREATENING,
        )

        self.assertEqual(
            updated.reaction,
            "Anaphylaxis",
        )

        self.assertEqual(
            updated.notes,
            "Requires EpiPen.",
        )

    def test_delete_allergy(
        self,
    ) -> None:
        """
        Allergy should be deleted successfully.
        """

        allergy_id = self.allergy.id

        delete_allergy(
            instance=self.allergy,
        )

        self.assertFalse(
            Allergy.objects.filter(
                id=allergy_id,
            ).exists(),
        )

    def test_update_returns_same_instance(
        self,
    ) -> None:
        """
        Update service should return the same instance.
        """

        updated = update_allergy(
            instance=self.allergy,
            validated_data={
                "status": AllergyStatus.RESOLVED,
            },
        )

        self.assertEqual(
            updated.pk,
            self.allergy.pk,
        )

        self.assertEqual(
            updated.status,
            AllergyStatus.RESOLVED,
        )

    def test_create_persists_to_database(
        self,
    ) -> None:
        """
        Allergy should persist after creation.
        """

        initial_count = Allergy.objects.count()

        create_allergy(
            validated_data={
                "organization": self.organization,
                "patient": self.patient,
                "provider": self.provider,
                "encounter": self.encounter,
                "allergen": "Latex",
                "category": AllergyCategory.LATEX,
            },
        )

        self.assertEqual(
            Allergy.objects.count(),
            initial_count + 1,
        )


__all__ = [
    "AllergyServiceTestCase",
]

"""
Tests for medication services.
"""

from __future__ import annotations

from apps.common.tests.base import BaseTestCase
from apps.medications.constants import (
    MedicationDosageForm,
    MedicationRoute,
)
from apps.medications.models import Medication
from apps.medications.services import (
    create_medication,
    delete_medication,
    update_medication,
)


class MedicationServiceTestCase(BaseTestCase):
    """
    Test cases for medication services.
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

    def test_create_medication(
        self,
    ) -> None:
        """
        Medication should be created successfully.
        """

        medication = create_medication(
            validated_data={
                "organization": self.organization,
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
            },
        )

        self.assertIsInstance(
            medication,
            Medication,
        )

        self.assertEqual(
            medication.medication_code,
            "MED000002",
        )

        self.assertEqual(
            medication.generic_name,
            "Metformin",
        )

    def test_update_medication(
        self,
    ) -> None:
        """
        Medication should be updated successfully.
        """

        updated = update_medication(
            instance=self.medication,
            validated_data={
                "brand_name": "Dolo",
                "manufacturer": "Micro Labs",
                "is_controlled": True,
            },
        )

        updated.refresh_from_db()

        self.assertEqual(
            updated.brand_name,
            "Dolo",
        )

        self.assertEqual(
            updated.manufacturer,
            "Micro Labs",
        )

        self.assertTrue(
            updated.is_controlled,
        )

    def test_delete_medication(
        self,
    ) -> None:
        """
        Medication should be deleted successfully.
        """

        medication_id = self.medication.id

        delete_medication(
            instance=self.medication,
        )

        self.assertFalse(
            Medication.objects.filter(
                id=medication_id,
            ).exists(),
        )

    def test_update_returns_same_instance(
        self,
    ) -> None:
        """
        Update service should return the same instance.
        """

        updated = update_medication(
            instance=self.medication,
            validated_data={
                "manufacturer": "Sun Pharma",
            },
        )

        self.assertEqual(
            updated.pk,
            self.medication.pk,
        )

        self.assertEqual(
            updated.manufacturer,
            "Sun Pharma",
        )

    def test_create_persists_to_database(
        self,
    ) -> None:
        """
        Medication should persist after creation.
        """

        initial_count = Medication.objects.count()

        create_medication(
            validated_data={
                "organization": self.organization,
                "medication_code": "MED000003",
                "generic_name": "Amoxicillin",
                "strength": "250",
                "strength_unit": "mg",
                "dosage_form": MedicationDosageForm.CAPSULE,
                "route": MedicationRoute.ORAL,
            },
        )

        self.assertEqual(
            Medication.objects.count(),
            initial_count + 1,
        )


__all__ = [
    "MedicationServiceTestCase",
]

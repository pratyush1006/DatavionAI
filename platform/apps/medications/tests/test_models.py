"""
Tests for the Medication model.
"""

from __future__ import annotations

from apps.common.tests.base import BaseTestCase
from apps.medications.constants import (
    DEFAULT_DOSAGE_FORM,
    DEFAULT_ROUTE,
    MedicationDosageForm,
    MedicationRoute,
)
from apps.medications.models import Medication


class MedicationModelTestCase(BaseTestCase):
    """
    Test cases for the Medication model.
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

    def test_str(
        self,
    ) -> None:
        """
        String representation should be correct.
        """

        self.assertEqual(
            str(self.medication),
            (
                f"{self.medication.medication_code} | "
                f"{self.medication.title}"
            ),
        )

    def test_title_property(
        self,
    ) -> None:
        """
        Title property should return a readable title.
        """

        self.assertEqual(
            self.medication.title,
            "Paracetamol 500mg (Crocin)",
        )

    def test_defaults(
        self,
    ) -> None:
        """
        Default values should be assigned.
        """

        medication = Medication.objects.create(
            organization=self.organization,
            medication_code="MED000002",
            generic_name="Metformin",
            strength="500",
            strength_unit="mg",
        )

        self.assertEqual(
            medication.dosage_form,
            DEFAULT_DOSAGE_FORM,
        )

        self.assertEqual(
            medication.route,
            DEFAULT_ROUTE,
        )

        self.assertFalse(
            medication.is_controlled,
        )

        self.assertEqual(
            medication.brand_name,
            "",
        )

        self.assertEqual(
            medication.manufacturer,
            "",
        )

        self.assertEqual(
            medication.description,
            "",
        )


__all__ = [
    "MedicationModelTestCase",
]

"""
Tests for the Patient model.
"""

from __future__ import annotations

from datetime import date

from django.core.exceptions import ValidationError

from apps.clinical.patients.constants import (
    DEFAULT_PATIENT_STATUS,
    BloodGroup,
    PatientGender,
)
from apps.clinical.patients.models import Patient
from apps.common.tests.base import BaseTestCase


class PatientModelTestCase(BaseTestCase):
    """
    Test cases for the Patient model.
    """

    def setUp(self) -> None:
        super().setUp()

        self.patient = Patient.objects.create(
            organization=self.organization,
            mrn="MRN000001",
            first_name="John",
            last_name="Doe",
            date_of_birth=date(1995, 5, 20),
            gender=PatientGender.MALE,
        )

    def test_patient_creation(self) -> None:
        """
        Patient should be created successfully.
        """

        self.assertEqual(
            self.patient.organization,
            self.organization,
        )

        self.assertEqual(
            self.patient.mrn,
            "MRN000001",
        )

        self.assertEqual(
            self.patient.first_name,
            "John",
        )

        self.assertEqual(
            self.patient.last_name,
            "Doe",
        )

    def test_string_representation(self) -> None:
        """
        __str__ should return the patient display name.
        """

        self.assertEqual(
            str(self.patient),
            "John Doe (MRN000001)",
        )

    def test_default_status(self) -> None:
        """
        Default patient status should be applied.
        """

        self.assertEqual(
            self.patient.status,
            DEFAULT_PATIENT_STATUS,
        )

    def test_default_country(self) -> None:
        """
        Default country should be India.
        """

        self.assertEqual(
            self.patient.country,
            "India",
        )

    def test_optional_fields_default_to_blank(self) -> None:
        """
        Optional fields should default to blank.
        """

        self.assertEqual(
            self.patient.middle_name,
            "",
        )

        self.assertEqual(
            self.patient.preferred_name,
            "",
        )

        self.assertEqual(
            self.patient.phone,
            "",
        )

        self.assertEqual(
            self.patient.email,
            "",
        )

    def test_blood_group_can_be_updated(self) -> None:
        """
        Blood group should be assignable.
        """

        self.patient.blood_group = BloodGroup.O_POSITIVE
        self.patient.save()

        self.patient.refresh_from_db()

        self.assertEqual(
            self.patient.blood_group,
            BloodGroup.O_POSITIVE,
        )

    def test_phone_validator(self) -> None:
        """
        Invalid phone numbers should fail validation.
        """

        self.patient.phone = "123"

        with self.assertRaises(
            ValidationError,
        ):
            self.patient.full_clean()

    def test_meta_ordering(self) -> None:
        """
        Patient model should use the configured ordering.
        """

        self.assertEqual(
            Patient._meta.ordering,
            (
                "first_name",
                "last_name",
            ),
        )

    def test_meta_table_name(self) -> None:
        """
        Patient model should use the configured database table.
        """

        self.assertEqual(
            Patient._meta.db_table,
            "patients",
        )

    def test_foreign_key_relationship(self) -> None:
        """
        Patient should belong to the configured organization.
        """

        self.assertEqual(
            self.patient.organization.id,
            self.organization.id,
        )


__all__ = [
    "PatientModelTestCase",
]

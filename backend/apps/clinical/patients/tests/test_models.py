"""
Tests for the Patient model.
"""

from __future__ import annotations

from datetime import date

from django.core.exceptions import ValidationError
from django.db import IntegrityError

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

    def test_full_name_property(self) -> None:
        """
        full_name should return the legal patient name.
        """

        self.assertEqual(
            self.patient.full_name,
            "John Doe",
        )

    def test_display_name_defaults_to_full_name(self) -> None:
        """
        display_name should fall back to full_name.
        """

        self.assertEqual(
            self.patient.display_name,
            "John Doe",
        )

    def test_display_name_uses_preferred_name(self) -> None:
        """
        display_name should use the preferred name when provided.
        """

        self.patient.preferred_name = "Johnny"

        self.assertEqual(
            self.patient.display_name,
            "Johnny",
        )

    def test_age_property(self) -> None:
        """
        Age should be calculated correctly.
        """

        self.assertGreaterEqual(
            self.patient.age,
            0,
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

    def test_unique_mrn_per_organization(self) -> None:
        """
        MRN should be unique within an organization.
        """

        with self.assertRaises(
            IntegrityError,
        ):
            Patient.objects.create(
                organization=self.organization,
                mrn="MRN000001",
                first_name="Jane",
                last_name="Doe",
                date_of_birth=date(1990, 1, 1),
                gender=PatientGender.FEMALE,
            )

    def test_meta_ordering(self) -> None:
        """
        Patient model should use the configured ordering.
        """

        self.assertEqual(
            Patient._meta.ordering,
            (
                "last_name",
                "first_name",
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
            self.patient.organization,
            self.organization,
        )


__all__ = [
    "PatientModelTestCase",
]

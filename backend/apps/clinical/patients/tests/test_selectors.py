"""
Tests for patient selectors.
"""

from __future__ import annotations

from datetime import date

from apps.clinical.patients.constants import (
    PatientGender,
    PatientStatus,
)
from apps.clinical.patients.selectors import PatientSelector
from apps.clinical.patients.tests.factories import PatientFactory
from apps.common.tests.base import BaseTestCase


class PatientSelectorTestCase(BaseTestCase):
    """
    Test cases for PatientSelector.
    """

    def setUp(self) -> None:
        super().setUp()

        self.active_patient = PatientFactory(
            organization=self.organization,
            mrn="MRN000001",
            first_name="John",
            last_name="Doe",
            gender=PatientGender.MALE,
            status=PatientStatus.ACTIVE,
            date_of_birth=date(
                1995,
                5,
                20,
            ),
        )

        self.inactive_patient = PatientFactory(
            organization=self.organization,
            mrn="MRN000002",
            first_name="Jane",
            last_name="Smith",
            gender=PatientGender.FEMALE,
            status=PatientStatus.INACTIVE,
            date_of_birth=date(
                1994,
                2,
                10,
            ),
        )

    def test_queryset(self) -> None:
        """
        queryset() should return a queryset.
        """

        queryset = PatientSelector.queryset()

        self.assertIn(
            self.active_patient,
            queryset,
        )

    def test_get(self) -> None:
        """
        get() should return the requested patient.
        """

        patient = PatientSelector.get(
            patient_id=self.active_patient.id,
        )

        self.assertEqual(
            patient,
            self.active_patient,
        )

    def test_get_by_mrn(self) -> None:
        """
        get_by_mrn() should return the correct patient.
        """

        patient = PatientSelector.get_by_mrn(
            organization=self.organization,
            mrn="MRN000001",
        )

        self.assertEqual(
            patient,
            self.active_patient,
        )

    def test_list(self) -> None:
        """
        list() should return all patients.
        """

        patients = PatientSelector.list()

        self.assertEqual(
            patients.count(),
            2,
        )

    def test_list_by_organization(self) -> None:
        """
        list_by_organization() should filter by organization.
        """

        patients = PatientSelector.list_by_organization(
            organization=self.organization,
        )

        self.assertEqual(
            patients.count(),
            2,
        )

    def test_list_active(self) -> None:
        """
        list_active() should return active patients.
        """

        patients = PatientSelector.list_active(
            organization=self.organization,
        )

        self.assertEqual(
            patients.count(),
            1,
        )

        self.assertEqual(
            patients.first(),
            self.active_patient,
        )

    def test_list_inactive(self) -> None:
        """
        list_inactive() should return inactive patients.
        """

        patients = PatientSelector.list_inactive(
            organization=self.organization,
        )

        self.assertEqual(
            patients.count(),
            1,
        )

        self.assertEqual(
            patients.first(),
            self.inactive_patient,
        )

    def test_exists(self) -> None:
        """
        exists() should return True for existing patient.
        """

        self.assertTrue(
            PatientSelector.exists(
                organization=self.organization,
                patient_id=self.active_patient.id,
            ),
        )

    def test_count(self) -> None:
        """
        count() should return the patient count.
        """

        self.assertEqual(
            PatientSelector.count(
                organization=self.organization,
            ),
            2,
        )

    def test_search(self) -> None:
        """
        search() should find matching patients.
        """

        patients = PatientSelector.search(
            organization=self.organization,
            query="John",
        )

        self.assertEqual(
            patients.count(),
            1,
        )

        self.assertEqual(
            patients.first(),
            self.active_patient,
        )


__all__ = [
    "PatientSelectorTestCase",
]

"""
Tests for PatientDocument model.
"""

from __future__ import annotations

from django.test import TestCase

from apps.organizations.tests.factories import (
    create_organization,
)
from apps.patient_management.patients.tests.factories import (
    create_patient,
)

from .factories import (
    create_patient_document,
)


class PatientDocumentModelTestCase(
    TestCase,
):
    """
    Tests for PatientDocument.
    """

    def setUp(
        self,
    ):
        self.organization = create_organization()

        self.patient = create_patient(
            organization=self.organization,
        )

    def test_create_document(
        self,
    ):
        """
        Should create a patient document.
        """

        document = create_patient_document(
            organization=self.organization,
            patient=self.patient,
        )

        self.assertEqual(
            document.title,
            "Laboratory Report",
        )

    def test_string_representation(
        self,
    ):
        """
        Test __str__.
        """

        document = create_patient_document(
            organization=self.organization,
            patient=self.patient,
        )

        self.assertTrue(
            str(document),
        )

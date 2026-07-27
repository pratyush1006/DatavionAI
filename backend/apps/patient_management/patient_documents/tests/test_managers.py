"""
Tests for PatientDocument managers.
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


class PatientDocumentManagerTestCase(
    TestCase,
):
    """
    Tests for custom manager.
    """

    def setUp(
        self,
    ):
        self.organization = create_organization()

        self.patient = create_patient(
            organization=self.organization,
        )

    def test_active_documents(
        self,
    ):
        """
        Active manager should return active documents.
        """

        create_patient_document(
            organization=self.organization,
            patient=self.patient,
        )

        self.assertEqual(
            1,
            create_patient_document.objects.active().count(),
        )

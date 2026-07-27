"""
Tests for Patient Document services.
"""

from __future__ import annotations

from django.test import TestCase

from apps.organizations.tests.factories import (
    create_organization,
)
from apps.patient_management.patient_documents.services import (
    archive_patient_document,
    update_patient_document,
)
from apps.patient_management.patients.tests.factories import (
    create_patient,
)

from .factories import (
    create_patient_document,
)


class PatientDocumentServiceTestCase(TestCase):
    """
    Tests for Patient Document services.
    """

    def setUp(self) -> None:
        self.organization = create_organization()

        self.patient = create_patient(
            organization=self.organization,
        )

        self.document = create_patient_document(
            organization=self.organization,
            patient=self.patient,
        )

    def test_update_patient_document(self) -> None:
        """
        Should update document title.
        """

        document = update_patient_document(
            document=self.document,
            title="Updated Report",
        )

        self.assertEqual(
            document.title,
            "Updated Report",
        )

    def test_archive_patient_document(self) -> None:
        """
        Should archive a document.
        """

        document = archive_patient_document(
            document=self.document,
        )

        self.assertEqual(
            document.status,
            "ARCHIVED",
        )

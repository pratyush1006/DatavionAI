"""
Tests for Patient Document selectors.
"""

from __future__ import annotations

from django.test import TestCase

from apps.organizations.tests.factories import (
    create_organization,
)
from apps.patient_management.patient_documents.selectors import (
    count_patient_documents,
    get_patient_document_by_id,
    list_patient_documents_by_patient,
)
from apps.patient_management.patients.tests.factories import (
    create_patient,
)

from .factories import (
    create_patient_document,
)


class PatientDocumentSelectorTestCase(TestCase):
    """
    Tests for Patient Document selectors.
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

    def test_get_patient_document_by_id(self) -> None:
        """
        Should return a document by id.
        """

        document = get_patient_document_by_id(
            self.document.id,
        )

        self.assertEqual(
            document.id,
            self.document.id,
        )

    def test_list_patient_documents_by_patient(self) -> None:
        """
        Should list patient documents.
        """

        queryset = list_patient_documents_by_patient(
            self.patient,
        )

        self.assertEqual(
            queryset.count(),
            1,
        )

    def test_count_patient_documents(self) -> None:
        """
        Should count patient documents.
        """

        count = count_patient_documents(
            patient=self.patient,
        )

        self.assertEqual(
            count,
            1,
        )

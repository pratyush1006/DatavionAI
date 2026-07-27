"""
Tests for Patient Document serializers.
"""

from __future__ import annotations

from django.test import TestCase

from apps.organizations.tests.factories import (
    create_organization,
)
from apps.patient_management.patient_documents.api.serializers import (
    PatientDocumentCreateSerializer,
    PatientDocumentDetailSerializer,
    PatientDocumentListSerializer,
    PatientDocumentUpdateSerializer,
)
from apps.patient_management.patients.tests.factories import (
    create_patient,
)

from .factories import (
    create_patient_document,
)


class PatientDocumentSerializerTestCase(TestCase):
    """
    Tests for Patient Document serializers.
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

    def test_list_serializer(self) -> None:
        serializer = PatientDocumentListSerializer(
            self.document,
        )

        self.assertEqual(
            serializer.data["title"],
            self.document.title,
        )

    def test_detail_serializer(self) -> None:
        serializer = PatientDocumentDetailSerializer(
            self.document,
        )

        self.assertEqual(
            serializer.data["document_number"],
            self.document.document_number,
        )

    def test_update_serializer(self) -> None:
        serializer = PatientDocumentUpdateSerializer(
            instance=self.document,
            data={
                "title": "Updated Document",
            },
            partial=True,
        )

        self.assertTrue(
            serializer.is_valid(),
        )

    def test_create_serializer_validation(self) -> None:
        serializer = PatientDocumentCreateSerializer(
            data={
                "organization": self.organization.id,
                "patient": self.patient.id,
                "document_number": "DOC-100",
                "title": "Prescription",
                "category": "PRESCRIPTION",
                "source": "MANUAL",
                "visibility": "PRIVATE",
                "storage_backend": "LOCAL",
            },
        )

        self.assertTrue(
            serializer.is_valid(),
        )

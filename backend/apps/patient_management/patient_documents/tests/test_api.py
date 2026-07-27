"""
API tests for Patient Documents.
"""

from __future__ import annotations

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.tests.factories import (
    create_user,
)
from apps.organizations.tests.factories import (
    create_organization,
)
from apps.patient_management.patients.tests.factories import (
    create_patient,
)

from .factories import (
    create_patient_document,
)


class PatientDocumentAPITestCase(APITestCase):
    """
    API tests for Patient Documents.
    """

    def setUp(self) -> None:
        self.organization = create_organization()

        self.user = create_user(
            organization=self.organization,
        )

        self.patient = create_patient(
            organization=self.organization,
        )

        self.document = create_patient_document(
            organization=self.organization,
            patient=self.patient,
        )

        self.client.force_authenticate(
            self.user,
        )

    def test_list_documents(self) -> None:
        """
        Should list documents.
        """

        response = self.client.get(
            reverse(
                "patient-documents:patient-document-api:list",
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_retrieve_document(self) -> None:
        """
        Should retrieve a document.
        """

        response = self.client.get(
            reverse(
                "patient-documents:patient-document-api:detail",
                kwargs={
                    "id": self.document.id,
                },
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_create_document(self) -> None:
        """
        Should create a document.
        """

        payload = {
            "organization": str(self.organization.id),
            "patient": str(self.patient.id),
            "document_number": "DOC-1000",
            "title": "Radiology Report",
            "description": "Chest X-Ray",
            "category": "RADIOLOGY",
            "source": "MANUAL",
            "visibility": "PRIVATE",
            "storage_backend": "LOCAL",
            "tags": [],
        }

        response = self.client.post(
            reverse(
                "patient-documents:patient-document-api:create",
            ),
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_update_document(self) -> None:
        """
        Should update a document.
        """

        response = self.client.patch(
            reverse(
                "patient-documents:patient-document-api:update",
                kwargs={
                    "id": self.document.id,
                },
            ),
            {
                "title": "Updated Report",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_delete_document(self) -> None:
        """
        Should delete a document.
        """

        response = self.client.delete(
            reverse(
                "patient-documents:patient-document-api:delete",
                kwargs={
                    "id": self.document.id,
                },
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

    def test_filter_by_category(self) -> None:
        """
        Should filter documents by category.
        """

        response = self.client.get(
            reverse(
                "patient-documents:patient-document-api:list",
            ),
            {
                "category": "LABORATORY",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_authentication_required(self) -> None:
        """
        Authentication should be required.
        """

        self.client.force_authenticate(
            user=None,
        )

        response = self.client.get(
            reverse(
                "patient-documents:patient-document-api:list",
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

"""
Tests for Patient Document permissions.
"""

from __future__ import annotations

from django.test import SimpleTestCase

from apps.patient_management.patient_documents.permissions import (
    PatientDocumentPermission,
)


class PatientDocumentPermissionTestCase(
    SimpleTestCase,
):
    """
    Tests for permission constants.
    """

    def test_permission_constants(self) -> None:
        self.assertEqual(
            PatientDocumentPermission.VIEW,
            "patient_documents.view",
        )

        self.assertEqual(
            PatientDocumentPermission.CREATE,
            "patient_documents.create",
        )

        self.assertEqual(
            PatientDocumentPermission.UPDATE,
            "patient_documents.update",
        )

        self.assertEqual(
            PatientDocumentPermission.DELETE,
            "patient_documents.delete",
        )

    def test_all_permissions(self) -> None:
        self.assertIn(
            PatientDocumentPermission.VIEW,
            PatientDocumentPermission.ALL,
        )

        self.assertIn(
            PatientDocumentPermission.CREATE,
            PatientDocumentPermission.ALL,
        )

        self.assertIn(
            PatientDocumentPermission.DELETE,
            PatientDocumentPermission.ALL,
        )

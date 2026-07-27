"""
Tests for patient permissions.
"""

from __future__ import annotations

from apps.clinical.patients.permissions import (
    CanCreatePatient,
    CanDeletePatient,
    CanUpdatePatient,
    CanViewPatient,
    PatientPermission,
)
from apps.common.tests.base import BaseTestCase


class PatientPermissionTestCase(BaseTestCase):
    """
    Test cases for patient permissions.
    """

    def test_permission_constants(self) -> None:
        """
        Permission constants should match the expected values.
        """

        self.assertEqual(
            PatientPermission.VIEW,
            "patient.view",
        )

        self.assertEqual(
            PatientPermission.CREATE,
            "patient.create",
        )

        self.assertEqual(
            PatientPermission.UPDATE,
            "patient.update",
        )

        self.assertEqual(
            PatientPermission.DELETE,
            "patient.delete",
        )

    def test_view_permission_code(self) -> None:
        """
        View permission should expose the correct permission code.
        """

        self.assertEqual(
            CanViewPatient.permission_code,
            PatientPermission.VIEW,
        )

    def test_create_permission_code(self) -> None:
        """
        Create permission should expose the correct permission code.
        """

        self.assertEqual(
            CanCreatePatient.permission_code,
            PatientPermission.CREATE,
        )

    def test_update_permission_code(self) -> None:
        """
        Update permission should expose the correct permission code.
        """

        self.assertEqual(
            CanUpdatePatient.permission_code,
            PatientPermission.UPDATE,
        )

    def test_delete_permission_code(self) -> None:
        """
        Delete permission should expose the correct permission code.
        """

        self.assertEqual(
            CanDeletePatient.permission_code,
            PatientPermission.DELETE,
        )


__all__ = [
    "PatientPermissionTestCase",
]

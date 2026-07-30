"""
Model tests for the Master Patient Index.
"""

from __future__ import annotations

from django.test import TestCase

from apps.patient_management.mpi.tests.factories import (
    MasterPatientIndexFactory,
)


class MasterPatientIndexModelTestCase(TestCase):
    """Tests for MasterPatientIndex."""

    def test_create_mpi_record(
        self,
    ) -> None:
        mpi = MasterPatientIndexFactory()

        self.assertIsNotNone(
            mpi.pk,
        )

    def test_string_representation(
        self,
    ) -> None:
        mpi = MasterPatientIndexFactory()

        self.assertEqual(
            str(mpi),
            mpi.mpi_id,
        )

"""
Selector tests for the Master Patient Index.
"""

from __future__ import annotations

from django.test import TestCase

from apps.patient_management.mpi.selectors import (
    get_mpi_by_id,
)
from apps.patient_management.mpi.tests.factories import (
    MasterPatientIndexFactory,
)


class MasterPatientIndexSelectorTestCase(TestCase):
    """Tests for MPI selectors."""

    def test_get_mpi_by_id(
        self,
    ) -> None:
        mpi = MasterPatientIndexFactory()

        self.assertEqual(
            get_mpi_by_id(
                mpi.pk,
            ),
            mpi,
        )

"""
Service tests for the Master Patient Index.
"""

from __future__ import annotations

from apps.patient_management.mpi.services import (
    create_mpi_record,
)
from apps.patient_management.mpi.tests.factories import (
    MasterPatientIndexFactory,
)
from django.test import TestCase


class MasterPatientIndexServiceTestCase(TestCase):
    """Tests for MPI services."""

    def test_create_mpi_record(
        self,
    ) -> None:
        mpi = MasterPatientIndexFactory.build()

        created = create_mpi_record(
            organization=mpi.organization,
            patient=mpi.patient,
            mpi_id=mpi.mpi_id,
            abha_number=mpi.abha_number,
            aadhaar_number=mpi.aadhaar_number,
            passport_number=mpi.passport_number,
            status=mpi.status,
            verification_status=mpi.verification_status,
            record_source=mpi.record_source,
            match_confidence=mpi.match_confidence,
            merge_status=mpi.merge_status,
            merged_into=mpi.merged_into,
            notes=mpi.notes,
        )

        self.assertIsNotNone(
            created.pk,
        )

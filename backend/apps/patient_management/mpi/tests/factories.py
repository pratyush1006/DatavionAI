"""
Factories for the Master Patient Index module.
"""

from __future__ import annotations

import factory
from apps.patient_management.mpi.constants import (
    MPIMatchConfidence,
    MPIMergeStatus,
    MPIRecordSource,
    MPIStatus,
    MPIVerificationStatus,
)
from apps.patient_management.mpi.models import (
    MasterPatientIndex,
)


class MasterPatientIndexFactory(factory.django.DjangoModelFactory):
    """Factory for MasterPatientIndex."""

    class Meta:
        model = MasterPatientIndex

    organization = factory.SubFactory(
        "apps.organizations.tests.factories.OrganizationFactory",
    )

    patient = factory.SubFactory(
        "apps.patient_management.patients.tests.factories.PatientFactory",
    )

    mpi_id = factory.Sequence(
        lambda n: f"MPI-{n:010d}",
    )

    abha_number = ""
    aadhaar_number = ""
    passport_number = ""

    status = MPIStatus.ACTIVE
    verification_status = MPIVerificationStatus.PENDING
    record_source = MPIRecordSource.MANUAL
    match_confidence = MPIMatchConfidence.EXACT
    merge_status = MPIMergeStatus.NOT_MERGED
    merged_into = None
    notes = ""

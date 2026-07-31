"""
Custom managers and querysets for the Master Patient Index.
"""

from __future__ import annotations

from django.db import models

from apps.patient_management.mpi.constants import (
    MPIMergeStatus,
    MPIStatus,
    MPIVerificationStatus,
)


class MasterPatientIndexQuerySet(models.QuerySet):
    """QuerySet for MasterPatientIndex."""

    def active(self) -> MasterPatientIndexQuerySet:
        return self.filter(
            status=MPIStatus.ACTIVE,
        )

    def inactive(self) -> MasterPatientIndexQuerySet:
        return self.filter(
            status=MPIStatus.INACTIVE,
        )

    def archived(self) -> MasterPatientIndexQuerySet:
        return self.filter(
            status=MPIStatus.ARCHIVED,
        )

    def verified(self) -> MasterPatientIndexQuerySet:
        return self.filter(
            verification_status=MPIVerificationStatus.VERIFIED,
        )

    def pending(self) -> MasterPatientIndexQuerySet:
        return self.filter(
            verification_status=MPIVerificationStatus.PENDING,
        )

    def merged(self) -> MasterPatientIndexQuerySet:
        return self.filter(
            merge_status=MPIMergeStatus.MERGED,
        )

    def by_organization(
        self,
        organization_id: int,
    ) -> MasterPatientIndexQuerySet:
        return self.filter(
            organization_id=organization_id,
        )

    def by_patient(
        self,
        patient_id: int,
    ) -> MasterPatientIndexQuerySet:
        return self.filter(
            patient_id=patient_id,
        )


MasterPatientIndexManager = models.Manager.from_queryset(
    MasterPatientIndexQuerySet,
)

__all__ = [
    "MasterPatientIndexManager",
    "MasterPatientIndexQuerySet",
]

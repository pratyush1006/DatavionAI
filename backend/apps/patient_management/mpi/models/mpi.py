"""
Master Patient Index model.
"""

from __future__ import annotations

from apps.patient_management.patients.models import Patient
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.patient_management.mpi.constants import (
    MPIMatchConfidence,
    MPIMergeStatus,
    MPIRecordSource,
    MPIStatus,
    MPIVerificationStatus,
)
from apps.patient_management.mpi.managers import (
    MasterPatientIndexManager,
)
from apps.patient_management.mpi.validators import (
    validate_aadhaar_number,
    validate_abha_number,
    validate_mpi_id,
    validate_passport_number,
)
from apps.platform.organizations.models import Organization


class MasterPatientIndex(BaseModel):
    """
    Enterprise Master Patient Index.
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="mpi_records",
    )

    patient = models.OneToOneField(
        Patient,
        on_delete=models.CASCADE,
        related_name="mpi_record",
    )

    mpi_id = models.CharField(
        max_length=32,
        unique=True,
        validators=[
            validate_mpi_id,
        ],
        verbose_name=_("MPI ID"),
    )

    abha_number = models.CharField(
        max_length=20,
        blank=True,
        validators=[
            validate_abha_number,
        ],
    )

    aadhaar_number = models.CharField(
        max_length=12,
        blank=True,
        validators=[
            validate_aadhaar_number,
        ],
    )

    passport_number = models.CharField(
        max_length=16,
        blank=True,
        validators=[
            validate_passport_number,
        ],
    )

    status = models.CharField(
        max_length=20,
        choices=MPIStatus.choices,
        default=MPIStatus.ACTIVE,
    )

    verification_status = models.CharField(
        max_length=20,
        choices=MPIVerificationStatus.choices,
        default=MPIVerificationStatus.PENDING,
    )

    record_source = models.CharField(
        max_length=20,
        choices=MPIRecordSource.choices,
        default=MPIRecordSource.MANUAL,
    )

    match_confidence = models.CharField(
        max_length=20,
        choices=MPIMatchConfidence.choices,
        default=MPIMatchConfidence.EXACT,
    )

    merge_status = models.CharField(
        max_length=20,
        choices=MPIMergeStatus.choices,
        default=MPIMergeStatus.NOT_MERGED,
    )

    merged_into = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="merged_records",
    )

    notes = models.TextField(
        blank=True,
    )

    verified_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    objects = MasterPatientIndexManager()

    class Meta:
        verbose_name = _("Master Patient Index")
        verbose_name_plural = _("Master Patient Index")

        ordering = ("-created_at",)

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "status",
                ],
            ),
            models.Index(
                fields=[
                    "patient",
                ],
            ),
            models.Index(
                fields=[
                    "mpi_id",
                ],
            ),
            models.Index(
                fields=[
                    "abha_number",
                ],
            ),
            models.Index(
                fields=[
                    "verification_status",
                ],
            ),
            models.Index(
                fields=[
                    "merge_status",
                ],
            ),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "patient",
                ],
                name="unique_mpi_per_patient",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        return self.mpi_id

    @property
    def is_active(
        self,
    ) -> bool:
        """
        Return whether the MPI record is active.
        """
        return self.status == MPIStatus.ACTIVE

    @property
    def is_verified(
        self,
    ) -> bool:
        """
        Return whether the MPI record is verified.
        """
        return self.verification_status == MPIVerificationStatus.VERIFIED

    @property
    def is_merged(
        self,
    ) -> bool:
        """
        Return whether the MPI record has been merged.
        """
        return self.merge_status == MPIMergeStatus.MERGED

    def clean(
        self,
    ) -> None:
        """
        Validate the MPI record.
        """
        super().clean()

        if self.merge_status == MPIMergeStatus.MERGED and self.merged_into is None:
            raise ValidationError(
                {
                    "merged_into": _(
                        "Merged records must reference the target MPI record.",
                    ),
                },
            )

        if self.merged_into and self.merged_into_id == self.pk:
            raise ValidationError(
                {
                    "merged_into": _(
                        "An MPI record cannot be merged into itself.",
                    ),
                },
            )

    def save(
        self,
        *args,
        **kwargs,
    ) -> None:
        """
        Validate before saving.
        """
        self.full_clean()

        super().save(
            *args,
            **kwargs,
        )

    def activate(
        self,
    ) -> None:
        """
        Activate the MPI record.
        """
        self.status = MPIStatus.ACTIVE
        self.save(
            update_fields=[
                "status",
                "updated_at",
            ],
        )

    def deactivate(
        self,
    ) -> None:
        """
        Deactivate the MPI record.
        """
        self.status = MPIStatus.INACTIVE
        self.save(
            update_fields=[
                "status",
                "updated_at",
            ],
        )

    def verify(
        self,
    ) -> None:
        """
        Mark the MPI record as verified.
        """
        self.verification_status = MPIVerificationStatus.VERIFIED
        self.verified_at = timezone.now()

        self.save(
            update_fields=[
                "verification_status",
                "verified_at",
                "updated_at",
            ],
        )

    def merge(
        self,
        *,
        target: MasterPatientIndex,
    ) -> None:
        """
        Merge this MPI record into another record.
        """
        if target.pk == self.pk:
            raise ValidationError(
                _("An MPI record cannot be merged into itself."),
            )

        self.merge_status = MPIMergeStatus.MERGED
        self.status = MPIStatus.MERGED
        self.merged_into = target

        self.save(
            update_fields=[
                "merge_status",
                "status",
                "merged_into",
                "updated_at",
            ],
        )

    def unmerge(
        self,
    ) -> None:
        """
        Restore a merged MPI record.
        """
        self.merge_status = MPIMergeStatus.UNMERGED
        self.status = MPIStatus.ACTIVE
        self.merged_into = None

        self.save(
            update_fields=[
                "merge_status",
                "status",
                "merged_into",
                "updated_at",
            ],
        )

    def archive(
        self,
    ) -> None:
        """
        Archive the MPI record.
        """
        self.status = MPIStatus.ARCHIVED

        self.save(
            update_fields=[
                "status",
                "updated_at",
            ],
        )

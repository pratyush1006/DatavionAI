"""
Domain services for the Master Patient Index.
"""

from __future__ import annotations

from collections.abc import Mapping
from decimal import Decimal
from typing import Any

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from apps.patient_management.mpi.constants import (
    ALLOWED_RECORD_TRANSITIONS,
    MPIMatchStatus,
    MPIRecordStatus,
)
from apps.patient_management.mpi.exceptions import (
    MPIIdentityError,
    MPILifecycleError,
    MPIMergeError,
    MPIOrganizationError,
)
from apps.patient_management.mpi.matching import calculate_match
from apps.patient_management.mpi.models import (
    MPIMatchCandidate,
    MPIRecord,
)
from apps.patient_management.patients.models import Patient
from apps.platform.accounts.models import User


class MPIService:
    """Encapsulate validated Master Patient Index mutations."""

    @staticmethod
    def _ensure_boundary(
        *,
        patient: Patient,
        organization: Any,
    ) -> None:
        """Ensure patient and organization share the same tenant and organization."""

        if patient.organization_id != organization.pk:
            raise MPIOrganizationError(
                "Patient does not belong to the selected organization.",
            )

        if patient.organization.tenant_id != organization.tenant_id:
            raise MPIOrganizationError(
                "Patient and MPI organization belong to different tenants.",
            )

    @staticmethod
    def _ensure_record_boundary(
        *,
        record: MPIRecord,
        organization: Any,
    ) -> None:
        """Ensure an MPI record belongs to the selected organization and tenant."""

        if record.organization_id != organization.pk:
            raise MPIOrganizationError(
                "MPI record does not belong to the selected organization.",
            )

        if record.organization.tenant_id != organization.tenant_id:
            raise MPIOrganizationError(
                "MPI record belongs to a different tenant.",
            )

    @staticmethod
    def _validate_score(value: Decimal) -> Decimal:
        """Validate and normalize a match score."""

        score = Decimal(str(value))
        if score < 0 or score > 1:
            raise ValidationError(
                {"score": "Match score must be between 0 and 1."},
            )
        return score.quantize(Decimal("0.0001"))

    @classmethod
    @transaction.atomic
    def create_record(
        cls,
        *,
        organization: Any,
        patient: Patient,
        enterprise_identifier: str,
        source_system: str = "",
        source_patient_identifier: str = "",
        demographics_snapshot: Mapping[str, Any] | None = None,
        performed_by: User | None = None,
    ) -> MPIRecord:
        """Create one MPI record for the canonical Patient."""

        cls._ensure_boundary(
            patient=patient,
            organization=organization,
        )

        enterprise_identifier = enterprise_identifier.strip()
        if not enterprise_identifier:
            raise ValidationError(
                {"enterprise_identifier": "Enterprise identifier is required."},
            )

        record = MPIRecord(
            organization=organization,
            patient=patient,
            enterprise_identifier=enterprise_identifier,
            source_system=source_system.strip(),
            source_patient_identifier=source_patient_identifier.strip(),
            demographics_snapshot=dict(demographics_snapshot or {}),
        )
        record.full_clean()
        record.save()
        return record

    @classmethod
    @transaction.atomic
    def update_record(
        cls,
        *,
        record: MPIRecord,
        data: Mapping[str, Any],
        performed_by: User | None = None,
    ) -> MPIRecord:
        """Update mutable MPI metadata without changing identity ownership."""

        if record.is_deleted:
            raise ValidationError(
                {"detail": "Deleted MPI records cannot be updated."},
            )

        allowed_fields = {
            "source_system",
            "source_patient_identifier",
            "demographics_snapshot",
            "match_score",
            "confidence",
        }
        unknown = set(data) - allowed_fields
        if unknown:
            raise ValidationError(
                {
                    "detail": ("Unsupported MPI fields: " + ", ".join(sorted(unknown))),
                },
            )

        for field, value in data.items():
            if field in {"match_score", "confidence"}:
                value = cls._validate_score(value)
            elif field in {"source_system", "source_patient_identifier"}:
                value = str(value).strip()
            setattr(record, field, value)

        record.full_clean()
        record.save()
        return record

    @classmethod
    @transaction.atomic
    def transition(
        cls,
        *,
        record: MPIRecord,
        status: str,
        performed_by: User,
    ) -> MPIRecord:
        """Apply a strict MPI record lifecycle transition."""

        if record.is_deleted:
            raise MPILifecycleError(
                "Deleted MPI records cannot change lifecycle state.",
            )

        allowed = ALLOWED_RECORD_TRANSITIONS.get(record.status)
        if allowed is None or status not in allowed:
            raise MPILifecycleError(
                f"Invalid MPI transition: {record.status} -> {status}.",
            )

        record.status = status
        record.is_active = status == MPIRecordStatus.ACTIVE
        if status == MPIRecordStatus.RETIRED:
            record.reviewed_at = timezone.now()
            record.reviewed_by_id = performed_by.pk

        record.full_clean()
        record.save()
        return record

    @classmethod
    @transaction.atomic
    def create_candidate(
        cls,
        *,
        organization: Any,
        left_record: MPIRecord,
        right_record: MPIRecord,
        performed_by: User | None = None,
    ) -> MPIMatchCandidate:
        """Create or refresh a pending candidate without reopening reviewed decisions."""

        if left_record.pk == right_record.pk:
            raise MPIIdentityError(
                "An MPI record cannot be matched with itself.",
            )

        cls._ensure_record_boundary(
            record=left_record,
            organization=organization,
        )
        cls._ensure_record_boundary(
            record=right_record,
            organization=organization,
        )

        if left_record.status != MPIRecordStatus.ACTIVE:
            raise MPIIdentityError("Only active MPI records may be matched.")
        if right_record.status != MPIRecordStatus.ACTIVE:
            raise MPIIdentityError("Only active MPI records may be matched.")

        result = calculate_match(
            left=left_record.demographics_snapshot,
            right=right_record.demographics_snapshot,
        )

        first, second = sorted(
            (left_record, right_record),
            key=lambda item: str(item.pk),
        )

        candidate = (
            MPIMatchCandidate.objects.select_for_update()
            .filter(
                organization=organization,
                left_record=first,
                right_record=second,
            )
            .first()
        )

        if candidate is not None:
            if candidate.status in {
                MPIMatchStatus.CONFIRMED,
                MPIMatchStatus.REJECTED,
            }:
                raise MPIIdentityError(
                    "Reviewed MPI candidates cannot be silently reopened.",
                )
            candidate.score = cls._validate_score(result.score)
            candidate.evidence = result.evidence
            candidate.status = MPIMatchStatus.PENDING
            candidate.full_clean()
            candidate.save()
            return candidate

        candidate = MPIMatchCandidate(
            organization=organization,
            left_record=first,
            right_record=second,
            score=cls._validate_score(result.score),
            status=MPIMatchStatus.PENDING,
            evidence=result.evidence,
        )
        candidate.full_clean()
        candidate.save()
        return candidate

    @classmethod
    @transaction.atomic
    def review_candidate(
        cls,
        *,
        candidate: MPIMatchCandidate,
        status: str,
        performed_by: User,
    ) -> MPIMatchCandidate:
        """Review a pending MPI candidate match."""

        if status not in {
            MPIMatchStatus.CONFIRMED,
            MPIMatchStatus.REJECTED,
        }:
            raise ValidationError(
                {"status": "Candidate review must confirm or reject the match."},
            )

        if candidate.status != MPIMatchStatus.PENDING:
            raise ValidationError(
                {"status": "Only pending candidates may be reviewed."},
            )

        candidate.status = status
        candidate.reviewed_at = timezone.now()
        candidate.reviewed_by_id = performed_by.pk
        candidate.full_clean()
        candidate.save()
        return candidate

    @classmethod
    @transaction.atomic
    def merge_records(
        cls,
        *,
        survivor: MPIRecord,
        duplicate: MPIRecord,
        candidate: MPIMatchCandidate,
        performed_by: User,
    ) -> tuple[MPIRecord, MPIRecord]:
        """Merge an active duplicate only after an explicit confirmed match."""

        if survivor.pk == duplicate.pk:
            raise MPIMergeError(
                "An MPI record cannot be merged into itself.",
            )

        if survivor.organization_id != duplicate.organization_id:
            raise MPIOrganizationError(
                "MPI records from different organizations cannot be merged.",
            )

        if candidate.organization_id != survivor.organization_id:
            raise MPIOrganizationError(
                "The confirmed candidate belongs to a different organization.",
            )

        pair = {candidate.left_record_id, candidate.right_record_id}
        if pair != {survivor.pk, duplicate.pk}:
            raise MPIMergeError(
                "The confirmed candidate does not represent the requested merge pair.",
            )

        if candidate.status != MPIMatchStatus.CONFIRMED:
            raise MPIMergeError(
                "MPI merges require a confirmed candidate match.",
            )

        if survivor.status != MPIRecordStatus.ACTIVE:
            raise MPIMergeError(
                "The survivor MPI record must be active.",
            )

        if duplicate.status != MPIRecordStatus.ACTIVE:
            raise MPIMergeError(
                "Only active MPI records may be merged.",
            )

        if survivor.is_deleted or duplicate.is_deleted:
            raise MPIMergeError(
                "Deleted MPI records cannot participate in a merge.",
            )

        duplicate.status = MPIRecordStatus.MERGED
        duplicate.is_active = False
        duplicate.merged_into = survivor
        duplicate.reviewed_at = timezone.now()
        duplicate.reviewed_by_id = performed_by.pk
        duplicate.full_clean()
        duplicate.save()

        return survivor, duplicate

    @classmethod
    @transaction.atomic
    def reverse_merge(
        cls,
        *,
        duplicate: MPIRecord,
        performed_by: User,
    ) -> MPIRecord:
        """Reverse an MPI merge only while its survivor remains active."""

        if duplicate.status != MPIRecordStatus.MERGED:
            raise MPIMergeError(
                "Only merged MPI records may be restored from a merge.",
            )

        if duplicate.merged_into_id is None:
            raise MPIMergeError(
                "Merged MPI record has no survivor reference.",
            )

        survivor = MPIRecord.objects.filter(
            pk=duplicate.merged_into_id,
            organization_id=duplicate.organization_id,
            status=MPIRecordStatus.ACTIVE,
            is_active=True,
            is_deleted=False,
        ).first()
        if survivor is None:
            raise MPIMergeError(
                "The merge survivor is no longer active; reversal is blocked.",
            )

        duplicate.status = MPIRecordStatus.ACTIVE
        duplicate.is_active = True
        duplicate.merged_into = None
        duplicate.reviewed_at = timezone.now()
        duplicate.reviewed_by_id = performed_by.pk
        duplicate.full_clean()
        duplicate.save()
        return duplicate

    @classmethod
    @transaction.atomic
    def delete_record(
        cls,
        *,
        record: MPIRecord,
        performed_by: User,
    ) -> MPIRecord:
        """Soft-delete an MPI record after it leaves the active lifecycle."""

        if record.status == MPIRecordStatus.ACTIVE:
            raise MPIMergeError(
                "Active MPI records must be retired before deletion.",
            )

        record.delete(user_id=performed_by.pk)
        return record

    @classmethod
    @transaction.atomic
    def restore_record(
        cls,
        *,
        record: MPIRecord,
        performed_by: User,
    ) -> MPIRecord:
        """Restore a soft-deleted MPI record without changing lifecycle state."""

        if record.status == MPIRecordStatus.MERGED:
            raise MPIMergeError(
                "Merged MPI records cannot be restored directly.",
            )

        record.restore()
        record.full_clean()
        record.save()
        return record


__all__ = ("MPIService",)

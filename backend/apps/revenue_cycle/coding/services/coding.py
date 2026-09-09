from __future__ import annotations

"""Transactional Coding domain services."""

from typing import Any
from uuid import UUID

from django.db import IntegrityError, transaction
from django.utils import timezone

from apps.core.events import publisher

from ..constants import ALLOWED_TRANSITIONS, CodingStatus
from ..events import build_coding_event
from ..exceptions import CodingTransitionError, CodingValidationError
from ..models import CodeAssignment, CodingRecord
from ..selectors import (
    get_coding_record_for_update,
    get_deleted_coding_record_for_update,
)
from ..validators import (
    validate_code_system,
    validate_code_value,
    validate_documentation,
    validate_encounter_reference,
)


class CodingService:
    """Perform transactional Coding aggregate mutations."""

    @staticmethod
    def _validate_organization_tenant(
        *,
        organization: Any,
        tenant_id: UUID,
    ) -> None:
        """Ensure the organization belongs to the active tenant."""

        if organization.tenant_id != tenant_id:
            raise CodingValidationError(
                "Organization does not belong to the active tenant."
            )

    @staticmethod
    def _validate_patient(
        *,
        patient: Any,
        organization: Any,
    ) -> None:
        """Ensure the canonical patient belongs to the organization."""

        if patient.organization_id != organization.id:
            raise CodingValidationError("Patient does not belong to the organization.")

    @staticmethod
    def _publish(
        *,
        event_name: str,
        record: CodingRecord,
        tenant_id: UUID,
        actor: Any,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Schedule a Coding domain event after transaction commit."""

        event = build_coding_event(
            event_name=event_name,
            coding_record_id=record.id,
            organization_id=record.organization_id,
            tenant_id=tenant_id,
            actor_id=getattr(actor, "id", None),
            metadata=metadata,
        )
        transaction.on_commit(
            lambda: publisher.publish(event),
        )

    @classmethod
    @transaction.atomic
    def create(
        cls,
        *,
        organization: Any,
        tenant_id: UUID,
        patient: Any,
        actor: Any,
        idempotency_key: str,
        source_reference: str,
        service_date: Any,
        coding_type: str,
        encounter_type: str = "",
        clinical_summary: str = "",
        documentation: dict[str, Any] | None = None,
        coding_notes: str = "",
    ) -> CodingRecord:
        """Create a tenant-owned Coding record."""

        cls._validate_organization_tenant(
            organization=organization,
            tenant_id=tenant_id,
        )
        cls._validate_patient(
            patient=patient,
            organization=organization,
        )

        normalized_key = idempotency_key.strip()
        normalized_reference = validate_encounter_reference(
            source_reference,
        )

        if not normalized_key:
            raise CodingValidationError("Idempotency key is required.")

        existing = CodingRecord.objects.filter(
            organization=organization,
            idempotency_key=normalized_key,
        ).first()
        if existing is not None:
            return existing

        try:
            record = CodingRecord.objects.create(
                organization=organization,
                patient=patient,
                coding_type=coding_type,
                source_reference=normalized_reference,
                service_date=service_date,
                encounter_type=encounter_type.strip(),
                clinical_summary=clinical_summary,
                documentation=validate_documentation(documentation),
                coding_notes=coding_notes,
                idempotency_key=normalized_key,
            )
        except IntegrityError as exc:
            existing = CodingRecord.objects.filter(
                organization=organization,
                idempotency_key=normalized_key,
            ).first()
            if existing is not None:
                return existing
            raise CodingValidationError(
                "Coding record could not be created because a "
                "unique constraint was violated."
            ) from exc

        cls._publish(
            event_name="revenue_cycle.coding.created",
            record=record,
            tenant_id=tenant_id,
            actor=actor,
        )
        return record

    @classmethod
    @transaction.atomic
    def update(
        cls,
        *,
        record_id: UUID,
        organization: Any,
        tenant_id: UUID,
        actor: Any,
        **changes: Any,
    ) -> CodingRecord:
        """Update mutable Coding fields under a row lock."""

        record = get_coding_record_for_update(
            organization_id=organization.id,
            record_id=record_id,
            tenant_id=tenant_id,
        )

        if record.status in {
            CodingStatus.RELEASED,
            CodingStatus.VOIDED,
        }:
            raise CodingValidationError(
                "Released or voided coding records are immutable."
            )

        allowed = {
            "encounter_type",
            "clinical_summary",
            "documentation",
            "coding_notes",
            "rejection_reason",
        }

        for key, value in changes.items():
            if key not in allowed:
                continue

            if key == "documentation":
                value = validate_documentation(value)

            setattr(record, key, value)

        record.save()

        cls._publish(
            event_name="revenue_cycle.coding.updated",
            record=record,
            tenant_id=tenant_id,
            actor=actor,
        )
        return record

    @classmethod
    @transaction.atomic
    def transition(
        cls,
        *,
        record_id: UUID,
        organization: Any,
        tenant_id: UUID,
        actor: Any,
        target_status: str,
        note: str = "",
    ) -> CodingRecord:
        """Apply a validated Coding lifecycle transition."""

        record = get_coding_record_for_update(
            organization_id=organization.id,
            record_id=record_id,
            tenant_id=tenant_id,
        )

        allowed = ALLOWED_TRANSITIONS.get(record.status, set())
        if target_status not in allowed:
            raise CodingTransitionError(
                f"Invalid coding transition: {record.status} -> {target_status}."
            )

        now = timezone.now()
        previous_status = record.status
        record.status = target_status

        if target_status == CodingStatus.ASSIGNED:
            record.assigned_to = actor
            record.assigned_at = now
        elif target_status == CodingStatus.IN_REVIEW:
            record.reviewed_by = actor
            record.reviewed_at = now
        elif target_status == CodingStatus.VALIDATED:
            record.validated_by = actor
            record.validated_at = now
        elif target_status == CodingStatus.RELEASED:
            has_active_code = CodeAssignment.objects.filter(
                coding_record=record,
                is_deleted=False,
            ).exists()
            if not has_active_code:
                raise CodingValidationError(
                    "At least one active code assignment is required before release."
                )
            record.released_by = actor
            record.released_at = now
        elif target_status == CodingStatus.VOIDED:
            record.voided_at = now

        if note:
            record.coding_notes = note.strip()

        record.save()

        cls._publish(
            event_name="revenue_cycle.coding.status_changed",
            record=record,
            tenant_id=tenant_id,
            actor=actor,
            metadata={
                "from_status": previous_status,
                "to_status": target_status,
            },
        )
        return record

    @classmethod
    @transaction.atomic
    def add_code(
        cls,
        *,
        record_id: UUID,
        organization: Any,
        tenant_id: UUID,
        actor: Any,
        code_system: str,
        code: str,
        description: str = "",
        sequence: int = 1,
        is_primary: bool = False,
        present_on_admission: bool | None = None,
        evidence: dict[str, Any] | None = None,
    ) -> CodeAssignment:
        """Add a code assignment to a mutable Coding record."""

        record = get_coding_record_for_update(
            organization_id=organization.id,
            record_id=record_id,
            tenant_id=tenant_id,
        )

        if record.status in {
            CodingStatus.RELEASED,
            CodingStatus.VOIDED,
        }:
            raise CodingValidationError(
                "Released or voided coding records cannot be modified."
            )

        normalized_system = validate_code_system(code_system)
        normalized_code = validate_code_value(code)

        if sequence < 1:
            raise CodingValidationError("Sequence must be at least one.")

        if is_primary:
            CodeAssignment.objects.filter(
                coding_record=record,
                is_primary=True,
                is_deleted=False,
            ).update(is_primary=False)

        assignment = CodeAssignment.objects.create(
            coding_record=record,
            code_system=normalized_system,
            code=normalized_code,
            description=description.strip(),
            sequence=sequence,
            is_primary=is_primary,
            present_on_admission=present_on_admission,
            evidence=evidence or {},
        )

        cls._publish(
            event_name="revenue_cycle.coding.code_assigned",
            record=record,
            tenant_id=tenant_id,
            actor=actor,
            metadata={
                "code_assignment_id": str(assignment.id),
                "code_system": normalized_system,
                "code": normalized_code,
            },
        )
        return assignment

    @classmethod
    @transaction.atomic
    def delete(
        cls,
        *,
        record_id: UUID,
        organization: Any,
        tenant_id: UUID,
        actor: Any,
    ) -> CodingRecord:
        """Soft-delete a mutable Coding record."""

        record = get_coding_record_for_update(
            organization_id=organization.id,
            record_id=record_id,
            tenant_id=tenant_id,
        )

        if record.status == CodingStatus.RELEASED:
            raise CodingValidationError("Released coding records cannot be deleted.")

        record.soft_delete(user_id=actor.id)

        cls._publish(
            event_name="revenue_cycle.coding.deleted",
            record=record,
            tenant_id=tenant_id,
            actor=actor,
        )
        return record

    @classmethod
    @transaction.atomic
    def restore(
        cls,
        *,
        record_id: UUID,
        organization: Any,
        tenant_id: UUID,
        actor: Any,
    ) -> CodingRecord:
        """Restore a deleted Coding record under a row lock."""

        record = get_deleted_coding_record_for_update(
            organization_id=organization.id,
            record_id=record_id,
            tenant_id=tenant_id,
        )

        record.restore()

        cls._publish(
            event_name="revenue_cycle.coding.restored",
            record=record,
            tenant_id=tenant_id,
            actor=actor,
        )
        return record


__all__ = ("CodingService",)

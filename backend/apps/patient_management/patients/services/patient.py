"""
Patient Core domain services.

Responsibilities
----------------
- Patient aggregate persistence.
- Aggregate validation.
- Normalization.
- Lifecycle state mutation.
- Patient audit logging.

Non-responsibilities
--------------------
- HTTP/API concerns.
- RBAC authorization.
- Workflow orchestration.
- Domain event publication.
- Background processing.

All externally initiated mutations should enter through a Patient
workflow. These services remain the persistence/domain boundary used
by those workflows.
"""

from __future__ import annotations

from collections.abc import Mapping
from datetime import date
from typing import Any

from django.db import transaction

from apps.patient_management.patients.constants import PatientStatus
from apps.patient_management.patients.models import (
    Patient,
    PatientAuditAction,
    PatientAuditLog,
)
from apps.platform.accounts.models import User


class PatientService:
    """
    Domain service for Patient aggregate mutations.
    """

    # ------------------------------------------------------------------
    # Audit
    # ------------------------------------------------------------------

    @staticmethod
    def _serialize_value(
        value: Any,
    ) -> Any:
        """
        Convert model/domain values into JSON-safe audit values.
        """

        if isinstance(value, date):
            return value.isoformat()

        if hasattr(value, "pk"):
            return str(value.pk)

        if hasattr(value, "id"):
            return str(value.id)

        if isinstance(value, (list, tuple)):
            return [PatientService._serialize_value(item) for item in value]

        if isinstance(value, dict):
            return {
                str(key): PatientService._serialize_value(item)
                for key, item in value.items()
            }

        return value

    @staticmethod
    def _log_audit(
        *,
        organization: Any,
        patient: Patient,
        action: PatientAuditAction | str,
        changes: Mapping[str, Any] | None = None,
        performed_by: User | None = None,
    ) -> PatientAuditLog:
        """
        Persist a patient audit record.

        Audit creation occurs inside the same database transaction as
        the aggregate mutation.
        """

        serialized_changes = {
            str(key): PatientService._serialize_value(value)
            for key, value in (changes or {}).items()
        }

        return PatientAuditLog.objects.create(
            organization=organization,
            patient=patient,
            action=action,
            changes=serialized_changes,
            performed_by=performed_by,
        )

    # ------------------------------------------------------------------
    # Create
    # ------------------------------------------------------------------

    @staticmethod
    @transaction.atomic
    def create(
        *,
        validated_data: Mapping[str, Any],
        performed_by: User | None = None,
    ) -> Patient:
        """
        Create a Patient aggregate.
        """

        data = dict(validated_data)

        patient = Patient(
            **data,
        )

        patient.full_clean()
        patient.save()

        PatientService._log_audit(
            organization=patient.organization,
            patient=patient,
            action=PatientAuditAction.CREATE,
            changes=data,
            performed_by=performed_by,
        )

        return patient

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------

    @staticmethod
    @transaction.atomic
    def update(
        *,
        instance: Patient,
        validated_data: Mapping[str, Any],
        performed_by: User | None = None,
    ) -> Patient:
        """
        Update mutable Patient fields.

        Only explicitly supplied fields are changed.
        """

        if not validated_data:
            return instance

        changes: dict[str, Any] = {}

        for field, value in validated_data.items():
            if not hasattr(instance, field):
                raise ValueError(
                    f"Unknown patient field: {field}.",
                )

            old_value = getattr(
                instance,
                field,
            )

            if old_value != value:
                changes[field] = {
                    "old": old_value,
                    "new": value,
                }

            setattr(
                instance,
                field,
                value,
            )

        if not changes:
            return instance

        instance.full_clean()

        instance.save(
            update_fields=tuple(
                changes.keys(),
            ),
        )

        instance.refresh_from_db()

        PatientService._log_audit(
            organization=instance.organization,
            patient=instance,
            action=PatientAuditAction.UPDATE,
            changes=changes,
            performed_by=performed_by,
        )

        return instance

    # ------------------------------------------------------------------
    # Activate
    # ------------------------------------------------------------------

    @staticmethod
    @transaction.atomic
    def activate(
        *,
        instance: Patient,
        performed_by: User | None = None,
    ) -> Patient:
        """
        Activate a patient.
        """

        previous_status = instance.status
        previous_is_active = instance.is_active

        if previous_status == PatientStatus.ACTIVE and previous_is_active:
            return instance

        instance.status = PatientStatus.ACTIVE
        instance.is_active = True

        instance.save(
            update_fields=(
                "status",
                "is_active",
            ),
        )

        PatientService._log_audit(
            organization=instance.organization,
            patient=instance,
            action=PatientAuditAction.UPDATE,
            changes={
                "status": {
                    "old": previous_status,
                    "new": PatientStatus.ACTIVE,
                },
                "is_active": {
                    "old": previous_is_active,
                    "new": True,
                },
            },
            performed_by=performed_by,
        )

        return instance

    # ------------------------------------------------------------------
    # Deactivate
    # ------------------------------------------------------------------

    @staticmethod
    @transaction.atomic
    def deactivate(
        *,
        instance: Patient,
        performed_by: User | None = None,
    ) -> Patient:
        """
        Deactivate a patient.
        """

        previous_status = instance.status
        previous_is_active = instance.is_active

        if previous_status == PatientStatus.INACTIVE and not previous_is_active:
            return instance

        instance.status = PatientStatus.INACTIVE
        instance.is_active = False

        instance.save(
            update_fields=(
                "status",
                "is_active",
            ),
        )

        PatientService._log_audit(
            organization=instance.organization,
            patient=instance,
            action=PatientAuditAction.UPDATE,
            changes={
                "status": {
                    "old": previous_status,
                    "new": PatientStatus.INACTIVE,
                },
                "is_active": {
                    "old": previous_is_active,
                    "new": False,
                },
            },
            performed_by=performed_by,
        )

        return instance

    # ------------------------------------------------------------------
    # Archive
    # ------------------------------------------------------------------

    @staticmethod
    @transaction.atomic
    def archive(
        *,
        instance: Patient,
        performed_by: User | None = None,
    ) -> Patient:
        """
        Archive a patient.

        Archive is a business lifecycle state and is deliberately
        distinct from BaseModel soft deletion.
        """

        previous_status = instance.status
        previous_is_active = instance.is_active

        if previous_status == PatientStatus.ARCHIVED and not previous_is_active:
            return instance

        instance.status = PatientStatus.ARCHIVED
        instance.is_active = False

        instance.save(
            update_fields=(
                "status",
                "is_active",
            ),
        )

        PatientService._log_audit(
            organization=instance.organization,
            patient=instance,
            action=PatientAuditAction.ARCHIVE,
            changes={
                "status": {
                    "old": previous_status,
                    "new": PatientStatus.ARCHIVED,
                },
                "is_active": {
                    "old": previous_is_active,
                    "new": False,
                },
            },
            performed_by=performed_by,
        )

        return instance

    # ------------------------------------------------------------------
    # Restore
    # ------------------------------------------------------------------

    @staticmethod
    @transaction.atomic
    def restore(
        *,
        instance: Patient,
        performed_by: User | None = None,
    ) -> Patient:
        """
        Restore an archived patient to active state.
        """

        previous_status = instance.status
        previous_is_active = instance.is_active

        if previous_status == PatientStatus.ACTIVE and previous_is_active:
            return instance

        if previous_status != PatientStatus.ARCHIVED:
            return instance

        instance.status = PatientStatus.ACTIVE
        instance.is_active = True

        instance.save(
            update_fields=(
                "status",
                "is_active",
            ),
        )

        PatientService._log_audit(
            organization=instance.organization,
            patient=instance,
            action=PatientAuditAction.RESTORE,
            changes={
                "status": {
                    "old": previous_status,
                    "new": PatientStatus.ACTIVE,
                },
                "is_active": {
                    "old": previous_is_active,
                    "new": True,
                },
            },
            performed_by=performed_by,
        )

        return instance

    # ------------------------------------------------------------------
    # Delete
    # ------------------------------------------------------------------

    @staticmethod
    @transaction.atomic
    def delete(
        *,
        instance: Patient,
        performed_by: User | None = None,
    ) -> None:
        """
        Delete through BaseModel's configured lifecycle.

        BaseModel controls whether deletion is represented as a
        soft-delete. This service deliberately does not bypass that
        lifecycle with direct queryset deletion.
        """

        PatientService._log_audit(
            organization=instance.organization,
            patient=instance,
            action=PatientAuditAction.DELETE,
            changes={
                "status": instance.status,
                "is_active": instance.is_active,
            },
            performed_by=performed_by,
        )

        instance.delete()


# ----------------------------------------------------------------------
# Functional aliases
# ----------------------------------------------------------------------

create_patient = PatientService.create
update_patient = PatientService.update
activate_patient = PatientService.activate
deactivate_patient = PatientService.deactivate
archive_patient = PatientService.archive
restore_patient = PatientService.restore
delete_patient = PatientService.delete


__all__ = (
    "PatientService",
    "activate_patient",
    "archive_patient",
    "create_patient",
    "deactivate_patient",
    "delete_patient",
    "restore_patient",
    "update_patient",
)

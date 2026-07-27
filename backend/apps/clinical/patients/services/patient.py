"""
Patient services.
"""

from __future__ import annotations

from collections.abc import Mapping
from datetime import date
from typing import Any

from django.db import transaction

from apps.clinical.patients.models import (
    Patient,
    PatientAuditLog,
)
from apps.platform.accounts.models import User


class PatientService:
    """
    Application service responsible for patient write operations.

    This service is the single entry point for all patient lifecycle
    operations and provides a centralized location for future business
    rules such as:

    - MRN generation
    - Duplicate detection
    - Patient merge
    - Archive / Restore
    - Audit logging
    - Domain events
    - Notifications
    - External integrations
    """

    @staticmethod
    def _log_audit(
        *,
        organization: Any,
        patient: Patient,
        action: str,
        changes: dict[str, Any] | None = None,
        performed_by: User | None = None,
    ) -> None:
        """
        Create an audit log entry.
        """

        def _serialize(value: Any) -> Any:
            if isinstance(value, (date,)):
                return value.isoformat()

            if hasattr(value, "pk"):
                return str(value.pk)

            if hasattr(value, "id"):
                return str(value.id)

            return value

        serialized_changes: dict[str, Any] = {}

        for key, value in (changes or {}).items():
            if isinstance(value, dict):
                serialized_changes[key] = {
                    inner_key: _serialize(inner_value)
                    for inner_key, inner_value in value.items()
                }
            else:
                serialized_changes[key] = _serialize(value)

        PatientAuditLog.objects.create(
            organization=organization,
            patient=patient,
            action=action,
            changes=serialized_changes,
            performed_by=performed_by,
        )

    @staticmethod
    @transaction.atomic
    def create(
        *,
        validated_data: Mapping[str, Any],
        performed_by: User | None = None,
    ) -> Patient:
        """
        Create a new patient.
        """

        patient = Patient(
            **validated_data,
        )

        patient.full_clean()

        patient.save()

        PatientService._log_audit(
            organization=patient.organization,
            patient=patient,
            action="create",
            changes=validated_data,
            performed_by=performed_by,
        )

        return patient

    @staticmethod
    @transaction.atomic
    def update(
        *,
        instance: Patient,
        validated_data: Mapping[str, Any],
        performed_by: User | None = None,
    ) -> Patient:
        """
        Update an existing patient.
        """

        changes: dict[str, Any] = {}

        for field, value in validated_data.items():
            old_value = getattr(
                instance,
                field,
                None,
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

        instance.full_clean()

        instance.save()

        if changes:
            PatientService._log_audit(
                organization=instance.organization,
                patient=instance,
                action="update",
                changes=changes,
                performed_by=performed_by,
            )

        return instance

    @staticmethod
    @transaction.atomic
    def delete(
        *,
        instance: Patient,
        performed_by: User | None = None,
    ) -> None:
        """
        Delete a patient.

        If DatavionOS later adopts soft deletion or archival,
        the implementation should change here without affecting
        API consumers.
        """

        PatientService._log_audit(
            organization=instance.organization,
            patient=instance,
            action="delete",
            performed_by=performed_by,
        )

        instance.hard_delete()

    @staticmethod
    @transaction.atomic
    def archive(
        *,
        instance: Patient,
        performed_by: User | None = None,
    ) -> Patient:
        """
        Archive a patient.
        """

        from apps.clinical.patients.constants import PatientStatus

        instance.status = PatientStatus.ARCHIVED
        instance.is_active = False

        instance.full_clean()

        instance.save(
            update_fields=[
                "status",
                "is_active",
            ],
        )

        PatientService._log_audit(
            organization=instance.organization,
            patient=instance,
            action="archive",
            performed_by=performed_by,
        )

        return instance

    @staticmethod
    @transaction.atomic
    def restore(
        *,
        instance: Patient,
        performed_by: User | None = None,
    ) -> Patient:
        """
        Restore an archived patient.
        """

        from apps.clinical.patients.constants import (
            DEFAULT_PATIENT_STATUS,
        )

        instance.status = DEFAULT_PATIENT_STATUS
        instance.is_active = True

        instance.full_clean()

        instance.save(
            update_fields=[
                "status",
                "is_active",
            ],
        )

        PatientService._log_audit(
            organization=instance.organization,
            patient=instance,
            action="restore",
            performed_by=performed_by,
        )

        return instance

    @staticmethod
    @transaction.atomic
    def bulk_create(
        *,
        validated_data_list: list[Mapping[str, Any]],
        performed_by: User | None = None,
    ) -> list[Patient]:
        """
        Create multiple patients.
        """

        patients: list[Patient] = []

        for validated_data in validated_data_list:
            patient = Patient(
                **validated_data,
            )

            patient.full_clean()

            patient.save()

            PatientService._log_audit(
                organization=patient.organization,
                patient=patient,
                action="create",
                changes=validated_data,
                performed_by=performed_by,
            )

            patients.append(patient)

        return patients

    @staticmethod
    @transaction.atomic
    def bulk_update(
        *,
        validated_data_list: list[tuple[Patient, Mapping[str, Any]]],
        performed_by: User | None = None,
    ) -> list[Patient]:
        """
        Update multiple patients.

        Each item in ``validated_data_list`` should be a tuple
        of ``(instance, validated_data)``.
        """

        patients: list[Patient] = []

        for instance, validated_data in validated_data_list:
            changes: dict[str, Any] = {}

            for field, value in validated_data.items():
                old_value = getattr(
                    instance,
                    field,
                    None,
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

            instance.full_clean()

            instance.save()

            if changes:
                PatientService._log_audit(
                    organization=instance.organization,
                    patient=instance,
                    action="update",
                    changes=changes,
                    performed_by=performed_by,
                )

            patients.append(instance)

        return patients

    @staticmethod
    @transaction.atomic
    def bulk_delete(
        *,
        instances: list[Patient],
        performed_by: User | None = None,
    ) -> None:
        """
        Delete multiple patients.
        """

        patient_ids = [instance.pk for instance in instances]

        for instance in instances:
            PatientService._log_audit(
                organization=instance.organization,
                patient=instance,
                action="delete",
                performed_by=performed_by,
            )

        Patient.all_objects.filter(
            pk__in=patient_ids,
        ).delete()


create_patient = PatientService.create
update_patient = PatientService.update
delete_patient = PatientService.delete


__all__ = [
    "PatientService",
    "create_patient",
    "update_patient",
    "delete_patient",
]

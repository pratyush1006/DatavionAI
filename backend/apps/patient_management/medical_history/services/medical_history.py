"""Mutation services for Patient Medical History."""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from apps.patient_management.medical_history.constants import ClinicalStatus
from apps.patient_management.medical_history.models import PatientMedicalHistory


class PatientMedicalHistoryService:
    """PatientMedicalHistoryService implementation."""

    @staticmethod
    @transaction.atomic
    def create(*, validated_data, performed_by=None):
        """Create."""
        instance = PatientMedicalHistory(
            **dict(validated_data), is_active=True, is_deleted=False
        )
        instance.normalize()
        instance.full_clean()
        instance.save()
        return instance

    @staticmethod
    @transaction.atomic
    def update(*, instance, validated_data, performed_by=None):
        """Update."""
        protected = {
            "id",
            "organization",
            "organization_id",
            "patient",
            "patient_id",
            "is_deleted",
            "deleted_at",
            "deleted_by",
            "is_verified",
            "verified_at",
            "verified_by",
            "created_at",
            "updated_at",
        }
        changes = dict(validated_data)
        invalid = protected.intersection(changes)
        if invalid:
            raise ValidationError(
                {"detail": "Protected fields: " + ", ".join(sorted(invalid))}
            )
        if instance.is_deleted:
            raise ValidationError(
                {"detail": "Deleted medical history cannot be updated."}
            )
        for field, value in changes.items():
            setattr(instance, field, value)
        instance.normalize()
        instance.full_clean()
        instance.save()
        return instance

    @staticmethod
    @transaction.atomic
    def delete(*, instance, performed_by=None):
        """Delete."""
        if instance.is_deleted:
            return instance
        instance.is_active = False
        instance.is_deleted = True
        instance.deleted_at = timezone.now()
        instance.deleted_by = performed_by
        instance.save(
            update_fields=(
                "is_active",
                "is_deleted",
                "deleted_at",
                "deleted_by",
                "updated_at",
            )
        )
        return instance

    @staticmethod
    @transaction.atomic
    def restore(*, instance, performed_by=None):
        """Restore."""
        if not instance.is_deleted:
            return instance
        instance.is_deleted = False
        instance.is_active = True
        instance.deleted_at = None
        instance.deleted_by = None
        instance.full_clean()
        instance.save(
            update_fields=(
                "is_deleted",
                "is_active",
                "deleted_at",
                "deleted_by",
                "updated_at",
            )
        )
        return instance

    @staticmethod
    @transaction.atomic
    def activate(*, instance, performed_by=None):
        """Activate."""
        if instance.is_deleted:
            raise ValidationError(
                {
                    "detail": "Deleted medical history must be restored before activation."
                }
            )
        instance.is_active = True
        if instance.clinical_status == ClinicalStatus.INACTIVE:
            instance.clinical_status = ClinicalStatus.ACTIVE
        instance.full_clean()
        instance.save(update_fields=("is_active", "clinical_status", "updated_at"))
        return instance

    @staticmethod
    @transaction.atomic
    def deactivate(*, instance, performed_by=None):
        """Deactivate."""
        if instance.is_deleted:
            raise ValidationError(
                {"detail": "Deleted medical history cannot be deactivated."}
            )
        instance.is_active = False
        instance.clinical_status = ClinicalStatus.INACTIVE
        instance.full_clean()
        instance.save(update_fields=("is_active", "clinical_status", "updated_at"))
        return instance

    @staticmethod
    @transaction.atomic
    def verify(*, instance, performed_by=None):
        """Verify."""
        if instance.is_deleted:
            raise ValidationError(
                {"detail": "Deleted medical history cannot be verified."}
            )
        if performed_by is None:
            raise ValidationError({"detail": "A verifying actor is required."})
        instance.is_verified = True
        instance.verified_at = timezone.now()
        instance.verified_by = performed_by
        instance.save(
            update_fields=("is_verified", "verified_at", "verified_by", "updated_at")
        )
        return instance


create_medical_history = PatientMedicalHistoryService.create
update_medical_history = PatientMedicalHistoryService.update
delete_medical_history = PatientMedicalHistoryService.delete
restore_medical_history = PatientMedicalHistoryService.restore
activate_medical_history = PatientMedicalHistoryService.activate
deactivate_medical_history = PatientMedicalHistoryService.deactivate
verify_medical_history = PatientMedicalHistoryService.verify


__all__ = (
    "PatientMedicalHistoryService",
    "create_medical_history",
    "update_medical_history",
    "delete_medical_history",
    "restore_medical_history",
    "activate_medical_history",
    "deactivate_medical_history",
    "verify_medical_history",
)

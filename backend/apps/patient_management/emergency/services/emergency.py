"""Domain services for patient emergency records."""

from __future__ import annotations

from django.db import transaction
from django.utils import timezone

from apps.patient_management.emergency.constants import (
    EmergencyContactPriority,
    EmergencyRecordStatus,
)
from apps.patient_management.emergency.exceptions import (
    EmergencyValidationError,
)
from apps.patient_management.emergency.models import EmergencyContact


class EmergencyService:
    """Perform transactional emergency domain mutations."""

    @staticmethod
    @transaction.atomic
    def create(*, organization, patient, data) -> EmergencyContact:
        """Create and normalize an emergency contact."""

        if data.get("priority") == EmergencyContactPriority.PRIMARY:
            EmergencyContact.objects.filter(
                organization=organization,
                patient=patient,
                priority=EmergencyContactPriority.PRIMARY,
                is_deleted=False,
            ).update(
                priority=EmergencyContactPriority.SECONDARY,
            )

        record = EmergencyContact(
            organization=organization,
            patient=patient,
            **data,
        )
        record.normalize()
        record.full_clean()
        record.save()

        return record

    @staticmethod
    @transaction.atomic
    def update(*, record, data) -> EmergencyContact:
        """Update and normalize an emergency contact."""

        for field, value in data.items():
            setattr(record, field, value)

        record.normalize()
        record.full_clean()
        record.save()

        return record

    @staticmethod
    @transaction.atomic
    def delete(*, record) -> EmergencyContact:
        """Soft-delete an emergency contact."""

        record.is_deleted = True
        record.status = EmergencyRecordStatus.DELETED
        record.deleted_at = timezone.now()
        record.save(
            update_fields=(
                "is_deleted",
                "status",
                "deleted_at",
                "updated_at",
            ),
        )

        return record

    @staticmethod
    @transaction.atomic
    def set_primary(*, record) -> EmergencyContact:
        """Make one contact primary within its patient scope."""

        EmergencyContact.objects.filter(
            organization=record.organization,
            patient=record.patient,
            is_deleted=False,
            priority=EmergencyContactPriority.PRIMARY,
        ).exclude(
            id=record.id,
        ).update(
            priority=EmergencyContactPriority.SECONDARY,
        )

        record.priority = EmergencyContactPriority.PRIMARY
        record.status = EmergencyRecordStatus.ACTIVE
        record.full_clean()
        record.save(
            update_fields=(
                "priority",
                "status",
                "updated_at",
            ),
        )

        return record

    @staticmethod
    @transaction.atomic
    def activate(*, record) -> EmergencyContact:
        """Activate an emergency contact."""

        if record.is_deleted:
            raise EmergencyValidationError(
                "A deleted emergency contact cannot be activated.",
            )

        record.status = EmergencyRecordStatus.ACTIVE
        record.save(
            update_fields=(
                "status",
                "updated_at",
            ),
        )

        return record

    @staticmethod
    @transaction.atomic
    def deactivate(*, record) -> EmergencyContact:
        """Deactivate an emergency contact."""

        if record.is_deleted:
            raise EmergencyValidationError(
                "A deleted emergency contact cannot be deactivated.",
            )

        record.status = EmergencyRecordStatus.INACTIVE
        record.save(
            update_fields=(
                "status",
                "updated_at",
            ),
        )

        return record


__all__ = ("EmergencyService",)

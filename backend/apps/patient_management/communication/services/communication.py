"""Domain services for Patient Communication."""

from __future__ import annotations

from typing import Any

from django.utils import timezone

from apps.patient_management.communication.constants import CommunicationStatus
from apps.patient_management.communication.models import PatientCommunication
from apps.patient_management.communication.validators import validate_communication_data


class PatientCommunicationService:
    """Own communication persistence, validation, normalization and lifecycle mutation."""

    @staticmethod
    def create(
        *, validated_data: dict[str, Any], performed_by: Any = None
    ) -> PatientCommunication:
        """Create a communication record."""
        validate_communication_data(validated_data)
        data = dict(validated_data)
        data["created_by"] = performed_by
        return PatientCommunication.objects.create(**data)

    @staticmethod
    def update(
        *,
        instance: PatientCommunication,
        validated_data: dict[str, Any],
        performed_by: Any = None,
    ) -> PatientCommunication:
        """Update a communication record."""
        data = dict(validated_data)
        validate_communication_data({**model_to_dict(instance), **data})
        for field, value in data.items():
            setattr(instance, field, value)
        instance.save()
        return instance

    @staticmethod
    def transition(
        *, instance: PatientCommunication, status: str, performed_by: Any = None
    ) -> PatientCommunication:
        """Apply a supported communication status transition."""
        if instance.is_deleted:
            raise ValueError("Deleted communications cannot change status.")
        now = timezone.now()
        instance.status = status
        if status == CommunicationStatus.SENT:
            instance.sent_at = instance.sent_at or now
        elif status == CommunicationStatus.DELIVERED:
            instance.delivered_at = instance.delivered_at or now
        elif status == CommunicationStatus.READ:
            instance.read_at = instance.read_at or now
        if status == CommunicationStatus.ARCHIVED:
            instance.is_active = False
        else:
            instance.is_active = True
        instance.save()
        return instance

    @staticmethod
    def delete(
        *, instance: PatientCommunication, performed_by: Any = None
    ) -> PatientCommunication:
        """Soft-delete a communication record."""
        instance.is_active = False
        instance.status = CommunicationStatus.ARCHIVED
        instance.save(update_fields=("is_active", "status", "updated_at"))
        instance.delete(user_id=getattr(performed_by, "id", performed_by))
        return instance

    @staticmethod
    def restore(
        *, instance: PatientCommunication, performed_by: Any = None
    ) -> PatientCommunication:
        """Restore a soft-deleted communication as an inactive draft."""
        instance.restore()
        instance.status = CommunicationStatus.DRAFT
        instance.is_active = False
        instance.save(update_fields=("status", "is_active", "updated_at"))
        return instance


def model_to_dict(instance: PatientCommunication) -> dict[str, Any]:
    """Return model fields needed for cross-field validation."""
    return {
        "channel": instance.channel,
        "direction": instance.direction,
        "status": instance.status,
        "content": instance.content,
    }


__all__ = ("PatientCommunicationService",)

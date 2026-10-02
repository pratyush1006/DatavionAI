from __future__ import annotations

from typing import Any
from uuid import UUID

from django.core.exceptions import ValidationError
from django.db import transaction

from apps.clinical.medications.models import Medication
from apps.clinical.medications.services.events import enqueue_event


def _org_id(organization) -> UUID:
    return organization.id


def _validate_organization(instance: Medication, organization) -> None:
    if instance.organization_id != organization.id:
        raise ValidationError("Medication is outside the organization scope.")


@transaction.atomic
def create_medication(
    *, organization, validated_data: dict[str, Any], actor=None
) -> Medication:
    data = dict(validated_data)
    data["organization"] = organization
    medication = Medication.objects.create(**data)
    enqueue_event(
        organization=organization,
        event_type="medication.created",
        aggregate_type="Medication",
        aggregate_id=medication.id,
        payload={
            "medication_id": str(medication.id),
            "medication_code": medication.medication_code,
        },
    )
    return medication


@transaction.atomic
def update_medication(
    *,
    instance: Medication,
    validated_data: dict[str, Any],
    organization=None,
    actor=None,
) -> Medication:
    organization = organization or instance.organization
    locked = Medication.objects.select_for_update().get(pk=instance.pk)
    _validate_organization(locked, organization)
    if locked.is_deleted:
        raise ValidationError("Deleted medications cannot be updated.")
    for key, value in validated_data.items():
        if key == "organization":
            raise ValidationError("Medication organization cannot be changed.")
        setattr(locked, key, value)
    locked.save()
    enqueue_event(
        organization=organization,
        event_type="medication.updated",
        aggregate_type="Medication",
        aggregate_id=locked.id,
        payload={"medication_id": str(locked.id)},
    )
    return locked


@transaction.atomic
def delete_medication(
    *, instance: Medication, organization=None, actor=None
) -> Medication:
    organization = organization or instance.organization
    locked = Medication.objects.select_for_update().get(pk=instance.pk)
    _validate_organization(locked, organization)
    if locked.is_deleted:
        return locked
    locked.soft_delete(getattr(actor, "id", None))
    enqueue_event(
        organization=organization,
        event_type="medication.deleted",
        aggregate_type="Medication",
        aggregate_id=locked.id,
        payload={"medication_id": str(locked.id)},
    )
    return locked


@transaction.atomic
def restore_medication(
    *, instance: Medication, organization=None, actor=None
) -> Medication:
    organization = organization or instance.organization
    locked = Medication.all_objects.select_for_update().get(pk=instance.pk)
    _validate_organization(locked, organization)
    locked.restore()
    enqueue_event(
        organization=organization,
        event_type="medication.restored",
        aggregate_type="Medication",
        aggregate_id=locked.id,
        payload={"medication_id": str(locked.id)},
    )
    return locked

from django.db import transaction
from django.utils import timezone

from apps.clinical.encounters.constants import (
    EncounterStatus,
    is_valid_encounter_transition,
)
from apps.clinical.encounters.exceptions import (
    EncounterTransitionError,
    EncounterValidationError,
)
from apps.clinical.encounters.models import Encounter


class EncounterService:
    @staticmethod
    @transaction.atomic
    def create(
        *, organization, appointment, patient, provider, encounter_number, data=None
    ):
        if appointment.organization_id != organization.id:
            raise EncounterValidationError(
                "Appointment belongs to another organization."
            )
        if patient.organization_id != organization.id:
            raise EncounterValidationError("Patient belongs to another organization.")
        if provider.organization_id != organization.id:
            raise EncounterValidationError("Provider belongs to another organization.")
        if (
            appointment.patient_id != patient.id
            or appointment.provider_id != provider.id
        ):
            raise EncounterValidationError(
                "Encounter patient/provider must match appointment."
            )
        payload = dict(data or {})
        for key in (
            "organization",
            "appointment",
            "patient",
            "provider",
            "status",
            "encounter_number",
        ):
            payload.pop(key, None)
        return Encounter.objects.create(
            organization=organization,
            appointment=appointment,
            patient=patient,
            provider=provider,
            encounter_number=encounter_number,
            status=EncounterStatus.SCHEDULED,
            **payload,
        )

    @staticmethod
    @transaction.atomic
    def update(*, encounter, data):
        protected = {
            "id",
            "organization",
            "appointment",
            "patient",
            "provider",
            "encounter_number",
            "status",
            "started_at",
            "ended_at",
            "duration_minutes",
            "is_deleted",
            "deleted_at",
            "deleted_by_id",
        }
        for key, value in data.items():
            if key not in protected:
                setattr(encounter, key, value)
        encounter.save()
        return encounter

    @staticmethod
    @transaction.atomic
    def transition(*, encounter, target_status, actor_id=None):
        if not is_valid_encounter_transition(encounter.status, target_status):
            raise EncounterTransitionError(
                f"Invalid encounter transition: {encounter.status} -> {target_status}."
            )
        now = timezone.now()
        update_fields = ["status", "updated_at"]
        encounter.status = target_status
        if target_status == EncounterStatus.IN_PROGRESS:
            encounter.started_at = encounter.started_at or now
            update_fields.append("started_at")
        elif target_status in {EncounterStatus.COMPLETED, EncounterStatus.CANCELLED}:
            encounter.ended_at = encounter.ended_at or now
            update_fields.append("ended_at")
            if target_status == EncounterStatus.COMPLETED and encounter.started_at:
                encounter.duration_minutes = max(
                    0,
                    int(
                        (encounter.ended_at - encounter.started_at).total_seconds()
                        // 60
                    ),
                )
                update_fields.append("duration_minutes")
        encounter.save(update_fields=sorted(set(update_fields)))
        return encounter

    @staticmethod
    @transaction.atomic
    def delete(*, encounter, actor_id=None):
        encounter.soft_delete(user_id=actor_id)
        if getattr(encounter, "is_active", True):
            encounter.is_active = False
            encounter.save(update_fields=["is_active", "updated_at"])
        return encounter

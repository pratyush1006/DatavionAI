from django.db import transaction

from apps.clinical.diagnoses.constants import DiagnosisStatus
from apps.clinical.diagnoses.exceptions import DiagnosisValidationError
from apps.clinical.diagnoses.models import Diagnosis


class DiagnosisService:
    @staticmethod
    @transaction.atomic
    def create(*, organization, encounter, diagnosis_code, diagnosis_type, data=None):
        if encounter.organization_id != organization.id:
            raise DiagnosisValidationError("Encounter belongs to another organization.")
        payload = dict(data or {})
        payload.pop("organization", None)
        payload.pop("encounter", None)
        payload.pop("diagnosis_code", None)
        payload.pop("diagnosis_type", None)
        if payload.get("is_primary"):
            Diagnosis.objects.filter(
                organization=organization,
                encounter=encounter,
                is_primary=True,
            ).update(is_primary=False)
        return Diagnosis.objects.create(
            organization=organization,
            encounter=encounter,
            diagnosis_code=diagnosis_code.strip().upper(),
            diagnosis_type=diagnosis_type,
            status=DiagnosisStatus.ACTIVE,
            **payload,
        )

    @staticmethod
    @transaction.atomic
    def update(*, diagnosis, data):
        protected = {
            "id",
            "organization",
            "encounter",
            "diagnosis_code",
            "diagnosis_type",
            "status",
            "is_deleted",
            "deleted_at",
            "deleted_by_id",
        }
        for key, value in data.items():
            if key not in protected:
                setattr(diagnosis, key, value)
        if getattr(diagnosis, "is_primary", False):
            Diagnosis.objects.filter(
                organization=diagnosis.organization,
                encounter=diagnosis.encounter,
                is_primary=True,
            ).exclude(pk=diagnosis.pk).update(is_primary=False)
        diagnosis.save()
        return diagnosis

    @staticmethod
    @transaction.atomic
    def delete(*, diagnosis, actor_id=None):
        diagnosis.soft_delete(user_id=actor_id)
        if getattr(diagnosis, "is_active", True):
            diagnosis.is_active = False
            diagnosis.save(update_fields=["is_active", "updated_at"])
        return diagnosis

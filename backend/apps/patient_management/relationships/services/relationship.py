"""
Domain services for Patient Relationships.

Services own validation, normalization, persistence and domain
invariants. HTTP/RBAC/workflow orchestration stays outside this layer.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from apps.patient_management.relationships.constants import (
    RelationshipStatus,
    VerificationStatus,
)
from apps.patient_management.relationships.models import PatientRelationship


class PatientRelationshipService:
    """Domain service for PatientRelationship."""

    _PROTECTED_FIELDS = frozenset(
        {
            "id",
            "uuid",
            "organization",
            "organization_id",
            "patient",
            "patient_id",
            "created_at",
            "created_by",
            "created_by_id",
            "updated_at",
            "updated_by",
            "updated_by_id",
            "is_deleted",
            "deleted_at",
            "deleted_by",
            "deleted_by_id",
        }
    )

    @classmethod
    def _validate_mutable_fields(
        cls,
        data: Mapping[str, Any],
    ) -> None:
        protected = cls._PROTECTED_FIELDS.intersection(data.keys())
        if protected:
            raise ValidationError(
                dict.fromkeys(
                    sorted(protected),
                    "This field cannot be changed through the Patient Relationship service.",
                )
            )

    @staticmethod
    def _normalize_data(
        data: Mapping[str, Any],
    ) -> dict[str, Any]:
        normalized = dict(data)

        for field in (
            "relationship_name",
            "notes",
        ):
            if field in normalized and normalized[field] is not None:
                normalized[field] = str(normalized[field]).strip()

        return normalized

    @staticmethod
    def _ensure_same_organization(
        *,
        organization_id,
        patient_id,
        related_patient_id,
    ) -> None:
        if not patient_id:
            raise ValidationError({"patient": "Patient is required."})

        from apps.patient_management.patients.models import Patient

        patient = (
            Patient.objects.filter(id=patient_id).only("id", "organization_id").first()
        )
        if patient is None:
            raise ValidationError({"patient": "Patient was not found."})

        if patient.organization_id != organization_id:
            raise ValidationError(
                {
                    "organization": (
                        "The relationship organization must match "
                        "the patient organization."
                    )
                }
            )

        if related_patient_id:
            related_patient = (
                Patient.objects.filter(id=related_patient_id)
                .only("id", "organization_id")
                .first()
            )
            if related_patient is None:
                raise ValidationError(
                    {"related_patient": "Related patient was not found."}
                )

            if related_patient.organization_id != organization_id:
                raise ValidationError(
                    {
                        "related_patient": (
                            "The related patient must belong to the same organization."
                        )
                    }
                )

    @classmethod
    @transaction.atomic
    def create(
        cls,
        *,
        validated_data: Mapping[str, Any],
        performed_by=None,
    ) -> PatientRelationship:
        data = cls._normalize_data(validated_data)
        cls._validate_mutable_fields(data)

        organization = data.get("organization")
        patient = data.get("patient")
        related_patient = data.get("related_patient")

        organization_id = getattr(organization, "id", organization)
        patient_id = getattr(patient, "id", patient)
        related_patient_id = getattr(related_patient, "id", related_patient)

        cls._ensure_same_organization(
            organization_id=organization_id,
            patient_id=patient_id,
            related_patient_id=related_patient_id,
        )

        instance = PatientRelationship(**data)

        if performed_by is not None and hasattr(instance, "created_by_id"):
            instance.created_by = performed_by
            instance.updated_by = performed_by

        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def update(
        cls,
        *,
        instance: PatientRelationship,
        validated_data: Mapping[str, Any],
        performed_by=None,
    ) -> PatientRelationship:
        data = cls._normalize_data(validated_data)
        cls._validate_mutable_fields(data)

        candidate_organization_id = getattr(
            instance,
            "organization_id",
            None,
        )
        candidate_patient_id = getattr(
            instance,
            "patient_id",
            None,
        )
        candidate_related_patient_id = getattr(
            instance,
            "related_patient_id",
            None,
        )

        organization = data.get("organization")
        patient = data.get("patient")
        related_patient = data.get("related_patient")

        if organization is not None:
            candidate_organization_id = getattr(
                organization,
                "id",
                organization,
            )
        if patient is not None:
            candidate_patient_id = getattr(patient, "id", patient)
        if "related_patient" in data:
            candidate_related_patient_id = getattr(
                related_patient,
                "id",
                related_patient,
            )

        cls._ensure_same_organization(
            organization_id=candidate_organization_id,
            patient_id=candidate_patient_id,
            related_patient_id=candidate_related_patient_id,
        )

        for field, value in data.items():
            setattr(instance, field, value)

        if performed_by is not None and hasattr(instance, "updated_by_id"):
            instance.updated_by = performed_by

        instance.full_clean()
        instance.save()
        return instance

    @staticmethod
    @transaction.atomic
    def verify(
        *,
        instance: PatientRelationship,
        performed_by=None,
    ) -> PatientRelationship:
        if instance.verification_status == VerificationStatus.VERIFIED:
            return instance

        if instance.status == RelationshipStatus.TERMINATED:
            raise ValidationError(
                {"status": ("A terminated relationship cannot be verified.")}
            )

        instance.verification_status = VerificationStatus.VERIFIED
        if performed_by is not None and hasattr(instance, "updated_by_id"):
            instance.updated_by = performed_by

        instance.save(
            update_fields=(
                "verification_status",
                "updated_at",
                *(("updated_by",) if hasattr(instance, "updated_by_id") else ()),
            )
        )
        return instance

    @staticmethod
    @transaction.atomic
    def terminate(
        *,
        instance: PatientRelationship,
        performed_by=None,
    ) -> PatientRelationship:
        if instance.status == RelationshipStatus.TERMINATED:
            return instance

        instance.status = RelationshipStatus.TERMINATED
        instance.is_active = False
        instance.is_primary = False
        instance.effective_to = instance.effective_to or timezone.localdate()

        if performed_by is not None and hasattr(instance, "updated_by_id"):
            instance.updated_by = performed_by

        instance.save(
            update_fields=(
                "status",
                "is_active",
                "is_primary",
                "effective_to",
                "updated_at",
                *(("updated_by",) if hasattr(instance, "updated_by_id") else ()),
            )
        )
        return instance

    @staticmethod
    @transaction.atomic
    def set_primary(
        *,
        instance: PatientRelationship,
        performed_by=None,
    ) -> PatientRelationship:
        if instance.is_deleted:
            raise ValidationError(
                {"is_deleted": "Deleted relationships cannot be primary."}
            )
        if not instance.is_active:
            raise ValidationError(
                {"is_active": "Only active relationships can be primary."}
            )
        if instance.status != RelationshipStatus.ACTIVE:
            raise ValidationError(
                {"status": "Only active relationships can be primary."}
            )

        (
            PatientRelationship.objects.select_for_update()
            .filter(
                organization_id=instance.organization_id,
                patient_id=instance.patient_id,
                is_deleted=False,
                is_active=True,
                is_primary=True,
            )
            .exclude(pk=instance.pk)
            .update(is_primary=False)
        )

        instance.is_primary = True

        if performed_by is not None and hasattr(instance, "updated_by_id"):
            instance.updated_by = performed_by

        instance.save(
            update_fields=(
                "is_primary",
                "updated_at",
                *(("updated_by",) if hasattr(instance, "updated_by_id") else ()),
            )
        )
        return instance

    @staticmethod
    @transaction.atomic
    def activate(
        *,
        instance: PatientRelationship,
        performed_by=None,
    ) -> PatientRelationship:
        if instance.status == RelationshipStatus.TERMINATED:
            raise ValidationError(
                {"status": ("Terminated relationships cannot be activated.")}
            )

        instance.is_active = True
        instance.status = RelationshipStatus.ACTIVE

        if performed_by is not None and hasattr(instance, "updated_by_id"):
            instance.updated_by = performed_by

        instance.full_clean()
        instance.save()
        return instance

    @staticmethod
    @transaction.atomic
    def deactivate(
        *,
        instance: PatientRelationship,
        performed_by=None,
    ) -> PatientRelationship:
        if instance.status == RelationshipStatus.TERMINATED:
            return instance

        instance.is_active = False
        instance.status = RelationshipStatus.INACTIVE
        instance.is_primary = False

        if performed_by is not None and hasattr(instance, "updated_by_id"):
            instance.updated_by = performed_by

        instance.full_clean()
        instance.save()
        return instance

    @staticmethod
    @transaction.atomic
    def delete(
        *,
        instance: PatientRelationship,
        performed_by=None,
    ) -> PatientRelationship:
        if instance.is_deleted:
            return instance

        instance.is_active = False
        instance.is_primary = False
        instance.is_deleted = True
        instance.deleted_at = timezone.now()

        if hasattr(instance, "deleted_by_id"):
            instance.deleted_by_id = (
                performed_by.pk if performed_by is not None else None
            )

        if performed_by is not None and hasattr(instance, "updated_by_id"):
            instance.updated_by = performed_by

        update_fields = [
            "is_active",
            "is_primary",
            "is_deleted",
            "deleted_at",
            "updated_at",
        ]
        if hasattr(instance, "deleted_by_id"):
            update_fields.append("deleted_by_id")
        if hasattr(instance, "updated_by_id"):
            update_fields.append("updated_by")

        instance.save(update_fields=update_fields)
        return instance

    @staticmethod
    @transaction.atomic
    def restore(
        *,
        instance: PatientRelationship,
        performed_by=None,
    ) -> PatientRelationship:
        if not instance.is_deleted:
            return instance

        if instance.status == RelationshipStatus.TERMINATED:
            raise ValidationError(
                {
                    "status": (
                        "A terminated relationship cannot be restored to active state."
                    )
                }
            )

        instance.is_deleted = False
        instance.is_active = True
        instance.status = RelationshipStatus.ACTIVE
        instance.deleted_at = None

        if hasattr(instance, "deleted_by_id"):
            instance.deleted_by_id = None
        if performed_by is not None and hasattr(instance, "updated_by_id"):
            instance.updated_by = performed_by

        instance.full_clean()

        update_fields = [
            "is_deleted",
            "is_active",
            "status",
            "deleted_at",
            "updated_at",
        ]
        if hasattr(instance, "deleted_by_id"):
            update_fields.append("deleted_by_id")
        if hasattr(instance, "updated_by_id"):
            update_fields.append("updated_by")

        instance.save(update_fields=update_fields)
        return instance


create_patient_relationship = PatientRelationshipService.create
update_patient_relationship = PatientRelationshipService.update
verify_patient_relationship = PatientRelationshipService.verify
terminate_patient_relationship = PatientRelationshipService.terminate
set_primary_patient_relationship = PatientRelationshipService.set_primary
activate_patient_relationship = PatientRelationshipService.activate
deactivate_patient_relationship = PatientRelationshipService.deactivate
delete_patient_relationship = PatientRelationshipService.delete
restore_patient_relationship = PatientRelationshipService.restore


__all__ = (
    "PatientRelationshipService",
    "activate_patient_relationship",
    "create_patient_relationship",
    "deactivate_patient_relationship",
    "delete_patient_relationship",
    "restore_patient_relationship",
    "set_primary_patient_relationship",
    "terminate_patient_relationship",
    "update_patient_relationship",
    "verify_patient_relationship",
)

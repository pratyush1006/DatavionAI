"""
Domain services for Patient Family Members.

Services own:
- normalization
- validation
- persistence
- lifecycle mutations
- aggregate invariants
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any
from uuid import UUID, uuid4

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.utils import timezone

from apps.patient_management.family_members.constants import FamilyMemberStatus
from apps.patient_management.family_members.models import FamilyMember
from apps.patient_management.patients.models import Patient
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization


class FamilyMemberService:
    """Domain service for Family Member mutations."""

    _PROTECTED_FIELDS = frozenset(
        {
            "id",
            "organization",
            "organization_id",
            "patient",
            "patient_id",
            "family_member_number",
            "created_at",
            "updated_at",
            "is_deleted",
            "deleted_at",
            "deleted_by",
            "is_active",
        }
    )

    _MUTABLE_FIELDS = frozenset(
        {
            "first_name",
            "middle_name",
            "last_name",
            "relationship",
            "gender",
            "date_of_birth",
            "mobile_number",
            "email",
            "blood_group",
            "occupation",
            "address",
            "city",
            "state",
            "postal_code",
            "country",
            "is_living",
            "is_emergency_contact",
            "is_next_of_kin",
            "notes",
        }
    )

    _TEXT_FIELDS = (
        "first_name",
        "middle_name",
        "last_name",
        "mobile_number",
        "email",
        "blood_group",
        "occupation",
        "address",
        "city",
        "state",
        "postal_code",
        "country",
        "notes",
    )

    @classmethod
    def _normalize(cls, data: Mapping[str, Any]) -> dict[str, Any]:
        normalized = dict(data)

        for field in cls._TEXT_FIELDS:
            value = normalized.get(field)

            if isinstance(value, str):
                value = value.strip()

                if field == "email":
                    value = value.lower()

                normalized[field] = value

        return normalized

    @classmethod
    def _validate_fields(
        cls,
        data: Mapping[str, Any],
        *,
        allow_server_fields: bool = False,
    ) -> None:
        errors: dict[str, str] = {}

        protected = set(data).intersection(cls._PROTECTED_FIELDS)

        if allow_server_fields:
            protected.difference_update(
                {
                    "organization",
                    "patient",
                }
            )

        unsupported = set(data).difference(
            cls._MUTABLE_FIELDS
            | ({"organization", "patient"} if allow_server_fields else set())
        )

        for field in sorted(protected):
            errors[field] = (
                "This field cannot be modified through the Family Member service."
            )

        for field in sorted(unsupported):
            errors[field] = (
                "This field is not supported by the Family Member mutation contract."
            )

        if errors:
            raise ValidationError(errors)

    @staticmethod
    def _validate_patient(
        *,
        patient: Patient,
        organization: Organization,
    ) -> None:
        if patient.organization_id != organization.id:
            raise ValidationError(
                {"patient": ("Patient does not belong to the selected organization.")}
            )

    @staticmethod
    def _lock_patient(patient_id: UUID) -> Patient:
        return Patient.objects.select_for_update().get(pk=patient_id)

    @staticmethod
    def _generate_number() -> str:
        return f"FM-{uuid4().hex[:20].upper()}"

    @classmethod
    def _create_instance(
        cls,
        *,
        data: dict[str, Any],
    ) -> FamilyMember:
        for _ in range(3):
            data["family_member_number"] = cls._generate_number()

            try:
                with transaction.atomic():
                    instance = FamilyMember(**data)
                    instance.full_clean()
                    instance.save()

                return instance

            except IntegrityError:
                continue

        raise ValidationError(
            {
                "family_member_number": (
                    "Unable to generate a unique family member number."
                )
            }
        )

    @staticmethod
    def _clear_next_of_kin(
        *,
        patient_id: UUID,
        exclude_id: UUID | None = None,
    ) -> None:
        queryset = FamilyMember.all_objects.filter(
            patient_id=patient_id,
            is_next_of_kin=True,
            is_deleted=False,
        )

        if exclude_id:
            queryset = queryset.exclude(pk=exclude_id)

        queryset.update(
            is_next_of_kin=False,
            updated_at=timezone.now(),
        )

    @classmethod
    @transaction.atomic
    def create(
        cls,
        *,
        organization: Organization,
        patient: Patient,
        validated_data: Mapping[str, Any],
        performed_by: User | None = None,
    ) -> FamilyMember:
        del performed_by

        cls._validate_patient(
            patient=patient,
            organization=organization,
        )

        data = cls._normalize(validated_data)
        cls._validate_fields(
            data,
            allow_server_fields=True,
        )

        locked_patient = cls._lock_patient(patient.id)

        data.pop("organization", None)
        data.pop("organization_id", None)
        data.pop("patient", None)
        data.pop("patient_id", None)

        data["organization"] = organization
        data["patient"] = locked_patient

        if data.get("is_next_of_kin", False):
            cls._clear_next_of_kin(
                patient_id=locked_patient.id,
            )

        return cls._create_instance(data=data)

    @classmethod
    @transaction.atomic
    def update(
        cls,
        *,
        instance: FamilyMember,
        validated_data: Mapping[str, Any],
        performed_by: User | None = None,
    ) -> FamilyMember:
        del performed_by

        if instance.is_deleted:
            raise ValidationError(
                "A deleted family member must be restored before it can be updated."
            )

        data = cls._normalize(validated_data)
        cls._validate_fields(data)

        if not data:
            return instance

        patient = cls._lock_patient(instance.patient_id)

        if patient.organization_id != instance.organization_id:
            raise ValidationError(
                {
                    "patient": (
                        "Patient and family member organization "
                        "boundaries do not match."
                    )
                }
            )

        if data.get("is_next_of_kin", instance.is_next_of_kin):
            cls._clear_next_of_kin(
                patient_id=patient.id,
                exclude_id=instance.id,
            )

        for field, value in data.items():
            setattr(instance, field, value)

        instance.full_clean()
        instance.save(
            update_fields=(*data.keys(), "updated_at"),
        )

        return instance

    @classmethod
    @transaction.atomic
    def mark_next_of_kin(
        cls,
        *,
        instance: FamilyMember,
        performed_by: User | None = None,
    ) -> FamilyMember:
        del performed_by

        if instance.is_deleted:
            raise ValidationError("A deleted family member cannot be made next of kin.")

        if instance.status != FamilyMemberStatus.ACTIVE:
            raise ValidationError("Only an active family member can be next of kin.")

        cls._lock_patient(instance.patient_id)
        cls._clear_next_of_kin(
            patient_id=instance.patient_id,
            exclude_id=instance.id,
        )

        if instance.is_next_of_kin:
            return instance

        instance.is_next_of_kin = True
        instance.full_clean()
        instance.save(
            update_fields=("is_next_of_kin", "updated_at"),
        )

        return instance

    @classmethod
    @transaction.atomic
    def remove_next_of_kin(
        cls,
        *,
        instance: FamilyMember,
        performed_by: User | None = None,
    ) -> FamilyMember:
        del performed_by

        if not instance.is_next_of_kin:
            return instance

        instance.is_next_of_kin = False
        instance.full_clean()
        instance.save(
            update_fields=("is_next_of_kin", "updated_at"),
        )

        return instance

    @classmethod
    @transaction.atomic
    def mark_emergency_contact(
        cls,
        *,
        instance: FamilyMember,
        performed_by: User | None = None,
    ) -> FamilyMember:
        del performed_by

        if instance.is_deleted:
            raise ValidationError(
                "A deleted family member cannot be an emergency contact."
            )

        if instance.is_emergency_contact:
            return instance

        instance.is_emergency_contact = True
        instance.full_clean()
        instance.save(
            update_fields=("is_emergency_contact", "updated_at"),
        )

        return instance

    @classmethod
    @transaction.atomic
    def remove_emergency_contact(
        cls,
        *,
        instance: FamilyMember,
        performed_by: User | None = None,
    ) -> FamilyMember:
        del performed_by

        if not instance.is_emergency_contact:
            return instance

        instance.is_emergency_contact = False
        instance.full_clean()
        instance.save(
            update_fields=("is_emergency_contact", "updated_at"),
        )

        return instance

    @classmethod
    @transaction.atomic
    def activate(
        cls,
        *,
        instance: FamilyMember,
        performed_by: User | None = None,
    ) -> FamilyMember:
        del performed_by

        if instance.is_deleted:
            raise ValidationError("A deleted family member must be restored first.")

        if instance.status == FamilyMemberStatus.ACTIVE and instance.is_active:
            return instance

        instance.status = FamilyMemberStatus.ACTIVE
        instance.is_active = True
        instance.full_clean()
        instance.save(
            update_fields=("status", "is_active", "updated_at"),
        )

        return instance

    @classmethod
    @transaction.atomic
    def deactivate(
        cls,
        *,
        instance: FamilyMember,
        performed_by: User | None = None,
    ) -> FamilyMember:
        del performed_by

        if instance.is_deleted:
            raise ValidationError("A deleted family member cannot be deactivated.")

        if (
            instance.status == FamilyMemberStatus.INACTIVE
            and not instance.is_active
            and not instance.is_next_of_kin
            and not instance.is_emergency_contact
        ):
            return instance

        instance.status = FamilyMemberStatus.INACTIVE
        instance.is_active = False
        instance.is_next_of_kin = False
        instance.is_emergency_contact = False

        instance.full_clean()
        instance.save(
            update_fields=(
                "status",
                "is_active",
                "is_next_of_kin",
                "is_emergency_contact",
                "updated_at",
            ),
        )

        return instance

    @classmethod
    @transaction.atomic
    def restore(
        cls,
        *,
        instance: FamilyMember,
        performed_by: User | None = None,
    ) -> FamilyMember:
        del performed_by

        if not instance.is_deleted:
            return instance

        patient = cls._lock_patient(instance.patient_id)

        if patient.organization_id != instance.organization_id:
            raise ValidationError(
                {
                    "patient": (
                        "Patient and family member organization "
                        "boundaries do not match."
                    )
                }
            )

        # Restore through the model, then validate the complete
        # active aggregate before making the record visible again.
        instance.restore()
        instance.status = FamilyMemberStatus.ACTIVE
        instance.is_active = True

        try:
            instance.full_clean()
            instance.save(
                update_fields=(
                    "is_deleted",
                    "deleted_at",
                    "deleted_by",
                    "status",
                    "is_active",
                    "updated_at",
                ),
            )
        except IntegrityError as exc:
            raise ValidationError(
                {
                    "family_member": (
                        "The family member cannot be restored because "
                        "an active conflicting family member already exists."
                    )
                }
            ) from exc

        return instance

    @classmethod
    @transaction.atomic
    def delete(
        cls,
        *,
        instance: FamilyMember,
        performed_by: User | None = None,
    ) -> FamilyMember:
        if instance.is_deleted:
            return instance

        instance.delete(user=performed_by)
        return instance


create_family_member = FamilyMemberService.create
update_family_member = FamilyMemberService.update
mark_as_next_of_kin = FamilyMemberService.mark_next_of_kin
remove_next_of_kin = FamilyMemberService.remove_next_of_kin
mark_as_emergency_contact = FamilyMemberService.mark_emergency_contact
remove_emergency_contact = FamilyMemberService.remove_emergency_contact
activate_family_member = FamilyMemberService.activate
deactivate_family_member = FamilyMemberService.deactivate
restore_family_member = FamilyMemberService.restore
delete_family_member = FamilyMemberService.delete


__all__ = (
    "FamilyMemberService",
    "activate_family_member",
    "create_family_member",
    "deactivate_family_member",
    "delete_family_member",
    "mark_as_emergency_contact",
    "mark_as_next_of_kin",
    "remove_emergency_contact",
    "remove_next_of_kin",
    "restore_family_member",
    "update_family_member",
)

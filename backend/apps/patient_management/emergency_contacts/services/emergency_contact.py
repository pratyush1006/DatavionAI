"""
Domain services for Patient Emergency Contacts.

Services own:
- normalization
- domain validation
- aggregate invariants
- persistence

Authorization belongs to policies.
Workflow orchestration belongs to workflows.
HTTP concerns belong to the API layer.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, cast
from uuid import UUID, uuid4

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.db.models import Manager
from django.utils import timezone

from apps.patient_management.emergency_contacts.constants import (
    EmergencyContactNumberPrefix,
    EmergencyContactStatus,
    PreferredContactMethod,
)
from apps.patient_management.patients.models import Patient
from apps.platform.accounts.models import User

from ..models import EmergencyContact


class EmergencyContactService:
    """
    Domain service for EmergencyContact mutations.
    """

    _PROTECTED_FIELDS = frozenset(
        {
            "id",
            "organization",
            "organization_id",
            "patient",
            "patient_id",
            "emergency_contact_number",
            "created_at",
            "updated_at",
            "is_deleted",
            "deleted_at",
            "deleted_by",
        }
    )

    _NORMALIZED_TEXT_FIELDS = (
        "first_name",
        "middle_name",
        "last_name",
        "mobile_number",
        "alternate_mobile_number",
        "home_phone",
        "work_phone",
        "email",
        "address_line_1",
        "address_line_2",
        "city",
        "state",
        "postal_code",
        "country",
        "notes",
    )

    _CONTACT_CHANNEL_FIELDS = (
        "mobile_number",
        "alternate_mobile_number",
        "home_phone",
        "work_phone",
        "email",
    )

    @classmethod
    def _normalize_data(
        cls,
        validated_data: Mapping[str, Any],
    ) -> dict[str, Any]:
        data = dict(
            validated_data,
        )

        for field in cls._NORMALIZED_TEXT_FIELDS:
            value = data.get(field)

            if not isinstance(
                value,
                str,
            ):
                continue

            value = value.strip()

            if field == "email":
                value = value.lower()

            data[field] = value

        return data

    @classmethod
    def _validate_mutable_fields(
        cls,
        data: Mapping[str, Any],
    ) -> None:
        protected_fields = frozenset(data) & cls._PROTECTED_FIELDS

        if not protected_fields:
            return

        raise ValidationError(
            dict.fromkeys(
                sorted(protected_fields),
                "This field cannot be modified through the Emergency Contact service.",
            )
        )

    @staticmethod
    def _validate_patient_organization(
        *,
        patient: Patient,
        organization_id: UUID,
    ) -> None:
        if cast(Any, patient).organization_id != organization_id:
            raise ValidationError(
                {"patient": ("Patient does not belong to the selected organization.")}
            )

    @classmethod
    def _validate_contact_channels(
        cls,
        *,
        data: Mapping[str, Any],
    ) -> None:
        has_channel = any(data.get(field) for field in cls._CONTACT_CHANNEL_FIELDS)

        if not has_channel:
            raise ValidationError(
                {"contact": ("At least one emergency contact channel is required.")}
            )

        preferred_method = data.get(
            "preferred_contact_method",
            PreferredContactMethod.MOBILE,
        )

        channel_available = {
            PreferredContactMethod.MOBILE: bool(
                data.get("mobile_number"),
            ),
            PreferredContactMethod.HOME_PHONE: bool(
                data.get("home_phone"),
            ),
            PreferredContactMethod.WORK_PHONE: bool(
                data.get("work_phone"),
            ),
            PreferredContactMethod.EMAIL: bool(
                data.get("email"),
            ),
            PreferredContactMethod.SMS: bool(
                data.get("mobile_number"),
            ),
            PreferredContactMethod.WHATSAPP: bool(
                data.get("mobile_number"),
            ),
            PreferredContactMethod.ANY: has_channel,
        }

        if not channel_available.get(
            preferred_method,
            False,
        ):
            raise ValidationError(
                {
                    "preferred_contact_method": (
                        "The selected preferred contact method "
                        "does not have a corresponding contact "
                        "detail."
                    )
                }
            )

    @staticmethod
    def _validate_date_of_birth(
        *,
        data: Mapping[str, Any],
    ) -> None:
        date_of_birth = data.get(
            "date_of_birth",
        )

        if date_of_birth is not None and date_of_birth > timezone.localdate():
            raise ValidationError(
                {"date_of_birth": ("Date of birth cannot be in the future.")}
            )

    @staticmethod
    def _lock_patient(
        patient_id: UUID,
    ) -> Patient:
        return (
            cast(
                Manager[Patient],
                Patient._default_manager,
            )
            .select_for_update()
            .get(
                pk=patient_id,
            )
        )

    @staticmethod
    def _clear_other_primary_contacts(
        *,
        patient_id: UUID,
        exclude_id: UUID | None = None,
    ) -> None:
        queryset = EmergencyContact.objects.filter(
            patient_id=patient_id,
            is_primary=True,
            is_deleted=False,
        )

        if exclude_id is not None:
            queryset = queryset.exclude(
                pk=exclude_id,
            )

        queryset.update(
            is_primary=False,
            updated_at=timezone.now(),
        )

    @staticmethod
    def _generate_emergency_contact_number() -> str:
        """
        Generate an opaque, collision-resistant business identifier.

        The UUID-derived suffix keeps the value unique without introducing
        a shared sequence or additional locking infrastructure.
        """

        return f"{EmergencyContactNumberPrefix.DEFAULT}-{uuid4().hex[:20].upper()}"

    @classmethod
    def _create_with_generated_number(
        cls,
        *,
        data: dict[str, Any],
    ) -> EmergencyContact:
        """
        Create with a database-backed uniqueness retry.

        Each attempt uses its own savepoint so an IntegrityError does not
        poison the surrounding transaction.
        """

        for _ in range(3):
            data["emergency_contact_number"] = cls._generate_emergency_contact_number()

            try:
                with transaction.atomic():
                    instance = EmergencyContact(
                        **data,
                    )

                    instance.full_clean()

                    instance.save()

                return instance

            except IntegrityError:
                continue

        raise ValidationError(
            {
                "emergency_contact_number": (
                    "Unable to generate a unique emergency contact "
                    "number. Please retry the operation."
                )
            }
        )

    @classmethod
    @transaction.atomic
    def create(
        cls,
        *,
        validated_data: Mapping[str, Any],
        performed_by: User | None = None,
    ) -> EmergencyContact:
        del performed_by

        data = cls._normalize_data(
            validated_data,
        )

        cls._validate_mutable_fields(
            data,
        )

        organization = data.pop(
            "organization",
            None,
        )

        patient = data.pop(
            "patient",
            None,
        )

        if organization is None:
            raise ValidationError({"organization": ("Organization is required.")})

        if patient is None:
            raise ValidationError({"patient": ("Patient is required.")})

        locked_patient = cls._lock_patient(
            patient.pk,
        )

        cls._validate_patient_organization(
            patient=locked_patient,
            organization_id=organization.pk,
        )

        cls._validate_contact_channels(
            data=data,
        )

        cls._validate_date_of_birth(
            data=data,
        )

        data["organization"] = organization
        data["patient"] = locked_patient

        if data.get(
            "is_primary",
            False,
        ):
            cls._clear_other_primary_contacts(
                patient_id=locked_patient.pk,
            )

        return cls._create_with_generated_number(
            data=data,
        )

    @classmethod
    @transaction.atomic
    def update(
        cls,
        *,
        instance: EmergencyContact,
        validated_data: Mapping[str, Any],
        performed_by: User | None = None,
    ) -> EmergencyContact:
        del performed_by

        data = cls._normalize_data(
            validated_data,
        )

        cls._validate_mutable_fields(
            data,
        )

        if not data:
            return instance

        locked_patient = cls._lock_patient(
            instance.patient_id,
        )

        cls._validate_patient_organization(
            patient=locked_patient,
            organization_id=instance.organization_id,
        )

        candidate = {
            field: getattr(
                instance,
                field,
            )
            for field in cls._CONTACT_CHANNEL_FIELDS
        }

        candidate.update(
            {
                field: value
                for field, value in data.items()
                if field in cls._CONTACT_CHANNEL_FIELDS
            }
        )

        preferred_method = data.get(
            "preferred_contact_method",
            instance.preferred_contact_method,
        )

        validation_data = {
            **candidate,
            "preferred_contact_method": preferred_method,
        }

        cls._validate_contact_channels(
            data=validation_data,
        )

        date_of_birth = data.get(
            "date_of_birth",
            instance.date_of_birth,
        )

        if date_of_birth is not None and date_of_birth > timezone.localdate():
            raise ValidationError(
                {"date_of_birth": ("Date of birth cannot be in the future.")}
            )

        for field, value in data.items():
            setattr(
                instance,
                field,
                value,
            )

        instance.full_clean()

        instance.save(
            update_fields=(
                *data.keys(),
                "updated_at",
            ),
        )

        return instance

    @staticmethod
    @transaction.atomic
    def verify(
        *,
        instance: EmergencyContact,
        performed_by: User | None = None,
    ) -> EmergencyContact:
        if instance.is_verified:
            return instance

        instance.is_verified = True
        instance.verified_at = timezone.now()
        instance.verified_by = performed_by

        instance.full_clean()

        instance.save(
            update_fields=(
                "is_verified",
                "verified_at",
                "verified_by",
                "updated_at",
            )
        )

        return instance

    @staticmethod
    @transaction.atomic
    def activate(
        *,
        instance: EmergencyContact,
        performed_by: User | None = None,
    ) -> EmergencyContact:
        del performed_by

        if instance.status == EmergencyContactStatus.ACTIVE:
            return instance

        instance.status = EmergencyContactStatus.ACTIVE

        instance.full_clean()

        instance.save(
            update_fields=(
                "status",
                "updated_at",
            )
        )

        return instance

    @classmethod
    @transaction.atomic
    def deactivate(
        cls,
        *,
        instance: EmergencyContact,
        performed_by: User | None = None,
    ) -> EmergencyContact:
        del performed_by

        was_primary = instance.is_primary

        instance.status = EmergencyContactStatus.INACTIVE
        instance.is_primary = False

        instance.full_clean()

        instance.save(
            update_fields=(
                "status",
                "is_primary",
                "updated_at",
            )
        )

        if was_primary:
            cls._clear_other_primary_contacts(
                patient_id=instance.patient_id,
            )

        return instance

    @staticmethod
    @transaction.atomic
    def block(
        *,
        instance: EmergencyContact,
        performed_by: User | None = None,
    ) -> EmergencyContact:
        del performed_by

        instance.status = EmergencyContactStatus.BLOCKED
        instance.is_primary = False

        instance.full_clean()

        instance.save(
            update_fields=(
                "status",
                "is_primary",
                "updated_at",
            )
        )

        return instance

    @classmethod
    @transaction.atomic
    def set_primary(
        cls,
        *,
        instance: EmergencyContact,
        performed_by: User | None = None,
    ) -> EmergencyContact:
        del performed_by

        if instance.status != EmergencyContactStatus.ACTIVE:
            raise ValidationError(
                {"status": ("Only an active emergency contact can be made primary.")}
            )

        cls._validate_contact_channels(
            data={
                "mobile_number": instance.mobile_number,
                "alternate_mobile_number": (instance.alternate_mobile_number),
                "home_phone": instance.home_phone,
                "work_phone": instance.work_phone,
                "email": instance.email,
                "preferred_contact_method": (instance.preferred_contact_method),
            }
        )

        patient = cls._lock_patient(
            instance.patient_id,
        )

        cls._validate_patient_organization(
            patient=patient,
            organization_id=instance.organization_id,
        )

        cls._clear_other_primary_contacts(
            patient_id=patient.pk,
            exclude_id=instance.id,
        )

        instance.is_primary = True

        instance.full_clean()

        instance.save(
            update_fields=(
                "is_primary",
                "updated_at",
            )
        )

        return instance

    @staticmethod
    @transaction.atomic
    def delete(
        *,
        instance: EmergencyContact,
        performed_by: User | None = None,
    ) -> None:
        instance.delete(
            user=performed_by,
        )


create_emergency_contact = EmergencyContactService.create
update_emergency_contact = EmergencyContactService.update
verify_emergency_contact = EmergencyContactService.verify
activate_emergency_contact = EmergencyContactService.activate
deactivate_emergency_contact = EmergencyContactService.deactivate
block_emergency_contact = EmergencyContactService.block
set_primary_emergency_contact = EmergencyContactService.set_primary
delete_emergency_contact = EmergencyContactService.delete


__all__ = (
    "EmergencyContactService",
    "activate_emergency_contact",
    "block_emergency_contact",
    "create_emergency_contact",
    "deactivate_emergency_contact",
    "delete_emergency_contact",
    "set_primary_emergency_contact",
    "update_emergency_contact",
    "verify_emergency_contact",
)

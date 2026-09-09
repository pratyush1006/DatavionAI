"""
Domain service for Patient Addresses.

Responsibilities
----------------
- Normalization.
- Domain validation.
- Duplicate detection.
- Primary-address invariant.
- Lifecycle mutation.
- Persistence.

The service does not perform RBAC, HTTP handling, workflow orchestration,
or domain-event publication.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.core.exceptions import ValidationError
from django.db import transaction

from apps.patient_management.addresses.constants import (
    AddressStatus,
)
from apps.patient_management.addresses.exceptions import (
    DuplicateAddressError,
    InvalidAddressError,
)
from apps.patient_management.addresses.models import Address
from apps.patient_management.patients.models import Patient
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization


class AddressService:
    """
    Write-side Patient Address domain service.
    """

    @staticmethod
    def _normalize(
        data: Mapping[str, Any],
    ) -> dict[str, Any]:
        normalized = dict(data)

        for field in (
            "line_1",
            "line_2",
            "city",
            "state",
            "country",
            "postal_code",
        ):
            value = normalized.get(field)

            if isinstance(value, str):
                normalized[field] = value.strip()

        return normalized

    @staticmethod
    def _validate_required(
        *,
        data: Mapping[str, Any],
    ) -> None:
        required = (
            "line_1",
            "city",
            "state",
            "country",
            "postal_code",
        )

        errors: dict[str, str] = {}

        for field in required:
            value = data.get(field)

            if value is None or str(value).strip() == "":
                errors[field] = "This field is required."

        if errors:
            raise ValidationError(errors)

    @staticmethod
    def _validate_organization_boundary(
        *,
        organization: Organization,
        patient: Patient,
    ) -> None:
        if patient.organization_id != organization.pk:
            raise ValidationError(
                {
                    "patient": (
                        "The patient must belong to the selected organization."
                    ),
                },
            )

    @staticmethod
    def _ensure_not_duplicate(
        *,
        organization: Organization,
        patient: Patient,
        data: Mapping[str, Any],
        instance: Address | None = None,
    ) -> None:
        queryset = Address.objects.filter(
            organization_id=organization.pk,
            patient_id=patient.pk,
            address_type=data.get("address_type"),
            address_use=data.get("address_use"),
            line_1=data.get("line_1"),
            line_2=data.get(
                "line_2",
                "",
            ),
            city=data.get("city"),
            state=data.get("state"),
            country=data.get("country"),
            postal_code=data.get("postal_code"),
        )

        if instance is not None:
            queryset = queryset.exclude(
                pk=instance.pk,
            )

        if queryset.exists():
            raise DuplicateAddressError()

    @staticmethod
    def _clear_other_primary_addresses(
        *,
        patient: Patient,
        address_type: str,
        exclude_id: Any | None = None,
    ) -> None:
        queryset = Address.objects.filter(
            patient_id=patient.pk,
            address_type=address_type,
            is_primary=True,
        )

        if exclude_id is not None:
            queryset = queryset.exclude(
                pk=exclude_id,
            )

        queryset.update(
            is_primary=False,
        )

    @classmethod
    @transaction.atomic
    def create(
        cls,
        *,
        validated_data: Mapping[str, Any],
        performed_by: User | None = None,
    ) -> Address:
        data = cls._normalize(
            validated_data,
        )

        organization = data.get(
            "organization",
        )
        patient = data.get(
            "patient",
        )

        if not isinstance(
            organization,
            Organization,
        ):
            raise ValidationError(
                {
                    "organization": ("A valid organization is required."),
                },
            )

        if not isinstance(
            patient,
            Patient,
        ):
            raise ValidationError(
                {
                    "patient": ("A valid patient is required."),
                },
            )

        cls._validate_organization_boundary(
            organization=organization,
            patient=patient,
        )

        cls._validate_required(
            data=data,
        )

        cls._ensure_not_duplicate(
            organization=organization,
            patient=patient,
            data=data,
        )

        if data.get(
            "is_primary",
            False,
        ):
            cls._clear_other_primary_addresses(
                patient=patient,
                address_type=data["address_type"],
            )

        instance = Address.objects.create(
            **data,
        )

        instance.full_clean()
        instance.refresh_from_db()

        return instance

    @classmethod
    @transaction.atomic
    def update(
        cls,
        *,
        instance: Address,
        validated_data: Mapping[str, Any],
        performed_by: User | None = None,
    ) -> Address:
        data = cls._normalize(
            validated_data,
        )

        if not data:
            return instance

        forbidden_fields = {
            "organization",
            "patient",
            "status",
            "source",
        }

        forbidden = forbidden_fields.intersection(
            data.keys(),
        )

        if forbidden:
            raise InvalidAddressError(
                (
                    "These fields cannot be changed through the "
                    "address update workflow: " + ", ".join(sorted(forbidden))
                ),
            )

        candidate = {
            "address_type": data.get(
                "address_type",
                instance.address_type,
            ),
            "address_use": data.get(
                "address_use",
                instance.address_use,
            ),
            "line_1": data.get(
                "line_1",
                instance.line_1,
            ),
            "line_2": data.get(
                "line_2",
                instance.line_2,
            ),
            "city": data.get(
                "city",
                instance.city,
            ),
            "state": data.get(
                "state",
                instance.state,
            ),
            "country": data.get(
                "country",
                instance.country,
            ),
            "postal_code": data.get(
                "postal_code",
                instance.postal_code,
            ),
        }

        cls._validate_required(
            data=candidate,
        )

        cls._ensure_not_duplicate(
            organization=instance.organization,
            patient=instance.patient,
            data=candidate,
            instance=instance,
        )

        previous_type = instance.address_type

        for field, value in data.items():
            setattr(
                instance,
                field,
                value,
            )

        if instance.is_primary:
            cls._clear_other_primary_addresses(
                patient=instance.patient,
                address_type=instance.address_type,
                exclude_id=instance.pk,
            )

        elif previous_type != instance.address_type and instance.is_primary is False:
            cls._clear_other_primary_addresses(
                patient=instance.patient,
                address_type=previous_type,
            )

        instance.full_clean()
        instance.save()
        instance.refresh_from_db()

        return instance

    @classmethod
    @transaction.atomic
    def verify(
        cls,
        *,
        instance: Address,
        performed_by: User | None = None,
    ) -> Address:
        if instance.status == AddressStatus.INACTIVE:
            raise InvalidAddressError(
                "An inactive address cannot be verified.",
            )

        if instance.status == AddressStatus.VERIFIED:
            return instance

        instance.status = AddressStatus.VERIFIED
        instance.full_clean()
        instance.save()
        instance.refresh_from_db()

        return instance

    @classmethod
    @transaction.atomic
    def activate(
        cls,
        *,
        instance: Address,
        performed_by: User | None = None,
    ) -> Address:
        if instance.status in (
            AddressStatus.ACTIVE,
            AddressStatus.VERIFIED,
        ):
            return instance

        instance.status = AddressStatus.ACTIVE
        instance.full_clean()
        instance.save()
        instance.refresh_from_db()

        return instance

    @classmethod
    @transaction.atomic
    def deactivate(
        cls,
        *,
        instance: Address,
        performed_by: User | None = None,
    ) -> Address:
        if instance.status == AddressStatus.INACTIVE:
            return instance

        instance.status = AddressStatus.INACTIVE
        instance.is_primary = False
        instance.full_clean()
        instance.save()
        instance.refresh_from_db()

        return instance

    @classmethod
    @transaction.atomic
    def set_primary(
        cls,
        *,
        instance: Address,
        performed_by: User | None = None,
    ) -> Address:
        if instance.status not in (
            AddressStatus.ACTIVE,
            AddressStatus.VERIFIED,
        ):
            raise InvalidAddressError(
                "Only active or verified addresses can be primary.",
            )

        cls._clear_other_primary_addresses(
            patient=instance.patient,
            address_type=instance.address_type,
            exclude_id=instance.pk,
        )

        instance.is_primary = True
        instance.full_clean()
        instance.save()
        instance.refresh_from_db()

        return instance

    @staticmethod
    @transaction.atomic
    def delete(
        *,
        instance: Address,
        performed_by: User | None = None,
    ) -> None:
        instance.delete()


create_address = AddressService.create
update_address = AddressService.update
verify_address = AddressService.verify
activate_address = AddressService.activate
deactivate_address = AddressService.deactivate
set_primary_address = AddressService.set_primary
delete_address = AddressService.delete


__all__ = (
    "AddressService",
    "activate_address",
    "create_address",
    "deactivate_address",
    "delete_address",
    "set_primary_address",
    "update_address",
    "verify_address",
)

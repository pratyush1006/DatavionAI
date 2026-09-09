"""
Patient Identifier domain services.

Responsibilities
----------------
- Patient Identifier aggregate persistence.
- Identifier lifecycle transitions.
- Verification history.
- Primary identifier management.
- Aggregate validation.

Non-responsibilities
--------------------
- HTTP/API concerns.
- RBAC authorization.
- Workflow orchestration.
- Domain event publication.
- Background task dispatch.

All externally initiated mutations should enter through an Identifier
workflow. These services are the persistence/domain boundary used by those
workflows.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from apps.patient_management.identifiers.constants import (
    IdentifierStatus,
    VerificationStatus,
)
from apps.patient_management.identifiers.models import (
    IdentifierVerification,
    PatientIdentifier,
)
from apps.platform.accounts.models import User


class PatientIdentifierService:
    """
    Domain service for Patient Identifier aggregate mutations.
    """

    @staticmethod
    @transaction.atomic
    def create(
        *,
        validated_data: Mapping[str, Any],
        performed_by: User | None = None,
    ) -> PatientIdentifier:
        """
        Create a patient identifier.

        Organization and patient ownership must already have been resolved
        by the workflow/API layer. Model validation remains authoritative.
        """
        data = dict(validated_data)

        patient = data.get("patient")
        organization = data.get("organization")

        if patient is None:
            raise ValidationError(
                {
                    "patient": "A patient is required.",
                },
            )

        if organization is None:
            raise ValidationError(
                {
                    "organization": "An organization is required.",
                },
            )

        if patient.organization_id != organization.pk:
            raise ValidationError(
                {
                    "patient": (
                        "The patient must belong to the selected organization."
                    ),
                },
            )

        instance = PatientIdentifier(**data)

        instance.full_clean()
        instance.save()

        return instance

    @staticmethod
    @transaction.atomic
    def update(
        *,
        instance: PatientIdentifier,
        validated_data: Mapping[str, Any],
        performed_by: User | None = None,
    ) -> PatientIdentifier:
        """
        Update mutable identifier fields.

        Ownership fields cannot be changed through this service.
        """
        data = dict(validated_data)

        data.pop("organization", None)
        data.pop("patient", None)

        for field, value in data.items():
            setattr(
                instance,
                field,
                value,
            )

        instance.full_clean()
        instance.save()

        return instance

    @staticmethod
    @transaction.atomic
    def verify(
        *,
        instance: PatientIdentifier,
        status: str,
        verification_source: str,
        reference_number: str = "",
        remarks: str = "",
        performed_by: User,
    ) -> PatientIdentifier:
        """
        Record a verification decision and synchronize the aggregate state.

        Every verification attempt creates an immutable history record.
        """
        allowed_statuses = {
            VerificationStatus.VERIFIED,
            VerificationStatus.REJECTED,
        }

        if status not in allowed_statuses:
            raise ValidationError(
                {
                    "status": ("Verification status must be VERIFIED or REJECTED."),
                },
            )

        verified_at = timezone.now() if status == VerificationStatus.VERIFIED else None

        verification = IdentifierVerification(
            identifier=instance,
            status=status,
            verification_source=verification_source,
            reference_number=reference_number,
            remarks=remarks,
            verified_by=performed_by,
            verified_at=verified_at,
        )

        verification.full_clean()
        verification.save()

        instance.verification_status = status
        instance.verified_by = (
            performed_by if status == VerificationStatus.VERIFIED else None
        )
        instance.verified_at = verified_at

        instance.save(
            update_fields=(
                "verification_status",
                "verified_by",
                "verified_at",
                "updated_at",
            ),
        )

        return instance

    @staticmethod
    @transaction.atomic
    def activate(
        *,
        instance: PatientIdentifier,
        performed_by: User | None = None,
    ) -> PatientIdentifier:
        """
        Activate an identifier.

        The operation is idempotent.
        """
        if instance.status == IdentifierStatus.ACTIVE:
            return instance

        if instance.status == IdentifierStatus.REVOKED:
            raise ValidationError(
                {
                    "status": "A revoked identifier cannot be activated.",
                },
            )

        instance.status = IdentifierStatus.ACTIVE

        instance.save(
            update_fields=(
                "status",
                "updated_at",
            ),
        )

        return instance

    @staticmethod
    @transaction.atomic
    def deactivate(
        *,
        instance: PatientIdentifier,
        performed_by: User | None = None,
    ) -> PatientIdentifier:
        """
        Deactivate an identifier.

        The operation is idempotent.
        """
        if instance.status == IdentifierStatus.INACTIVE:
            return instance

        if instance.status == IdentifierStatus.REVOKED:
            raise ValidationError(
                {
                    "status": "A revoked identifier cannot be deactivated.",
                },
            )

        instance.status = IdentifierStatus.INACTIVE

        instance.save(
            update_fields=(
                "status",
                "updated_at",
            ),
        )

        return instance

    @staticmethod
    @transaction.atomic
    def revoke(
        *,
        instance: PatientIdentifier,
        performed_by: User | None = None,
    ) -> PatientIdentifier:
        """
        Permanently revoke an identifier.

        Revocation is idempotent and cannot be reversed through activation.
        """
        if instance.status == IdentifierStatus.REVOKED:
            return instance

        instance.status = IdentifierStatus.REVOKED

        if instance.is_primary:
            instance.is_primary = False

            instance.save(
                update_fields=(
                    "status",
                    "is_primary",
                    "updated_at",
                ),
            )
        else:
            instance.save(
                update_fields=(
                    "status",
                    "updated_at",
                ),
            )

        return instance

    @staticmethod
    @transaction.atomic
    def set_primary(
        *,
        instance: PatientIdentifier,
        performed_by: User | None = None,
    ) -> PatientIdentifier:
        """
        Make an identifier primary for its patient and identifier type.

        Existing primary identifiers of the same patient/type are cleared
        in the same transaction.
        """
        if instance.status in {
            IdentifierStatus.REVOKED,
            IdentifierStatus.EXPIRED,
        }:
            raise ValidationError(
                {
                    "status": (
                        "Only active or inactive identifiers may be "
                        "designated as primary."
                    ),
                },
            )

        (
            PatientIdentifier.objects.select_for_update()
            .filter(
                patient_id=instance.patient_id,
                identifier_type=instance.identifier_type,
                is_primary=True,
            )
            .exclude(
                pk=instance.pk,
            )
            .update(
                is_primary=False,
            )
        )

        if not instance.is_primary:
            instance.is_primary = True

            instance.save(
                update_fields=(
                    "is_primary",
                    "updated_at",
                ),
            )

        return instance

    @staticmethod
    @transaction.atomic
    def delete(
        *,
        instance: PatientIdentifier,
        performed_by: User | None = None,
    ) -> None:
        """
        Delete an identifier through the model's configured lifecycle.

        The service deliberately avoids direct queryset deletion so the
        project's model lifecycle remains authoritative.
        """
        instance.delete()


create_patient_identifier = PatientIdentifierService.create
update_patient_identifier = PatientIdentifierService.update
verify_patient_identifier = PatientIdentifierService.verify
activate_patient_identifier = PatientIdentifierService.activate
deactivate_patient_identifier = PatientIdentifierService.deactivate
revoke_patient_identifier = PatientIdentifierService.revoke
set_primary_patient_identifier = PatientIdentifierService.set_primary
delete_patient_identifier = PatientIdentifierService.delete


__all__ = (
    "PatientIdentifierService",
    "activate_patient_identifier",
    "create_patient_identifier",
    "deactivate_patient_identifier",
    "delete_patient_identifier",
    "revoke_patient_identifier",
    "set_primary_patient_identifier",
    "update_patient_identifier",
    "verify_patient_identifier",
)

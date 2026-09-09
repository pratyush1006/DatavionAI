"""
Domain service layer for Patient Registration.

Responsibilities
----------------
- Patient Registration aggregate persistence.
- Registration number generation.
- Organization/patient consistency validation.
- Registration lifecycle validation and mutation.
- Aggregate-level validation and normalization.

Non-responsibilities
--------------------
- HTTP/API handling.
- RBAC/permission evaluation.
- Workflow orchestration.
- Domain event publication.
- Background task execution.

All external mutations should enter through the corresponding workflow.
Workflows are responsible for authorization, actor resolution, orchestration,
and domain-event publication after commit.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from apps.common.exceptions import ValidationException
from apps.patient_management.registration.constants import (
    CancellationReason,
    RegistrationNumberPrefix,
    RegistrationStatus,
)
from apps.patient_management.registration.models import (
    PatientRegistration,
)
from apps.platform.organizations.models import Organization


class PatientRegistrationService:
    """
    Domain service for Patient Registration.

    The service deliberately does not perform authorization or publish
    domain events. Those responsibilities belong to policies and workflows.
    """

    _ALLOWED_TRANSITIONS: dict[str, frozenset[str]] = {
        RegistrationStatus.DRAFT: frozenset(
            {
                RegistrationStatus.PENDING_VERIFICATION,
                RegistrationStatus.VERIFIED,
                RegistrationStatus.REGISTERED,
                RegistrationStatus.CANCELLED,
                RegistrationStatus.REJECTED,
            }
        ),
        RegistrationStatus.PENDING_VERIFICATION: frozenset(
            {
                RegistrationStatus.VERIFIED,
                RegistrationStatus.CANCELLED,
                RegistrationStatus.REJECTED,
            }
        ),
        RegistrationStatus.VERIFIED: frozenset(
            {
                RegistrationStatus.REGISTERED,
                RegistrationStatus.CHECKED_IN,
                RegistrationStatus.NO_SHOW,
                RegistrationStatus.CANCELLED,
                RegistrationStatus.REJECTED,
            }
        ),
        RegistrationStatus.REGISTERED: frozenset(
            {
                RegistrationStatus.CHECKED_IN,
                RegistrationStatus.NO_SHOW,
                RegistrationStatus.CANCELLED,
                RegistrationStatus.REJECTED,
            }
        ),
        RegistrationStatus.CHECKED_IN: frozenset(
            {
                RegistrationStatus.COMPLETED,
                RegistrationStatus.CANCELLED,
            }
        ),
        RegistrationStatus.COMPLETED: frozenset(),
        RegistrationStatus.CANCELLED: frozenset(),
        RegistrationStatus.REJECTED: frozenset(),
        RegistrationStatus.NO_SHOW: frozenset(),
    }

    _PROTECTED_UPDATE_FIELDS = frozenset(
        {
            "registration_number",
            "registration_status",
            "verified",
            "verified_at",
            "verified_by",
            "checked_in_at",
            "completed_at",
            "cancellation_reason",
            "cancellation_notes",
            "organization",
            "organization_id",
            "patient",
            "patient_id",
        }
    )

    @staticmethod
    @transaction.atomic
    def create(
        *,
        validated_data: Mapping[str, Any],
        performed_by: Any | None = None,
    ) -> PatientRegistration:
        """
        Create a Patient Registration aggregate.

        Registration lifecycle state, verification state, timestamps,
        ownership, and registration number are controlled by the domain
        service and are never accepted from the client.
        """

        data = dict(validated_data)

        organization = data.get("organization")
        patient = data.get("patient")

        if organization is None:
            raise ValidationException(
                "Organization is required to create a registration.",
            )

        if patient is None:
            raise ValidationException(
                "Patient is required to create a registration.",
            )

        PatientRegistrationService._validate_organization_patient(
            organization=organization,
            patient=patient,
        )

        data.pop("registration_number", None)
        data.pop("registration_status", None)
        data.pop("verified", None)
        data.pop("verified_at", None)
        data.pop("verified_by", None)
        data.pop("checked_in_at", None)
        data.pop("completed_at", None)
        data.pop("cancellation_reason", None)
        data.pop("cancellation_notes", None)

        data["registration_status"] = RegistrationStatus.DRAFT
        data["verified"] = False
        data["verified_at"] = None
        data["verified_by"] = None
        data["checked_in_at"] = None
        data["completed_at"] = None
        data["cancellation_reason"] = ""
        data["cancellation_notes"] = ""

        data["registration_number"] = (
            PatientRegistrationService._generate_registration_number(
                organization=organization,
            )
        )

        registration = PatientRegistration(
            **data,
        )

        try:
            registration.full_clean()
        except ValidationError as exc:
            raise ValidationException(
                PatientRegistrationService._format_validation_error(
                    exc,
                ),
            ) from exc

        registration.save()

        return registration

    @staticmethod
    @transaction.atomic
    def update(
        *,
        instance: PatientRegistration,
        validated_data: Mapping[str, Any],
        performed_by: Any | None = None,
    ) -> PatientRegistration:
        """
        Update mutable registration data.

        Lifecycle state, verification state, ownership, timestamps, and
        registration number cannot be modified through generic update.
        """

        data = dict(validated_data)

        protected_fields = PatientRegistrationService._PROTECTED_UPDATE_FIELDS & set(
            data.keys()
        )

        if protected_fields:
            fields = ", ".join(
                sorted(protected_fields),
            )

            raise ValidationException(
                "The following fields can only be changed through their "
                f"dedicated lifecycle workflows: {fields}.",
            )

        if not data:
            return instance

        for field, value in data.items():
            setattr(
                instance,
                field,
                value,
            )

        try:
            instance.full_clean()
        except ValidationError as exc:
            raise ValidationException(
                PatientRegistrationService._format_validation_error(
                    exc,
                ),
            ) from exc

        instance.save(
            update_fields=[
                *data.keys(),
                "updated_at",
            ],
        )

        return instance

    @staticmethod
    @transaction.atomic
    def verify(
        *,
        instance: PatientRegistration,
        performed_by: Any,
    ) -> PatientRegistration:
        """
        Verify a registration.
        """

        if performed_by is None:
            raise ValidationException(
                "An actor is required to verify a registration.",
            )

        if instance.verified:
            raise ValidationException(
                "Registration is already verified.",
            )

        PatientRegistrationService._ensure_transition(
            instance=instance,
            target_status=RegistrationStatus.VERIFIED,
        )

        now = timezone.now()

        instance.verified = True
        instance.verified_at = now
        instance.verified_by = performed_by
        instance.registration_status = RegistrationStatus.VERIFIED

        instance.save(
            update_fields=[
                "verified",
                "verified_at",
                "verified_by",
                "registration_status",
                "updated_at",
            ],
        )

        return instance

    @staticmethod
    @transaction.atomic
    def check_in(
        *,
        instance: PatientRegistration,
        performed_by: Any,
    ) -> PatientRegistration:
        """
        Check in a verified registration.

        The canonical workflow set does not expose a separate registration
        workflow. Therefore a VERIFIED registration may transition directly
        to CHECKED_IN. REGISTERED registrations remain valid for existing
        data and can also transition to CHECKED_IN.
        """

        if performed_by is None:
            raise ValidationException(
                "An actor is required to check in a registration.",
            )

        if not instance.verified:
            raise ValidationException(
                "Registration must be verified before check-in.",
            )

        PatientRegistrationService._ensure_transition(
            instance=instance,
            target_status=RegistrationStatus.CHECKED_IN,
        )

        now = timezone.now()

        instance.registration_status = RegistrationStatus.CHECKED_IN
        instance.checked_in_at = now

        instance.save(
            update_fields=[
                "registration_status",
                "checked_in_at",
                "updated_at",
            ],
        )

        return instance

    @staticmethod
    @transaction.atomic
    def complete(
        *,
        instance: PatientRegistration,
        performed_by: Any,
    ) -> PatientRegistration:
        """
        Complete a checked-in registration.
        """

        if performed_by is None:
            raise ValidationException(
                "An actor is required to complete a registration.",
            )

        PatientRegistrationService._ensure_transition(
            instance=instance,
            target_status=RegistrationStatus.COMPLETED,
        )

        if instance.checked_in_at is None:
            raise ValidationException(
                "Registration must have a check-in timestamp before completion.",
            )

        now = timezone.now()

        instance.registration_status = RegistrationStatus.COMPLETED
        instance.completed_at = now

        instance.save(
            update_fields=[
                "registration_status",
                "completed_at",
                "updated_at",
            ],
        )

        return instance

    @staticmethod
    @transaction.atomic
    def cancel(
        *,
        instance: PatientRegistration,
        reason: str,
        notes: str = "",
        performed_by: Any | None = None,
    ) -> PatientRegistration:
        """
        Cancel a registration.
        """

        normalized_reason = PatientRegistrationService._normalize_required_text(
            reason,
            field_name="Cancellation reason",
        )

        normalized_notes = PatientRegistrationService._normalize_optional_text(
            notes,
        )

        PatientRegistrationService._validate_cancellation_reason(
            normalized_reason,
        )

        PatientRegistrationService._ensure_transition(
            instance=instance,
            target_status=RegistrationStatus.CANCELLED,
        )

        instance.registration_status = RegistrationStatus.CANCELLED
        instance.cancellation_reason = normalized_reason
        instance.cancellation_notes = normalized_notes

        try:
            instance.full_clean(
                exclude=[
                    "registration_number",
                ],
            )
        except ValidationError as exc:
            raise ValidationException(
                PatientRegistrationService._format_validation_error(
                    exc,
                ),
            ) from exc

        instance.save(
            update_fields=[
                "registration_status",
                "cancellation_reason",
                "cancellation_notes",
                "updated_at",
            ],
        )

        return instance

    @staticmethod
    @transaction.atomic
    def reject(
        *,
        instance: PatientRegistration,
        performed_by: Any,
    ) -> PatientRegistration:
        """
        Reject a registration.
        """

        if performed_by is None:
            raise ValidationException(
                "An actor is required to reject a registration.",
            )

        PatientRegistrationService._ensure_transition(
            instance=instance,
            target_status=RegistrationStatus.REJECTED,
        )

        instance.registration_status = RegistrationStatus.REJECTED

        instance.save(
            update_fields=[
                "registration_status",
                "updated_at",
            ],
        )

        return instance

    @staticmethod
    @transaction.atomic
    def no_show(
        *,
        instance: PatientRegistration,
        performed_by: Any,
    ) -> PatientRegistration:
        """
        Mark a verified or registered registration as no-show.
        """

        if performed_by is None:
            raise ValidationException(
                "An actor is required to mark a registration as no-show.",
            )

        PatientRegistrationService._ensure_transition(
            instance=instance,
            target_status=RegistrationStatus.NO_SHOW,
        )

        instance.registration_status = RegistrationStatus.NO_SHOW

        instance.save(
            update_fields=[
                "registration_status",
                "updated_at",
            ],
        )

        return instance

    @staticmethod
    @transaction.atomic
    def delete(
        *,
        instance: PatientRegistration,
        performed_by: Any | None = None,
    ) -> None:
        """
        Delete a registration aggregate.

        BaseModel supplies the persistence deletion behavior. Authorization
        belongs to the workflow and policy layers.
        """

        instance.delete()

    @staticmethod
    def _validate_organization_patient(
        *,
        organization: Any,
        patient: Any,
    ) -> None:
        """
        Ensure the patient belongs to the registration organization.
        """

        organization_id = getattr(
            organization,
            "pk",
            None,
        )

        patient_organization_id = getattr(
            patient,
            "organization_id",
            None,
        )

        if organization_id is None:
            raise ValidationException(
                "A valid organization is required.",
            )

        if patient_organization_id is None:
            raise ValidationException(
                "Patient organization information is unavailable.",
            )

        if patient_organization_id != organization_id:
            raise ValidationException(
                "Patient and registration organization must match.",
            )

    @staticmethod
    def _ensure_transition(
        *,
        instance: PatientRegistration,
        target_status: str,
    ) -> None:
        """
        Validate an explicit lifecycle transition.
        """

        current_status = instance.registration_status

        if current_status == target_status:
            raise ValidationException(
                f"Registration is already in {target_status} status.",
            )

        allowed = PatientRegistrationService._ALLOWED_TRANSITIONS.get(
            current_status,
            frozenset(),
        )

        if target_status not in allowed:
            raise ValidationException(
                f"Registration cannot transition from "
                f"{current_status} to {target_status}.",
            )

    @staticmethod
    def _normalize_required_text(
        value: Any,
        *,
        field_name: str,
    ) -> str:
        """
        Normalize required text input.
        """

        if value is None:
            raise ValidationException(
                f"{field_name} is required.",
            )

        normalized = str(value).strip()

        if not normalized:
            raise ValidationException(
                f"{field_name} is required.",
            )

        return normalized

    @staticmethod
    def _normalize_optional_text(
        value: Any,
    ) -> str:
        """
        Normalize optional text input.
        """

        if value is None:
            return ""

        return str(value).strip()

    @staticmethod
    def _validate_cancellation_reason(
        reason: str,
    ) -> None:
        """
        Validate cancellation reason against the canonical enum.
        """

        valid_reasons = {choice for choice, _label in CancellationReason.choices}

        if reason not in valid_reasons:
            raise ValidationException(
                "Invalid cancellation reason.",
            )

    @staticmethod
    def _format_validation_error(
        exc: ValidationError,
    ) -> str:
        """
        Convert Django ValidationError into a stable domain-level message.
        """

        if hasattr(exc, "message_dict") and exc.message_dict:
            messages: list[str] = []

            for field, errors in exc.message_dict.items():
                for error in errors:
                    messages.append(
                        f"{field}: {error}",
                    )

            return "; ".join(messages)

        if hasattr(exc, "messages") and exc.messages:
            return "; ".join(str(message) for message in exc.messages)

        return str(exc)

    @staticmethod
    def _generate_registration_number(
        *,
        organization: Organization,
    ) -> str:
        """
        Generate the next organization-scoped registration number.

        The organization row is locked for the duration of the transaction.
        This serializes registration-number generation for an organization
        without requiring a separate sequence table.

        Format:

            REG-<ORG>-<SEQUENCE>

        Example:

            REG-BLR-000001
        """

        organization_id = getattr(
            organization,
            "pk",
            None,
        )

        if organization_id is None:
            raise ValidationException(
                "A valid organization is required to generate a registration number.",
            )

        locked_organization = Organization.objects.select_for_update().get(
            pk=organization_id,
        )

        organization_token = PatientRegistrationService._organization_token(
            locked_organization,
        )

        prefix = RegistrationNumberPrefix.DEFAULT

        existing_numbers = PatientRegistration.objects.filter(
            organization_id=locked_organization.pk,
            registration_number__startswith=(f"{prefix}-{organization_token}-"),
        ).values_list(
            "registration_number",
            flat=True,
        )

        highest_sequence = 0

        sequence_pattern = re.compile(
            rf"^{re.escape(prefix)}-"
            rf"{re.escape(organization_token)}-"
            rf"(\d+)$",
        )

        for registration_number in existing_numbers:
            match = sequence_pattern.fullmatch(
                registration_number,
            )

            if match is None:
                continue

            highest_sequence = max(
                highest_sequence,
                int(match.group(1)),
            )

        sequence = highest_sequence + 1

        while True:
            registration_number = f"{prefix}-{organization_token}-{sequence:06d}"

            if not PatientRegistration.objects.filter(
                organization_id=locked_organization.pk,
                registration_number=registration_number,
            ).exists():
                return registration_number

            sequence += 1

    @staticmethod
    def _organization_token(
        organization: Any,
    ) -> str:
        """
        Resolve a stable organization token.

        Preference order:

        1. organization.code
        2. organization.slug
        3. organization.pk
        """

        candidate = getattr(
            organization,
            "code",
            None,
        )

        if not candidate:
            candidate = getattr(
                organization,
                "slug",
                None,
            )

        if not candidate:
            candidate = getattr(
                organization,
                "pk",
                None,
            )

        if candidate is None:
            raise ValidationException(
                "Unable to generate a registration number because the "
                "organization has no usable identifier.",
            )

        token = re.sub(
            r"[^A-Za-z0-9]",
            "",
            str(candidate),
        ).upper()

        if not token:
            raise ValidationException(
                "Unable to generate a registration number because the "
                "organization identifier is invalid.",
            )

        return token[:10]


__all__ = ("PatientRegistrationService",)

"""
Domain services for Patient Referrals.
"""

from __future__ import annotations

from django.db import IntegrityError, transaction
from django.utils import timezone

from apps.patient_management.referrals.constants import (
    ReferralStatus,
    is_valid_referral_transition,
)
from apps.patient_management.referrals.exceptions import (
    ReferralTransitionError,
    ReferralValidationError,
)
from apps.patient_management.referrals.models import PatientReferral
from apps.patient_management.referrals.validators import (
    validate_referral_payload,
)


class PatientReferralService:
    """Perform validated referral mutations."""

    MUTABLE_FIELDS = frozenset(
        {
            "referring_provider",
            "referred_to",
            "referred_to_organization",
            "reason",
            "priority",
            "urgency",
            "clinical_notes",
            "requested_date",
            "appointment_date",
        }
    )

    @staticmethod
    def _validate_boundary(
        *,
        patient,
        organization,
    ) -> None:
        """Validate patient, organization, and tenant alignment."""

        if patient.organization_id != organization.id:
            raise ReferralValidationError(
                "Patient does not belong to the selected organization.",
            )

        if patient.tenant_id != organization.tenant_id:
            raise ReferralValidationError(
                "Patient and organization do not share the same tenant.",
            )

    @classmethod
    @transaction.atomic
    def create(
        cls,
        *,
        patient,
        organization,
        referral_number: str,
        referred_to: str,
        reason: str,
        priority: str,
        urgency: str,
        referring_provider: str = "",
        referred_to_organization: str = "",
        clinical_notes: str = "",
        requested_date=None,
        performed_by=None,
    ) -> PatientReferral:
        """Create a tenant-safe referral."""

        cls._validate_boundary(
            patient=patient,
            organization=organization,
        )

        validate_referral_payload(
            referral_number=referral_number,
            referred_to=referred_to,
            reason=reason,
            priority=priority,
            urgency=urgency,
        )

        referral = PatientReferral(
            organization=organization,
            patient=patient,
            referral_number=referral_number.strip(),
            referring_provider=referring_provider.strip(),
            referred_to=referred_to.strip(),
            referred_to_organization=referred_to_organization.strip(),
            reason=reason.strip(),
            priority=priority,
            urgency=urgency,
            status=ReferralStatus.DRAFT,
            clinical_notes=clinical_notes.strip(),
            requested_date=requested_date,
            created_by_id=getattr(performed_by, "id", None),
            updated_by_id=getattr(performed_by, "id", None),
        )
        try:
            with transaction.atomic():
                referral.full_clean()
                referral.save()
        except IntegrityError as exc:
            raise ReferralValidationError(
                "A referral with this referral number already exists "
                "in the organization.",
            ) from exc

        return referral

    @classmethod
    @transaction.atomic
    def update(
        cls,
        *,
        referral: PatientReferral,
        performed_by=None,
        **changes,
    ) -> PatientReferral:
        """Update mutable referral data without changing lifecycle state."""

        protected = {
            "id",
            "organization",
            "organization_id",
            "patient",
            "patient_id",
            "status",
            "created_at",
            "created_by_id",
            "deleted_at",
            "deleted_by_id",
            "is_deleted",
        }

        referral = (
            PatientReferral.objects.select_for_update()
            .select_related("organization", "patient")
            .get(pk=referral.pk)
        )

        for field, value in changes.items():
            if field in protected:
                raise ReferralValidationError(
                    f"Field '{field}' cannot be changed by referral update."
                )
            if field not in cls.MUTABLE_FIELDS:
                raise ReferralValidationError(
                    f"Field '{field}' cannot be changed by referral update."
                )
            if not hasattr(referral, field):
                raise ReferralValidationError(f"Unknown referral field: {field}.")
            if isinstance(value, str):
                value = value.strip()
            setattr(referral, field, value)

        referral.updated_by_id = getattr(
            performed_by,
            "id",
            referral.updated_by_id,
        )
        referral.full_clean()
        referral.save()

        return referral

    @classmethod
    @transaction.atomic
    def transition(
        cls,
        *,
        referral: PatientReferral,
        target_status: str,
        performed_by=None,
    ) -> PatientReferral:
        """Perform a strict lifecycle transition."""

        referral = (
            PatientReferral.objects.select_for_update()
            .select_related("organization", "patient")
            .get(pk=referral.pk)
        )

        if not is_valid_referral_transition(
            referral.status,
            target_status,
        ):
            raise ReferralTransitionError(
                f"Invalid referral transition: {referral.status} -> {target_status}.",
            )

        now = timezone.now()

        referral.status = target_status
        referral.updated_by_id = getattr(
            performed_by,
            "id",
            referral.updated_by_id,
        )

        if target_status == ReferralStatus.ACCEPTED:
            referral.accepted_at = now

        if target_status == ReferralStatus.COMPLETED:
            referral.completed_at = now
            referral.completed_date = timezone.localdate()

        referral.full_clean()
        referral.save()

        return referral

    @staticmethod
    @transaction.atomic
    def delete(
        *,
        referral: PatientReferral,
        performed_by=None,
    ) -> PatientReferral:
        """Soft-delete a referral."""

        referral = PatientReferral.objects.select_for_update().get(pk=referral.pk)
        referral.delete(
            user_id=getattr(performed_by, "id", None),
        )
        return referral

    @staticmethod
    @transaction.atomic
    def restore(
        *,
        referral: PatientReferral,
        performed_by=None,
    ) -> PatientReferral:
        """Restore a deleted referral."""

        referral = (
            PatientReferral.all_objects.select_for_update()
            .select_related("organization", "patient")
            .get(pk=referral.pk)
        )
        referral.restore()
        referral.updated_by_id = getattr(
            performed_by,
            "id",
            referral.updated_by_id,
        )
        referral.save(
            update_fields=(
                "updated_by_id",
                "updated_at",
            ),
        )
        return referral


__all__ = ("PatientReferralService",)

# Organization-scoped duplicate referral contract: referral number already exists in the organization.

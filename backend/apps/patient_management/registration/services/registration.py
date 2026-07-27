"""
Services for the Patient Registration module.
"""

from __future__ import annotations

from django.db import transaction
from django.utils import timezone

from apps.common.exceptions import ValidationException
from apps.patient_management.registration.constants import (
    RegistrationStatus,
)
from apps.patient_management.registration.models import (
    PatientRegistration,
)


class PatientRegistrationService:
    """
    Service for Patient Registration.
    """

    @staticmethod
    @transaction.atomic
    def create_registration(
        **validated_data,
    ) -> PatientRegistration:
        """
        Create a patient registration.
        """

        return PatientRegistration.objects.create(
            **validated_data,
        )

    @staticmethod
    @transaction.atomic
    def update_registration(
        registration: PatientRegistration,
        **validated_data,
    ) -> PatientRegistration:
        """
        Update a registration.
        """

        for field, value in validated_data.items():
            setattr(
                registration,
                field,
                value,
            )

        registration.full_clean()

        registration.save()

        return registration

    @staticmethod
    @transaction.atomic
    def verify_registration(
        registration: PatientRegistration,
        user,
    ) -> PatientRegistration:
        """
        Verify a registration.
        """

        if registration.verified:
            raise ValidationException(
                "Registration is already verified.",
            )

        registration.verified = True
        registration.verified_at = timezone.now()
        registration.verified_by = user
        registration.registration_status = RegistrationStatus.VERIFIED

        registration.save(
            update_fields=[
                "verified",
                "verified_at",
                "verified_by",
                "registration_status",
                "updated_at",
            ],
        )

        return registration

    @staticmethod
    @transaction.atomic
    def check_in_registration(
        registration: PatientRegistration,
    ) -> PatientRegistration:
        """
        Check in a patient registration.
        """

        if not registration.verified:
            raise ValidationException(
                "Registration must be verified before check-in.",
            )

        registration.registration_status = RegistrationStatus.CHECKED_IN

        registration.checked_in_at = timezone.now()

        registration.save(
            update_fields=[
                "registration_status",
                "checked_in_at",
                "updated_at",
            ],
        )

        return registration

    @staticmethod
    @transaction.atomic
    def complete_registration(
        registration: PatientRegistration,
    ) -> PatientRegistration:
        """
        Complete a registration.
        """

        if registration.registration_status != RegistrationStatus.CHECKED_IN:
            raise ValidationException(
                "Registration must be checked in first.",
            )

        registration.registration_status = RegistrationStatus.COMPLETED

        registration.completed_at = timezone.now()

        registration.save(
            update_fields=[
                "registration_status",
                "completed_at",
                "updated_at",
            ],
        )

        return registration

    @staticmethod
    @transaction.atomic
    def cancel_registration(
        registration: PatientRegistration,
        *,
        reason: str,
        notes: str = "",
    ) -> PatientRegistration:
        """
        Cancel a registration.
        """

        if registration.registration_status == RegistrationStatus.COMPLETED:
            raise ValidationException(
                "Completed registrations cannot be cancelled.",
            )

        registration.registration_status = RegistrationStatus.CANCELLED

        registration.cancellation_reason = reason
        registration.cancellation_notes = notes

        registration.save(
            update_fields=[
                "registration_status",
                "cancellation_reason",
                "cancellation_notes",
                "updated_at",
            ],
        )

        return registration

    @staticmethod
    @transaction.atomic
    def delete_registration(
        registration: PatientRegistration,
    ) -> None:
        """
        Delete a registration.
        """

        registration.delete()

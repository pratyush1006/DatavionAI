"""Domain services for Patient Preferences."""

from __future__ import annotations

from django.db import transaction

from apps.patient_management.preferences.constants import PreferenceChannel
from apps.patient_management.preferences.exceptions import (
    PreferenceLifecycleError,
    PreferenceOrganizationError,
    PreferenceValidationError,
)
from apps.patient_management.preferences.models import PatientPreference
from apps.patient_management.preferences.validators import validate_preference_data


class PatientPreferenceService:
    """Perform transactional preference mutations."""

    @staticmethod
    def _ensure_boundary(*, patient, organization):
        """Ensure patient, organization, and tenant boundaries match."""

        if patient.organization_id != organization.id:
            raise PreferenceOrganizationError(
                "Patient does not belong to the requested organization.",
            )

        if patient.organization.tenant_id != organization.tenant_id:
            raise PreferenceOrganizationError(
                "Patient and organization do not belong to the same tenant.",
            )

    @classmethod
    @transaction.atomic
    def create(cls, *, patient, organization, validated_data):
        """Create or return the patient's organization-scoped preferences."""

        cls._ensure_boundary(
            patient=patient,
            organization=organization,
        )
        validate_preference_data(validated_data)

        preference, _ = PatientPreference.objects.get_or_create(
            patient=patient,
            defaults={
                "organization": organization,
                **validated_data,
            },
        )

        if preference.organization_id != organization.id:
            raise PreferenceOrganizationError(
                "Patient preference belongs to another organization.",
            )

        return preference

    @classmethod
    @transaction.atomic
    def update(cls, *, preference, validated_data):
        """Update mutable preference fields."""

        validate_preference_data(validated_data)

        protected = {
            "id",
            "patient",
            "patient_id",
            "organization",
            "organization_id",
            "is_deleted",
            "deleted_at",
            "deleted_by_id",
        }

        for field, value in validated_data.items():
            if field not in protected:
                setattr(preference, field, value)

        preference.save()
        return preference

    @staticmethod
    @transaction.atomic
    def delete(*, preference, user_id):
        """Soft-delete a preference."""

        if preference.is_deleted:
            raise PreferenceLifecycleError(
                "Patient preference is already deleted.",
            )

        preference.delete(user_id=user_id)
        return preference

    @staticmethod
    @transaction.atomic
    def restore(*, preference):
        """Restore a soft-deleted preference."""

        if not preference.is_deleted:
            raise PreferenceLifecycleError(
                "Patient preference is not deleted.",
            )

        preference.restore()
        return preference

    @classmethod
    @transaction.atomic
    def set_communication_preference(
        cls,
        *,
        preference,
        channel,
        validated_data,
    ):
        """Create or update one communication channel preference."""

        from apps.patient_management.preferences.models import (
            PatientCommunicationPreference,
        )

        allowed = {
            "enabled",
            "appointment_reminders",
            "clinical_updates",
            "administrative_updates",
            "marketing_messages",
        }

        data = {key: value for key, value in validated_data.items() if key in allowed}

        allowed_channels = {item.value for item in PreferenceChannel}
        if channel not in allowed_channels:
            raise PreferenceValidationError(
                "Unsupported communication preference channel.",
            )

        communication = (
            PatientCommunicationPreference.all_objects.select_for_update()
            .filter(
                preference=preference,
                channel=channel,
            )
            .first()
        )

        if communication is None:
            communication = PatientCommunicationPreference.objects.create(
                preference=preference,
                channel=channel,
                **data,
            )
            return communication

        if communication.is_deleted:
            communication.restore()

        for field, value in data.items():
            setattr(communication, field, value)

        communication.save()
        return communication


__all__ = ("PatientPreferenceService",)

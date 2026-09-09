"""
Patient Profile services.

Domain-specific write operations for PatientProfile.

The service layer owns profile-specific invariants and persistence.
Workflow orchestration, authorization, tenant resolution, and domain
event publication remain responsibilities of the workflow layer.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.core.exceptions import ValidationError
from django.db import transaction

from apps.patient_management.components import PatientMgmtService
from apps.patient_management.profile.models import PatientProfile


class ProfileService(PatientMgmtService):
    """
    Write-side service for patient profiles.

    Responsibilities
    ----------------
    - Enforce profile-specific domain invariants.
    - Validate patient/organization ownership.
    - Persist PatientProfile instances transactionally.

    Non-responsibilities
    --------------------
    - Authorization.
    - Tenant resolution.
    - Workflow orchestration.
    - Domain-event publication.
    - HTTP concerns.

    Those concerns belong to the policy, workflow, and API layers.
    """

    model = PatientProfile

    @classmethod
    @transaction.atomic
    def create(
        cls,
        *,
        validated_data: Mapping[str, Any],
        performed_by: Any = None,
    ) -> PatientProfile:
        """
        Create a patient profile.

        A patient may have at most one profile, and the profile's
        organization must match the patient's organization.
        """
        data = dict(validated_data)

        patient = data.get("patient")
        organization = data.get("organization")

        if patient is None:
            raise ValidationError(
                {
                    "patient": "A patient is required.",
                }
            )

        if organization is None:
            raise ValidationError(
                {
                    "organization": "An organization is required.",
                }
            )

        if patient.organization_id != organization.pk:
            raise ValidationError(
                {
                    "patient": (
                        "The patient must belong to the selected organization."
                    ),
                }
            )

        if PatientProfile.objects.filter(
            patient_id=patient.pk,
        ).exists():
            raise ValidationError(
                {
                    "patient": ("A profile already exists for this patient."),
                }
            )

        instance = cls.model(
            **data,
        )

        instance.full_clean()
        instance.save()

        return instance

    @classmethod
    @transaction.atomic
    def update(
        cls,
        *,
        instance: PatientProfile,
        validated_data: Mapping[str, Any],
        performed_by: Any = None,
    ) -> PatientProfile:
        """
        Update an existing patient profile.

        Organization and patient ownership are immutable after creation.
        """
        data = dict(validated_data)

        organization = data.get(
            "organization",
            instance.organization,
        )

        patient = data.get(
            "patient",
            instance.patient,
        )

        if organization is None:
            raise ValidationError(
                {
                    "organization": "An organization is required.",
                }
            )

        if patient is None:
            raise ValidationError(
                {
                    "patient": "A patient is required.",
                }
            )

        if organization.pk != instance.organization_id:
            raise ValidationError(
                {
                    "organization": (
                        "A patient profile cannot be moved to another organization."
                    ),
                }
            )

        if patient.pk != instance.patient_id:
            raise ValidationError(
                {
                    "patient": (
                        "A patient profile cannot be reassigned to another patient."
                    ),
                }
            )

        # These relationships are immutable.
        data.pop("organization", None)
        data.pop("patient", None)

        if not data:
            return instance

        for field, value in data.items():
            setattr(
                instance,
                field,
                value,
            )

        instance.full_clean()
        instance.save()

        return instance

    @classmethod
    @transaction.atomic
    def delete(
        cls,
        *,
        instance: PatientProfile,
        performed_by: Any = None,
    ) -> None:
        """
        Permanently delete a patient profile.

        Authorization and lifecycle decisions are made by the workflow
        and policy layers before this method is called.
        """
        instance.delete()


create_profile = ProfileService.create
update_profile = ProfileService.update
delete_profile = ProfileService.delete


__all__ = [
    "ProfileService",
    "create_profile",
    "update_profile",
    "delete_profile",
]

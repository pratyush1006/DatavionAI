"""
Selectors for the Patient Registration module.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, cast
from uuid import UUID

from django.db.models import QuerySet

from apps.common.exceptions import ResourceNotFoundException
from apps.patient_management.registration.models import (
    PatientRegistration,
)

if TYPE_CHECKING:
    from apps.platform.organizations.models import Organization


def get_registration_by_uuid(
    *,
    uuid: UUID | str,
    organization: Organization,
) -> PatientRegistration:
    """
    Retrieve a registration by UUID within an organization.

    Organization scoping is mandatory to prevent cross-organization access.
    """

    try:
        return cast(
            PatientRegistration,
            PatientRegistration.objects.get(
                id=uuid,
                organization=organization,
            ),
        )
    except PatientRegistration.DoesNotExist as exc:
        raise ResourceNotFoundException(
            message="Patient registration not found.",
        ) from exc


def get_registration_by_number(
    *,
    organization: Organization,
    registration_number: str,
) -> PatientRegistration:
    """
    Retrieve a registration by registration number within an organization.
    """

    try:
        return cast(
            PatientRegistration,
            PatientRegistration.objects.get(
                organization=organization,
                registration_number=registration_number,
            ),
        )
    except PatientRegistration.DoesNotExist as exc:
        raise ResourceNotFoundException(
            message="Patient registration not found.",
        ) from exc


def list_organization_registrations(
    *,
    organization: Organization,
) -> QuerySet[PatientRegistration]:
    """
    Return registrations belonging to an organization.
    """

    return PatientRegistration.objects.for_organization(
        organization,
    ).by_registration_datetime()


def list_patient_registrations(
    *,
    organization: Organization,
    patient_id: UUID | str,
) -> QuerySet[PatientRegistration]:
    """
    Return registrations for a patient within an organization.

    The patient ID is scoped through the registration organization boundary,
    preventing registrations belonging to another organization from being
    returned.
    """

    return (
        PatientRegistration.objects.for_organization(
            organization,
        )
        .filter(
            patient_id=patient_id,
        )
        .by_registration_datetime()
    )


def get_today_registrations(
    *,
    organization: Organization,
) -> QuerySet[PatientRegistration]:
    """
    Return today's registrations for an organization.
    """

    return (
        PatientRegistration.objects.for_organization(
            organization,
        )
        .today()
        .by_registration_datetime()
    )


def get_completed_registrations(
    *,
    organization: Organization,
) -> QuerySet[PatientRegistration]:
    """
    Return completed registrations for an organization.
    """

    return (
        PatientRegistration.objects.for_organization(
            organization,
        )
        .completed()
        .by_registration_datetime()
    )


def get_pending_verification_registrations(
    *,
    organization: Organization,
) -> QuerySet[PatientRegistration]:
    """
    Return registrations awaiting verification.
    """

    return (
        PatientRegistration.objects.for_organization(
            organization,
        )
        .pending_verification()
        .by_registration_datetime()
    )


def get_ready_for_checkin_registrations(
    *,
    organization: Organization,
) -> QuerySet[PatientRegistration]:
    """
    Return registrations ready for check-in.
    """

    return (
        PatientRegistration.objects.for_organization(
            organization,
        )
        .ready_for_checkin()
        .by_registration_datetime()
    )


def get_ready_for_completion_registrations(
    *,
    organization: Organization,
) -> QuerySet[PatientRegistration]:
    """
    Return registrations ready for completion.
    """

    return (
        PatientRegistration.objects.for_organization(
            organization,
        )
        .ready_for_completion()
        .by_registration_datetime()
    )


def search_registrations(
    *,
    organization: Organization,
    query: str,
) -> QuerySet[PatientRegistration]:
    """
    Search registrations within an organization.
    """

    return (
        PatientRegistration.objects.for_organization(
            organization,
        )
        .search(
            query,
        )
        .by_registration_datetime()
    )


__all__ = (
    "get_completed_registrations",
    "get_pending_verification_registrations",
    "get_ready_for_checkin_registrations",
    "get_ready_for_completion_registrations",
    "get_registration_by_number",
    "get_registration_by_uuid",
    "get_today_registrations",
    "list_organization_registrations",
    "list_patient_registrations",
    "search_registrations",
)

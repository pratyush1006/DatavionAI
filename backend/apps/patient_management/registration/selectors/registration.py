"""
Selectors for the Patient Registration module.
"""

from __future__ import annotations

from django.db.models import QuerySet

from apps.common.exceptions import ObjectNotFoundException
from apps.patient_management.registration.models import (
    PatientRegistration,
)


def get_registration_by_uuid(
    uuid: str,
) -> PatientRegistration:
    """
    Retrieve a registration by UUID.

    Raises:
        ObjectNotFoundException:
            If the registration does not exist.
    """

    try:
        return PatientRegistration.objects.get(
            uuid=uuid,
        )
    except PatientRegistration.DoesNotExist as exc:
        raise ObjectNotFoundException(
            "Patient registration not found.",
        ) from exc


def get_registration_by_number(
    organization,
    registration_number: str,
) -> PatientRegistration:
    """
    Retrieve a registration by registration number.
    """

    try:
        return PatientRegistration.objects.get(
            organization=organization,
            registration_number=registration_number,
        )
    except PatientRegistration.DoesNotExist as exc:
        raise ObjectNotFoundException(
            "Patient registration not found.",
        ) from exc


def list_registrations() -> QuerySet[PatientRegistration]:
    """
    Return all registrations.
    """

    return PatientRegistration.objects.all()


def list_organization_registrations(
    organization,
) -> QuerySet[PatientRegistration]:
    """
    Return registrations for an organization.
    """

    return PatientRegistration.objects.for_organization(
        organization,
    ).recent()


def list_patient_registrations(
    patient,
) -> QuerySet[PatientRegistration]:
    """
    Return registrations for a patient.
    """

    return PatientRegistration.objects.for_patient(
        patient,
    ).recent()


def get_today_registrations(
    organization,
) -> QuerySet[PatientRegistration]:
    """
    Return today's registrations.
    """

    return PatientRegistration.objects.for_organization(
        organization,
    ).today()


def get_completed_registrations(
    organization,
) -> QuerySet[PatientRegistration]:
    """
    Return completed registrations.
    """

    return PatientRegistration.objects.for_organization(
        organization,
    ).completed()


def get_pending_verification_registrations(
    organization,
) -> QuerySet[PatientRegistration]:
    """
    Return registrations awaiting verification.
    """

    return PatientRegistration.objects.for_organization(
        organization,
    ).pending_verification()


def get_ready_for_checkin_registrations(
    organization,
) -> QuerySet[PatientRegistration]:
    """
    Return registrations ready for check-in.
    """

    return PatientRegistration.objects.for_organization(
        organization,
    ).ready_for_checkin()


def get_ready_for_completion_registrations(
    organization,
) -> QuerySet[PatientRegistration]:
    """
    Return registrations ready for completion.
    """

    return PatientRegistration.objects.for_organization(
        organization,
    ).ready_for_completion()


def search_registrations(
    organization,
    query: str,
) -> QuerySet[PatientRegistration]:
    """
    Search registrations.
    """

    return PatientRegistration.objects.for_organization(
        organization,
    ).search(
        query,
    )

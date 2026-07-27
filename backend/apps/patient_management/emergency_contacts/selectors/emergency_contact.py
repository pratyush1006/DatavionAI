"""
Selectors for the Emergency Contacts module.
"""

from __future__ import annotations

from django.db.models import QuerySet

from ..models import EmergencyContact


def get_emergency_contact_by_uuid(
    uuid,
) -> EmergencyContact:
    return EmergencyContact.objects.get(
        uuid=uuid,
    )


def list_emergency_contacts() -> QuerySet[EmergencyContact]:
    return EmergencyContact.objects.all()


def list_patient_emergency_contacts(
    patient,
) -> QuerySet[EmergencyContact]:
    return EmergencyContact.objects.for_patient(patient)


def list_organization_emergency_contacts(
    organization,
) -> QuerySet[EmergencyContact]:
    return EmergencyContact.objects.for_organization(organization)


def get_primary_emergency_contact(
    patient,
) -> EmergencyContact | None:
    return EmergencyContact.objects.for_patient(patient).primary().first()


def search_emergency_contacts(
    query: str,
):
    return EmergencyContact.objects.search(
        query,
    )

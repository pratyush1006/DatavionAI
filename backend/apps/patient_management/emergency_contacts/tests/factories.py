"""Factories for Patient Emergency compatibility tests."""

from __future__ import annotations

import factory

from apps.patient_management.emergency.constants import (
    EmergencyContactPriority,
    EmergencyContactType,
    EmergencyRecordStatus,
)
from apps.patient_management.emergency.models import EmergencyContact


class EmergencyContactFactory(factory.django.DjangoModelFactory):
    """Create a canonical EmergencyContact with a persisted Patient aggregate."""

    class Meta:
        model = EmergencyContact

    organization = factory.SubFactory(
        "apps.platform.organizations.tests.factories.OrganizationFactory"
    )
    patient = factory.SubFactory(
        "apps.patient_management.patients.tests.factories.PatientFactory",
        organization=factory.SelfAttribute("..organization"),
    )
    name = factory.Sequence(lambda n: f"Emergency Contact {n}")
    relationship = EmergencyContactType.FAMILY
    phone = "9876543210"
    alternate_phone = ""
    email = ""
    priority = EmergencyContactPriority.SECONDARY
    status = EmergencyRecordStatus.ACTIVE
    notes = ""


__all__ = ("EmergencyContactFactory",)

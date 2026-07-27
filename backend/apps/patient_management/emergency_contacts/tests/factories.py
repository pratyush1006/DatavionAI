"""
Factories for Emergency Contact tests.
"""

from __future__ import annotations

import factory

from apps.patient_management.emergency_contacts.constants import (
    EmergencyContactRelationship,
    EmergencyContactStatus,
    PreferredContactMethod,
)
from apps.patient_management.emergency_contacts.models import (
    EmergencyContact,
)


class EmergencyContactFactory(
    factory.django.DjangoModelFactory,
):
    """
    Emergency Contact factory.
    """

    class Meta:
        model = EmergencyContact

    organization = factory.SubFactory(
        "apps.platform.organizations.tests.factories.OrganizationFactory",
    )

    patient = factory.SubFactory(
        "apps.patient_management.profile.tests.factories.PatientFactory",
    )

    first_name = "John"

    last_name = "Doe"

    relationship = EmergencyContactRelationship.FATHER

    mobile_number = "9876543210"

    preferred_contact_method = PreferredContactMethod.MOBILE

    status = EmergencyContactStatus.ACTIVE

    priority_order = 1

    is_primary = True

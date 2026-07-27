"""
Factories for the Contacts module.
"""

from __future__ import annotations

import factory

from apps.patient_management.contacts.constants import (
    ContactPurpose,
    ContactSource,
    ContactStatus,
    ContactType,
)
from apps.patient_management.contacts.models import Contact


class ContactFactory(factory.django.DjangoModelFactory):
    """Factory for Contact."""

    class Meta:
        model = Contact

    organization = factory.SubFactory(
        "apps.organizations.tests.factories.OrganizationFactory",
    )
    patient = factory.SubFactory(
        "apps.patient_management.tests.factories.PatientFactory",
    )

    contact_type = ContactType.MOBILE
    purpose = ContactPurpose.PRIMARY
    value = factory.Sequence(
        lambda n: f"+91990000{n:04d}",
    )
    status = ContactStatus.ACTIVE
    source = ContactSource.PATIENT
    is_primary = True
    is_preferred = True

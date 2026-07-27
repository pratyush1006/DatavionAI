"""
Factories for the Addresses module.
"""

from __future__ import annotations

import factory

from apps.patient_management.addresses.constants import (
    AddressSource,
    AddressStatus,
    AddressType,
    AddressUse,
)
from apps.patient_management.addresses.models import Address


class AddressFactory(factory.django.DjangoModelFactory):
    """Factory for Address."""

    class Meta:
        model = Address

    organization = factory.SubFactory(
        "apps.organizations.tests.factories.OrganizationFactory",
    )

    patient = factory.SubFactory(
        "apps.patient_management.patients.tests.factories.PatientFactory",
    )

    address_type = AddressType.HOME
    address_use = AddressUse.RESIDENTIAL
    line_1 = factory.Sequence(
        lambda n: f"{n} Main Street",
    )
    line_2 = ""
    city = "Bangalore"
    state = "Karnataka"
    country = "India"
    postal_code = "560001"
    status = AddressStatus.ACTIVE
    source = AddressSource.MANUAL
    is_primary = False

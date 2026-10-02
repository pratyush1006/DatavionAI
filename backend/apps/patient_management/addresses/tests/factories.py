"""Address test factories."""

from __future__ import annotations

import factory

from apps.patient_management.addresses.models import Address
from apps.platform.organizations.tests.factories import OrganizationFactory


class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address

    organization = factory.SubFactory(OrganizationFactory)
    tenant = factory.LazyAttribute(lambda obj: obj.organization.tenant)
    patient = None
    address_type = "home"
    address_use = "primary"
    status = "unverified"
    source = "patient"
    address_line_1 = factory.Sequence(lambda n: f"{n + 1} Test Street")
    address_line_2 = ""
    landmark = ""
    district = "Bengaluru Urban"
    postal_code = "560001"
    country = None
    region = None
    city = None
    city_name = "Bengaluru"
    region_name = "Karnataka"
    country_name = "India"
    country_code = "IN"
    latitude = None
    longitude = None
    formatted_address = ""
    geocoding_place_id = ""
    geocoding_raw = factory.LazyFunction(dict)
    geocoded_at = None
    is_primary = False
    is_verified = False
    verification_notes = ""
    verified_at = None
    verified_by = None

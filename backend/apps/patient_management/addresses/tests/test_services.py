"""Patient Address runtime service contracts."""

from __future__ import annotations

from unittest.mock import patch

import pytest
from django.core.exceptions import ValidationError

from apps.patient_management.addresses.exceptions import AddressScopeError
from apps.patient_management.addresses.services import AddressService
from apps.patient_management.addresses.tests.factories import AddressFactory
from apps.platform.geography.models import AdministrativeRegion, City, Country
from apps.platform.organizations.tests.factories import OrganizationFactory

pytestmark = pytest.mark.django_db


def test_reverse_geocode_resolves_canonical_geography():
    organization = OrganizationFactory()
    address = AddressFactory(
        organization=organization,
        tenant=organization.tenant,
        latitude=12.971599,
        longitude=77.594566,
    )

    country = Country.objects.create(
        code="IN",
        name="India",
        iso3="IND",
        phone_code="+91",
    )
    region = AdministrativeRegion.objects.create(
        country=country,
        code="KA",
        name="Karnataka",
        region_type="state",
    )
    city = City.objects.create(
        source="address-runtime-test",
        source_id="BLR-RUNTIME-001",
        country=country,
        region=region,
        name="Bengaluru",
        latitude=12.971599,
        longitude=77.594566,
    )

    payload = {
        "display_name": "Bengaluru, Karnataka, India",
        "formatted_address": "Bengaluru, Karnataka, India",
        "city": "Bengaluru",
        "region": "Karnataka",
        "country": "India",
        "country_code": "in",
        "district": "Bengaluru Urban",
        "postcode": "560001",
        "place_id": "runtime-test-place-001",
    }

    with patch(
        "apps.patient_management.addresses.services.address.reverse_geocode",
        return_value=payload,
    ):
        refreshed = AddressService.reverse_geocode(address)

    refreshed.refresh_from_db()
    assert refreshed.country_id == country.id
    assert refreshed.region_id == region.id
    assert refreshed.city_id == city.id
    assert refreshed.country_code == "IN"
    assert refreshed.city_name == "Bengaluru"
    assert refreshed.region_name == "Karnataka"
    assert refreshed.country_name == "India"
    assert refreshed.source == "geography"
    assert refreshed.is_verified is True
    assert refreshed.geocoded_at is not None
    assert refreshed.geocoding_place_id == "runtime-test-place-001"


def test_primary_address_is_unique_per_patient():
    from apps.patient_management.patients.tests.factories import PatientFactory

    patient = PatientFactory()
    address_one = AddressFactory(
        organization=patient.organization,
        tenant=patient.organization.tenant,
        patient=patient,
        is_primary=False,
    )
    address_two = AddressFactory(
        organization=patient.organization,
        tenant=patient.organization.tenant,
        patient=patient,
        is_primary=False,
    )

    AddressService.set_primary(address_one)
    AddressService.set_primary(address_two)

    address_one.refresh_from_db()
    address_two.refresh_from_db()
    assert address_one.is_primary is False
    assert address_two.is_primary is True


def test_create_rejects_cross_tenant_organization():
    organization = OrganizationFactory()
    other_organization = OrganizationFactory()
    with pytest.raises(AddressScopeError):
        AddressService.create(
            tenant=organization.tenant,
            organization=other_organization,
            address_line_1="Scope Test",
        )


def test_coordinates_are_required_together():
    address = AddressFactory(latitude=12.0, longitude=None)
    with pytest.raises(ValidationError):
        address.full_clean()

"""Patient Address API runtime contracts."""

from __future__ import annotations

import pytest
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.patient_management.addresses.api.views import AddressListCreateAPIView
from apps.patient_management.addresses.tests.factories import AddressFactory
from apps.platform.organizations.tests.factories import OrganizationFactory

pytestmark = pytest.mark.django_db


class _User:
    is_authenticated = True
    is_superuser = True
    pk = "address-runtime-test-user"

    def __init__(self, organization):
        self.organization_id = organization.id
        self.tenant_id = organization.tenant_id


def test_list_endpoint_returns_addresses():
    organization = OrganizationFactory()
    AddressFactory(
        organization=organization,
        tenant=organization.tenant,
    )

    request = APIRequestFactory().get("/api/patient-management/addresses/")
    force_authenticate(request, user=_User(organization))

    original_throttle_classes = AddressListCreateAPIView.throttle_classes
    AddressListCreateAPIView.throttle_classes = ()
    try:
        response = AddressListCreateAPIView.as_view()(request)
    finally:
        AddressListCreateAPIView.throttle_classes = original_throttle_classes

    assert response.status_code == 200
    assert len(response.data) == 1

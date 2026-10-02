"""Address dependency-chain tests."""

from __future__ import annotations

import pytest

from apps.patient_management.addresses.tests.factories import AddressFactory
from apps.patient_management.patients.tests.factories import PatientFactory

pytestmark = pytest.mark.django_db


def test_tenant_matches_organization():
    address = AddressFactory()
    assert address.tenant_id == address.organization.tenant_id


def test_patient_matches_organization():
    patient = PatientFactory()
    address = AddressFactory(
        organization=patient.organization,
        tenant=patient.organization.tenant,
        patient=patient,
    )
    assert address.patient.organization_id == address.organization_id
    assert address.tenant_id == address.organization.tenant_id

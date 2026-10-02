"""
Tests for Contact services.
"""

from __future__ import annotations

from django.test import TestCase

from apps.patient_management.contacts.services import (
    create_contact,
)
from apps.patient_management.contacts.tests.factories import ContactFactory


class ContactServiceTestCase(TestCase):
    """Tests for contact services."""

    def test_create_contact(self) -> None:
        organization = OrganizationFactory()
        patient = PatientFactory(organization=organization)
        contact = ContactFactory.build(organization=organization, patient=patient)

        created = create_contact(
            organization=contact.organization,
            patient=contact.patient,
            contact_type=contact.contact_type,
            purpose=contact.purpose,
            value=contact.value,
            status=contact.status,
            source=contact.source,
            is_primary=contact.is_primary,
            is_preferred=contact.is_preferred,
        )

        self.assertIsNotNone(created.pk)


# DatavionOS canonical test-factory binding.
from apps.patient_management.patients.tests.factories import (
    PatientFactory as __DATAVION_CANONICAL_PATIENT_FACTORY,
)
from apps.platform.organizations.tests.factories import (
    OrganizationFactory as __DATAVION_CANONICAL_ORGANIZATION_FACTORY,
)

PatientFactory = __DATAVION_CANONICAL_PATIENT_FACTORY
OrganizationFactory = __DATAVION_CANONICAL_ORGANIZATION_FACTORY

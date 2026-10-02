"""
Tests for Patient Identifier services.
"""

from __future__ import annotations

from django.test import TestCase

from apps.patient_management.identifiers.services import (
    create_patient_identifier,
)


class PatientIdentifierServiceTestCase(TestCase):
    """Tests for Patient Identifier services."""

    def test_create_patient_identifier(self):
        import uuid

        from django.db import connection

        from apps.patient_management.identifiers.models import PatientIdentifier
        from apps.patient_management.patients.models import Patient
        from apps.patient_management.patients.tests.factories import PatientFactory
        from apps.platform.organizations.models import Organization
        from apps.platform.organizations.tests.factories import OrganizationFactory

        organization = OrganizationFactory()
        patient = PatientFactory(organization=organization)

        self.assertIsInstance(organization, Organization)
        self.assertIsInstance(patient, Patient)
        self.assertEqual(patient.organization_id, organization.pk)
        self.assertTrue(Organization.objects.filter(pk=organization.pk).exists())
        self.assertTrue(Patient.objects.filter(pk=patient.pk).exists())

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM organizations WHERE id = %s", [str(organization.pk)]
            )
            self.assertIsNotNone(
                cursor.fetchone(),
                "Organization fixture must be persisted before identifier creation",
            )
            cursor.execute("SELECT 1 FROM patients WHERE id = %s", [str(patient.pk)])
            self.assertIsNotNone(
                cursor.fetchone(),
                "Patient fixture must be persisted before identifier creation",
            )

        identifier_value = "TEST-MRN-" + uuid.uuid4().hex[:12].upper()
        created = create_patient_identifier(
            organization=organization,
            patient=patient,
            identifier_type="MRN",
            identifier_value=identifier_value,
        )

        self.assertIsInstance(created, PatientIdentifier)
        self.assertEqual(created.organization_id, organization.pk)
        self.assertEqual(created.patient_id, patient.pk)
        self.assertEqual(created.identifier_type, "MRN")
        self.assertEqual(created.identifier_value, identifier_value)
        self.assertTrue(PatientIdentifier.objects.filter(pk=created.pk).exists())
        self.assertTrue(
            Organization.objects.filter(pk=created.organization_id).exists()
        )
        self.assertTrue(Patient.objects.filter(pk=created.patient_id).exists())

        # Delete only the child created by this test before Django's
        # deferred PostgreSQL constraint check at TestCase teardown.
        PatientIdentifier.objects.filter(pk=created.pk).delete()
        self.assertFalse(PatientIdentifier.objects.filter(pk=created.pk).exists())


# DatavionOS canonical Patient Identifier test-factory binding.
__DATAVION_CANONICAL_IDENTIFIER_TEST_FACTORIES = True
from apps.patient_management.patients.tests.factories import (
    PatientFactory as __DATAVION_IDENTIFIER_PATIENT_FACTORY,
)
from apps.platform.organizations.tests.factories import (
    OrganizationFactory as __DATAVION_IDENTIFIER_ORGANIZATION_FACTORY,
)

PatientFactory = __DATAVION_IDENTIFIER_PATIENT_FACTORY
OrganizationFactory = __DATAVION_IDENTIFIER_ORGANIZATION_FACTORY

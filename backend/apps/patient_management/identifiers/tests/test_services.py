"""
Tests for Patient Identifier services.
"""

from __future__ import annotations

from django.test import TestCase

from apps.patient_management.identifiers.services import (
    create_patient_identifier,
)
from apps.patient_management.identifiers.tests.factories import (
    PatientIdentifierFactory,
)


class PatientIdentifierServiceTestCase(TestCase):
    """Tests for Patient Identifier services."""

    def test_create_patient_identifier(self) -> None:
        identifier = PatientIdentifierFactory.build()

        created = create_patient_identifier(
            organization=identifier.organization,
            patient=identifier.patient,
            identifier_type=identifier.identifier_type,
            identifier_value=identifier.identifier_value,
            display_value=identifier.display_value,
            priority=identifier.priority,
            status=identifier.status,
            verification_status=identifier.verification_status,
            source=identifier.source,
            is_primary=identifier.is_primary,
        )

        self.assertIsNotNone(created.pk)

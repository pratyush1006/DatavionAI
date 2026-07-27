"""
Service tests for Patient Relationships.
"""

from __future__ import annotations

from django.test import TestCase

from apps.patient_management.relationships.services import (
    create_relationship,
)
from apps.patient_management.relationships.tests.factories import (
    PatientRelationshipFactory,
)


class PatientRelationshipServiceTestCase(
    TestCase,
):
    """Tests for relationship services."""

    def test_create_relationship(
        self,
    ) -> None:
        relationship = PatientRelationshipFactory.build()

        created = create_relationship(
            organization=relationship.organization,
            patient=relationship.patient,
            related_patient=relationship.related_patient,
            relationship_type=relationship.relationship_type,
            relationship_name=relationship.relationship_name,
            relationship_strength=relationship.relationship_strength,
            status=relationship.status,
            verification_status=relationship.verification_status,
            source=relationship.source,
            is_primary=relationship.is_primary,
            start_date=relationship.start_date,
            end_date=relationship.end_date,
            notes=relationship.notes,
        )

        self.assertIsNotNone(
            created.pk,
        )

"""
Selector tests for Patient Relationships.
"""

from __future__ import annotations

from django.test import TestCase

from apps.patient_management.relationships.selectors import (
    get_relationship_by_id,
)
from apps.patient_management.relationships.tests.factories import (
    PatientRelationshipFactory,
)


class PatientRelationshipSelectorTestCase(
    TestCase,
):
    """Tests for relationship selectors."""

    def test_get_relationship_by_id(
        self,
    ) -> None:
        relationship = PatientRelationshipFactory()

        self.assertEqual(
            get_relationship_by_id(
                relationship.pk,
            ),
            relationship,
        )

"""
Model tests for Patient Relationships.
"""

from __future__ import annotations

from django.test import TestCase

from apps.patient_management.relationships.tests.factories import (
    PatientRelationshipFactory,
)


class PatientRelationshipModelTestCase(TestCase):
    """Tests for PatientRelationship."""

    def test_create_relationship(
        self,
    ) -> None:
        relationship = PatientRelationshipFactory()

        self.assertIsNotNone(
            relationship.pk,
        )

    def test_string_representation(
        self,
    ) -> None:
        relationship = PatientRelationshipFactory()

        self.assertTrue(
            str(relationship),
        )

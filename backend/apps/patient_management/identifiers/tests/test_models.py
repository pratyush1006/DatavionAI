"""
Tests for PatientIdentifier models.
"""

from __future__ import annotations

from django.test import TestCase

from apps.patient_management.identifiers.tests.factories import (
    PatientIdentifierFactory,
)


class PatientIdentifierModelTestCase(TestCase):
    """Tests for PatientIdentifier."""

    def test_create_identifier(self) -> None:
        identifier = PatientIdentifierFactory()

        self.assertIsNotNone(identifier.pk)

    def test_string_representation(self) -> None:
        identifier = PatientIdentifierFactory()

        self.assertTrue(str(identifier))

"""
Tests for Patient Identifier selectors.
"""

from __future__ import annotations

from django.test import TestCase

from apps.patient_management.identifiers.selectors import (
    get_identifier_by_id,
)
from apps.patient_management.identifiers.tests.factories import (
    PatientIdentifierFactory,
)


class PatientIdentifierSelectorTestCase(TestCase):
    """Tests for identifier selectors."""

    def test_get_identifier_by_id(self) -> None:
        identifier = PatientIdentifierFactory()

        result = get_identifier_by_id(
            identifier.pk,
        )

        self.assertEqual(
            result.pk,
            identifier.pk,
        )

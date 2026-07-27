"""
Model tests for Address.
"""

from __future__ import annotations

from django.test import TestCase

from apps.patient_management.addresses.tests.factories import (
    AddressFactory,
)


class AddressModelTestCase(TestCase):
    """Tests for Address model."""

    def test_create_address(self) -> None:
        address = AddressFactory()

        self.assertIsNotNone(
            address.pk,
        )

    def test_string_representation(self) -> None:
        address = AddressFactory()

        self.assertTrue(
            str(address),
        )

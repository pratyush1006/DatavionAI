"""
Selector tests for Address.
"""

from __future__ import annotations

from django.test import TestCase

from apps.patient_management.addresses.selectors import (
    get_address_by_id,
)
from apps.patient_management.addresses.tests.factories import (
    AddressFactory,
)


class AddressSelectorTestCase(TestCase):
    """Tests for Address selectors."""

    def test_get_address_by_id(self) -> None:
        address = AddressFactory()

        self.assertEqual(
            get_address_by_id(
                address.pk,
            ),
            address,
        )

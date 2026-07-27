"""
Service tests for Address.
"""

from __future__ import annotations

from django.test import TestCase

from apps.patient_management.addresses.services import (
    create_address,
)
from apps.patient_management.addresses.tests.factories import (
    AddressFactory,
)


class AddressServiceTestCase(TestCase):
    """Tests for Address services."""

    def test_create_address(self) -> None:
        address = AddressFactory.build()

        created = create_address(
            organization=address.organization,
            patient=address.patient,
            address_type=address.address_type,
            address_use=address.address_use,
            line_1=address.line_1,
            line_2=address.line_2,
            city=address.city,
            state=address.state,
            country=address.country,
            postal_code=address.postal_code,
            status=address.status,
            source=address.source,
            is_primary=address.is_primary,
        )

        self.assertIsNotNone(
            created.pk,
        )

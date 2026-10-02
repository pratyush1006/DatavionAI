from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.pharmacy.models import PharmacyIdempotencyKey
from apps.pharmacy.services.idempotency import execute_idempotent
from apps.pharmacy.tests.factories import create_organization


class PharmacyIdempotencyTests(TestCase):
    def setUp(self):
        self.organization = create_organization("Idempotency Org")

    def test_repeated_key_replays_without_running_callback(self):
        calls = []

        def operation():
            calls.append("executed")
            return {"id": "stable-1"}, 201

        first = execute_idempotent(
            organization=self.organization,
            key="idem-001",
            operation="inventory.receive",
            callback=operation,
        )
        second = execute_idempotent(
            organization=self.organization,
            key="idem-001",
            operation="inventory.receive",
            callback=operation,
        )
        self.assertEqual(first[0], {"id": "stable-1"})
        self.assertEqual(first[1], 201)
        self.assertTrue(second[2])
        self.assertEqual(calls, ["executed"])

    def test_same_key_can_be_used_for_different_operations(self):
        first = execute_idempotent(
            organization=self.organization,
            key="idem-002",
            operation="inventory.receive",
            callback=lambda: ({"op": "receive"}, 201),
        )
        second = execute_idempotent(
            organization=self.organization,
            key="idem-002",
            operation="billing.dispensing_bill",
            callback=lambda: ({"op": "bill"}, 201),
        )
        self.assertEqual(first[0]["op"], "receive")
        self.assertEqual(second[0]["op"], "bill")
        self.assertEqual(
            PharmacyIdempotencyKey.objects.filter(
                organization=self.organization, key="idem-002"
            ).count(),
            2,
        )

    def test_missing_key_is_rejected_by_service(self):
        with self.assertRaisesMessage(ValidationError, "Idempotency key is required"):
            execute_idempotent(
                organization=self.organization,
                key="",
                operation="inventory.receive",
                callback=lambda: ({}, 201),
            )

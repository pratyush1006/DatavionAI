from django.db.models import UniqueConstraint
from django.test import TestCase

from apps.imaging.models import ImagingIdempotencyKey


class ImagingConcurrencyContractTests(TestCase):
    def test_idempotency_has_unique_database_contract(self):
        constraints = [
            c
            for c in ImagingIdempotencyKey._meta.constraints
            if isinstance(c, UniqueConstraint)
        ]
        self.assertTrue(constraints)
        self.assertTrue(
            any(set(c.fields) == {"tenant_id", "key", "operation"} for c in constraints)
        )
        self.assertEqual(
            ImagingIdempotencyKey._meta.db_table, "imaging_idempotency_keys"
        )

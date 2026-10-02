"""Architecture and invariant tests for Accounts Receivable."""

from __future__ import annotations

from decimal import Decimal

from django.test import SimpleTestCase

from apps.patient_management.patients.models import Patient

from ..constants import ARAccountStatus, ARTransactionType
from ..models import ARAccount, ARTransaction


class AccountsReceivableArchitectureTests(SimpleTestCase):
    """Verify non-negotiable Accounts Receivable architecture."""

    def test_uses_canonical_patient(self) -> None:
        """Verify AR models use the canonical Patient model."""

        self.assertEqual(
            ARAccount._meta.get_field("patient").remote_field.model, Patient
        )
        self.assertEqual(
            ARTransaction._meta.get_field("patient").remote_field.model,
            Patient,
        )

    def test_balance_fields_are_decimal(self) -> None:
        """Verify monetary fields use DecimalField."""

        self.assertEqual(
            ARAccount._meta.get_field("balance_amount").get_internal_type(),
            "DecimalField",
        )
        self.assertEqual(
            ARTransaction._meta.get_field("amount").get_internal_type(), "DecimalField"
        )

    def test_positive_transaction_types_exist(self) -> None:
        """Verify the expected financial transaction types exist."""

        self.assertIn(ARTransactionType.PAYMENT, ARTransactionType.values)
        self.assertIn(ARTransactionType.WRITE_OFF, ARTransactionType.values)

    def test_paid_state_exists(self) -> None:
        """Verify paid lifecycle state exists."""

        self.assertIn(ARAccountStatus.PAID, ARAccountStatus.values)
        self.assertGreater(Decimal("1.00"), Decimal("0.00"))


__all__ = ("AccountsReceivableArchitectureTests",)

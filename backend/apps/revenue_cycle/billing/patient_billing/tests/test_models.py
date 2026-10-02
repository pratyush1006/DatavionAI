"""Patient Billing model and domain invariant tests."""

from __future__ import annotations

from django.test import SimpleTestCase

from apps.revenue_cycle.billing.patient_billing.constants import (
    BillingPartyType,
    PatientBillingAccountStatus,
    PatientStatementStatus,
)


class PatientBillingConstantsTests(SimpleTestCase):
    """Verify core Patient Billing constants."""

    def test_party_types_exist(self) -> None:
        """Ensure all financial responsibility parties exist."""

        self.assertEqual(
            BillingPartyType.SELF,
            "SELF",
        )
        self.assertEqual(
            BillingPartyType.GUARANTOR,
            "GUARANTOR",
        )
        self.assertEqual(
            BillingPartyType.INSURANCE,
            "INSURANCE",
        )

    def test_account_lifecycle_is_terminal_at_closed(self) -> None:
        """Ensure the closed state remains represented explicitly."""

        self.assertEqual(
            PatientBillingAccountStatus.CLOSED,
            "CLOSED",
        )

    def test_statement_lifecycle_contains_required_states(self) -> None:
        """Ensure statement lifecycle states are present."""

        self.assertEqual(
            PatientStatementStatus.DRAFT,
            "DRAFT",
        )
        self.assertEqual(
            PatientStatementStatus.ISSUED,
            "ISSUED",
        )
        self.assertEqual(
            PatientStatementStatus.VOID,
            "VOID",
        )


__all__ = ("PatientBillingConstantsTests",)

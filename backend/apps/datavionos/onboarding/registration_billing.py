from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from django.db import transaction

from apps.platform.saas_billing.services.invoice_service import (
    InvoiceService,
)


class RegistrationBillingError(ValueError):
    """Expected registration billing error."""


@dataclass(frozen=True, slots=True)
class RegistrationBillingResult:
    """
    Canonical billing result for organization registration.

    A zero-value trial still creates and settles an invoice.
    A paid registration creates and issues an invoice but does
    not pretend that payment has happened.
    """

    invoice: Any
    amount: Decimal
    currency: str
    status: str
    payment_required: bool
    settled: bool
    checkout_required: bool

    @property
    def invoice_id(self) -> str:
        return str(
            getattr(
                self.invoice,
                "pk",
                "",
            )
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "invoice": {
                "id": self.invoice_id,
                "number": getattr(
                    self.invoice,
                    "invoice_number",
                    "",
                ),
                "status": getattr(
                    self.invoice,
                    "status",
                    "",
                ),
                "amount": str(self.amount),
                "currency": self.currency,
                "paid_amount": str(
                    getattr(
                        self.invoice,
                        "paid_amount",
                        Decimal("0"),
                    )
                ),
            },
            "billing": {
                "status": self.status,
                "payment_required": self.payment_required,
                "settled": self.settled,
                "checkout_required": self.checkout_required,
                "zero_value_trial": self.amount <= Decimal("0"),
            },
        }


class RegistrationBillingService:
    """
    Registration -> SaaS invoice boundary.

    Responsibilities:

    1. Create the canonical subscription invoice.
    2. Issue the invoice.
    3. Automatically settle a ₹0 trial.
    4. Leave paid invoices awaiting payment.
    5. Never manufacture a successful paid transaction.
    """

    ZERO_VALUE_REFERENCE = "REGISTRATION_FREE_TRIAL_ZERO_VALUE"

    @staticmethod
    def _amount(invoice: Any) -> Decimal:
        return Decimal(
            str(
                getattr(
                    invoice,
                    "total_amount",
                    "0",
                )
            )
        )

    @staticmethod
    def _currency(invoice: Any) -> str:
        return str(
            getattr(
                invoice,
                "currency",
                "INR",
            )
            or "INR"
        )

    @classmethod
    @transaction.atomic
    def create_registration_invoice(
        cls,
        *,
        subscription: Any,
    ) -> RegistrationBillingResult:
        if subscription is None:
            raise RegistrationBillingError(
                "Subscription is required before registration billing."
            )

        invoice = InvoiceService.create_subscription_invoice(
            subscription=subscription,
        )

        invoice = InvoiceService.issue_invoice(
            invoice=invoice,
        )

        amount = cls._amount(
            invoice,
        )

        currency = cls._currency(
            invoice,
        )

        if amount <= Decimal("0"):
            invoice = InvoiceService.mark_paid(
                invoice=invoice,
                payment_reference=cls.ZERO_VALUE_REFERENCE,
            )

            return RegistrationBillingResult(
                invoice=invoice,
                amount=amount,
                currency=currency,
                status="SETTLED_ZERO_VALUE",
                payment_required=False,
                settled=True,
                checkout_required=False,
            )

        return RegistrationBillingResult(
            invoice=invoice,
            amount=amount,
            currency=currency,
            status="PAYMENT_REQUIRED",
            payment_required=True,
            settled=False,
            checkout_required=True,
        )


__all__ = [
    "RegistrationBillingError",
    "RegistrationBillingResult",
    "RegistrationBillingService",
]

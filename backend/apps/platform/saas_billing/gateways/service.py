"""
Razorpay SaaS billing orchestration.

This service deliberately stays above the canonical invoice/subscription
models. It does not create duplicate billing state.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Any

from .razorpay import RazorpayGateway


class RazorpaySaaSBillingService:
    """
    External-payment orchestration boundary.

    The caller supplies the canonical invoice and its trusted amount.
    """

    def __init__(self) -> None:
        self.gateway = RazorpayGateway()

    def create_checkout_order(
        self,
        *,
        invoice_id: str,
        amount: Decimal,
        organization_id: str,
        subscription_id: str,
    ) -> dict[str, Any]:
        if amount <= Decimal("0"):
            return {
                "required": False,
                "reason": "zero_value_invoice",
                "order": None,
            }

        order = self.gateway.create_order(
            amount=amount,
            receipt=f"datavion-{invoice_id}",
            notes={
                "invoice_id": str(invoice_id),
                "organization_id": str(organization_id),
                "subscription_id": str(subscription_id),
            },
        )

        return {
            "required": True,
            "reason": "paid_invoice",
            "order": order,
        }

    def verify_checkout(
        self,
        *,
        order_id: str,
        payment_id: str,
        signature: str,
    ) -> None:
        self.gateway.verify_payment_signature(
            order_id=order_id,
            payment_id=payment_id,
            signature=signature,
        )

    def verify_webhook(
        self,
        *,
        body: bytes,
        signature: str,
    ) -> None:
        self.gateway.verify_webhook_signature(
            body=body,
            signature=signature,
        )


__all__ = ("RazorpaySaaSBillingService",)

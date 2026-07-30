"""
Payment reconciliation workflow.

Handles DatavionOS payment gateway
reconciliation and accounting synchronization.

Workflow:

Gateway Response
        |
Validate Transaction
        |
Payment Service
        |
Publish Payment Events
        |
Return Payment
"""

from __future__ import annotations

from apps.platform.saas_billing.events import (
    PaymentFailed,
    PaymentReconciled,
    PaymentSucceeded,
)
from apps.platform.saas_billing.models import (
    Payment,
)
from apps.platform.saas_billing.services import (
    PaymentService,
)
from apps.platform.saas_billing.workflows import (
    BaseWorkflow,
)


class ReconcilePaymentWorkflow(
    BaseWorkflow,
):
    """
    Enterprise payment reconciliation workflow.
    """

    def handle(
        self,
        *,
        payment: Payment,
        gateway_response: dict,
        success: bool = True,
    ) -> Payment:
        """
        Reconcile payment gateway response.

        Used for:

        - Stripe callbacks
        - Razorpay webhooks
        - PayPal notifications
        - Bank reconciliation
        """

        if not payment:
            raise ValueError(
                "Payment is required.",
            )

        if not gateway_response:
            raise ValueError(
                "Gateway response is required.",
            )

        # --------------------------------------------------------------
        # Gateway reconciliation
        # --------------------------------------------------------------

        payment = PaymentService.reconcile_gateway(
            payment=payment,
            response=gateway_response,
        )

        # --------------------------------------------------------------
        # Payment lifecycle update
        # --------------------------------------------------------------

        if success:
            payment = PaymentService.mark_success(
                payment=payment,
                gateway_response=gateway_response,
            )

        else:
            payment = PaymentService.mark_failed(
                payment=payment,
                reason=(
                    gateway_response.get(
                        "message",
                        "",
                    )
                ),
                gateway_response=gateway_response,
            )

        # --------------------------------------------------------------
        # Publish reconciliation event
        # --------------------------------------------------------------

        self.publish_event(
            PaymentReconciled(
                aggregate_id=(payment.id),
                metadata={
                    "gateway_status": (
                        gateway_response.get(
                            "status",
                        )
                    ),
                    "organization_id": (str(payment.organization.id)),
                },
            )
        )

        # --------------------------------------------------------------
        # Publish success/failure event
        # --------------------------------------------------------------

        if success:
            self.publish_event(
                PaymentSucceeded(
                    aggregate_id=(payment.id),
                    metadata={
                        "invoice_id": (str(payment.invoice.id)),
                    },
                )
            )

        else:
            self.publish_event(
                PaymentFailed(
                    aggregate_id=(payment.id),
                    metadata={
                        "invoice_id": (str(payment.invoice.id)),
                    },
                )
            )

        return payment


__all__ = [
    "ReconcilePaymentWorkflow",
]

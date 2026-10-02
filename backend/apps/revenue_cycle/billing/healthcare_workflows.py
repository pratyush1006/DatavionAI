from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .healthcare_services import (
    apply_adjustment,
    approve_refund,
    create_invoice,
    finalize_invoice,
    post_payment,
    process_refund,
    request_refund,
)


@dataclass(frozen=True)
class BillingWorkflowRequest:
    organization: Any
    payload: dict
    actor: Any = None
    idempotency_key: str | None = None


@dataclass(frozen=True)
class BillingWorkflowResult:
    value: Any
    replayed: bool = False


class CreateInvoiceWorkflow:
    name = "rcm.healthcare_billing.create_invoice"

    def execute(self, request):
        return BillingWorkflowResult(
            create_invoice(
                organization=request.organization,
                actor=request.actor,
                **request.payload,
            )
        )


class FinalizeInvoiceWorkflow:
    name = "rcm.healthcare_billing.finalize_invoice"

    def execute(self, request):
        return BillingWorkflowResult(
            finalize_invoice(
                organization=request.organization,
                actor=request.actor,
                **request.payload,
            )
        )


class PostPaymentWorkflow:
    name = "rcm.healthcare_billing.post_payment"

    def execute(self, request):
        return BillingWorkflowResult(
            post_payment(
                organization=request.organization,
                actor=request.actor,
                **request.payload,
            )
        )


class ApplyAdjustmentWorkflow:
    name = "rcm.healthcare_billing.apply_adjustment"

    def execute(self, request):
        return BillingWorkflowResult(
            apply_adjustment(
                organization=request.organization,
                actor=request.actor,
                **request.payload,
            )
        )


class RequestRefundWorkflow:
    name = "rcm.healthcare_billing.request_refund"

    def execute(self, request):
        return BillingWorkflowResult(
            request_refund(
                organization=request.organization,
                actor=request.actor,
                **request.payload,
            )
        )


class ApproveRefundWorkflow:
    name = "rcm.healthcare_billing.approve_refund"

    def execute(self, request):
        return BillingWorkflowResult(
            approve_refund(
                organization=request.organization,
                actor=request.actor,
                **request.payload,
            )
        )


class ProcessRefundWorkflow:
    name = "rcm.healthcare_billing.process_refund"

    def execute(self, request):
        return BillingWorkflowResult(
            process_refund(
                organization=request.organization,
                actor=request.actor,
                **request.payload,
            )
        )


WORKFLOW_REGISTRY = {
    x.name: x
    for x in [
        CreateInvoiceWorkflow,
        FinalizeInvoiceWorkflow,
        PostPaymentWorkflow,
        ApplyAdjustmentWorkflow,
        RequestRefundWorkflow,
        ApproveRefundWorkflow,
        ProcessRefundWorkflow,
    ]
}


def get_workflow(name):
    return WORKFLOW_REGISTRY[name]

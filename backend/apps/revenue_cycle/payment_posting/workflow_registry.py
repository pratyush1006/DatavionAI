"""Register payment posting workflows with the core registry."""

from __future__ import annotations

from apps.core.workflows import workflow_registry

from .workflows import (
    PaymentPostingCreateWorkflow,
    PaymentPostingDeleteWorkflow,
    PaymentPostingPostWorkflow,
    PaymentPostingRestoreWorkflow,
    PaymentPostingReverseWorkflow,
    PaymentPostingUpdateWorkflow,
)


def register_payment_posting_workflows() -> None:
    """Register all payment posting workflows idempotently."""

    workflows = {
        "revenue_cycle.payment_posting.create": PaymentPostingCreateWorkflow,
        "revenue_cycle.payment_posting.update": PaymentPostingUpdateWorkflow,
        "revenue_cycle.payment_posting.post": PaymentPostingPostWorkflow,
        "revenue_cycle.payment_posting.reverse": PaymentPostingReverseWorkflow,
        "revenue_cycle.payment_posting.delete": PaymentPostingDeleteWorkflow,
        "revenue_cycle.payment_posting.restore": PaymentPostingRestoreWorkflow,
    }
    for name, workflow in workflows.items():
        if not workflow_registry.is_registered(name):
            workflow_registry.register(name=name, workflow=workflow)


__all__ = ("register_payment_posting_workflows",)

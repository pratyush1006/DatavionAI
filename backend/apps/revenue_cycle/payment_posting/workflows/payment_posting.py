"""Workflows for payment posting mutations."""

from __future__ import annotations

from apps.core.events import publish_after_commit
from apps.core.workflows import BaseWorkflow, WorkflowResult
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization

from ..events import (
    PaymentPostedEvent,
    PaymentPostingCreatedEvent,
    PaymentPostingDeletedEvent,
    PaymentPostingRestoredEvent,
    PaymentPostingReversedEvent,
    PaymentPostingUpdatedEvent,
)
from ..services import (
    create_payment_posting,
    delete_payment_posting,
    post_payment,
    restore_payment_posting,
    reverse_payment,
    update_payment_posting,
)


def _organization(context):
    organization_id = context.metadata.get("organization_id")
    if organization_id is None:
        raise ValueError("Payment Posting workflow requires organization_id metadata.")
    return Organization.objects.get(
        id=organization_id,
        tenant_id=context.tenant_id,
    )


def _actor(context):
    return User.objects.get(pk=context.actor_id)


class PaymentPostingCreateWorkflow(BaseWorkflow):
    """Create a payment posting and publish its event after commit."""

    def _run(self, context):
        """Execute the creation workflow."""

        posting = create_payment_posting(
            organization=_organization(context),
            patient=context.payload["patient"],
            data=context.payload["data"],
            actor=_actor(context),
        )
        publish_after_commit(
            PaymentPostingCreatedEvent(
                posting_id=posting.id,
                organization_id=posting.organization_id,
                patient_id=posting.patient_id,
            )
        )
        return WorkflowResult.ok(context=context, data=posting)


class PaymentPostingUpdateWorkflow(BaseWorkflow):
    """Update a pending payment posting and publish its event after commit."""

    def _run(self, context):
        """Execute the update workflow."""

        posting = update_payment_posting(
            organization_id=context.metadata["organization_id"],
            tenant_id=context.tenant_id,
            posting_id=context.payload["posting_id"],
            data=context.payload["data"],
        )
        publish_after_commit(
            PaymentPostingUpdatedEvent(
                posting_id=posting.id,
                organization_id=posting.organization_id,
            )
        )
        return WorkflowResult.ok(context=context, data=posting)


class PaymentPostingPostWorkflow(BaseWorkflow):
    """Post a payment and publish its event after commit."""

    def _run(self, context):
        """Execute the posting workflow."""

        posting = post_payment(
            organization_id=context.metadata["organization_id"],
            tenant_id=context.tenant_id,
            posting_id=context.payload["posting_id"],
            actor=_actor(context),
        )
        publish_after_commit(
            PaymentPostedEvent(
                posting_id=posting.id,
                organization_id=posting.organization_id,
                amount=str(posting.amount),
            )
        )
        return WorkflowResult.ok(context=context, data=posting)


class PaymentPostingReverseWorkflow(BaseWorkflow):
    """Reverse a posted payment and publish its event after commit."""

    def _run(self, context):
        """Execute the reversal workflow."""

        posting = reverse_payment(
            organization_id=context.metadata["organization_id"],
            tenant_id=context.tenant_id,
            posting_id=context.payload["posting_id"],
            reason=context.payload["reason"],
        )
        publish_after_commit(
            PaymentPostingReversedEvent(
                posting_id=posting.id,
                organization_id=posting.organization_id,
            )
        )
        return WorkflowResult.ok(context=context, data=posting)


class PaymentPostingDeleteWorkflow(BaseWorkflow):
    """Soft-delete a payment posting and publish its event after commit."""

    def _run(self, context):
        """Execute the deletion workflow."""

        posting = delete_payment_posting(
            organization_id=context.metadata["organization_id"],
            tenant_id=context.tenant_id,
            posting_id=context.payload["posting_id"],
            user_id=context.actor_id,
        )
        publish_after_commit(
            PaymentPostingDeletedEvent(
                posting_id=posting.id,
                organization_id=posting.organization_id,
            )
        )
        return WorkflowResult.ok(context=context, data=posting)


class PaymentPostingRestoreWorkflow(BaseWorkflow):
    """Restore a payment posting and publish its event after commit."""

    def _run(self, context):
        """Execute the restore workflow."""

        posting = restore_payment_posting(
            organization_id=context.metadata["organization_id"],
            tenant_id=context.tenant_id,
            posting_id=context.payload["posting_id"],
        )
        publish_after_commit(
            PaymentPostingRestoredEvent(
                posting_id=posting.id,
                organization_id=posting.organization_id,
            )
        )
        return WorkflowResult.ok(context=context, data=posting)


__all__ = (
    "PaymentPostingCreateWorkflow",
    "PaymentPostingDeleteWorkflow",
    "PaymentPostingPostWorkflow",
    "PaymentPostingRestoreWorkflow",
    "PaymentPostingReverseWorkflow",
    "PaymentPostingUpdateWorkflow",
)

"""Workflow registry integration for claim submission."""

from __future__ import annotations

from apps.core.workflows import workflow_registry
from apps.revenue_cycle.claim_submission.workflows.workflows import (
    CreateClaimSubmissionWorkflow,
    DeleteClaimSubmissionWorkflow,
    RestoreClaimSubmissionWorkflow,
    TransitionClaimSubmissionWorkflow,
    UpdateClaimSubmissionWorkflow,
)


def register_claim_submission_workflows():
    """Register claim submission workflows once."""

    entries = {
        "revenue_cycle.claim_submission.create": CreateClaimSubmissionWorkflow,
        "revenue_cycle.claim_submission.update": UpdateClaimSubmissionWorkflow,
        "revenue_cycle.claim_submission.transition": TransitionClaimSubmissionWorkflow,
        "revenue_cycle.claim_submission.delete": DeleteClaimSubmissionWorkflow,
        "revenue_cycle.claim_submission.restore": RestoreClaimSubmissionWorkflow,
    }
    for name, workflow in entries.items():
        if not workflow_registry.is_registered(name):
            workflow_registry.register(name=name, workflow=workflow)


__all__ = ("register_claim_submission_workflows",)

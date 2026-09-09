"""Workflow orchestration for claim scrubbing."""

from __future__ import annotations

from apps.core.workflows import BaseWorkflow, WorkflowContext, WorkflowResult
from apps.revenue_cycle.claim_scrubbing.services import (
    override_scrub,
    run_scrub,
)
from apps.revenue_cycle.claim_scrubbing.workflows.requests import ScrubLifecycleRequest


class RunClaimScrubWorkflow(BaseWorkflow):
    """Run a deterministic claim scrub through the domain service."""

    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Execute the scrub and return its result."""

        request = context.payload
        scrub = run_scrub(
            organization_id=request.organization_id,
            tenant_id=request.tenant_id,
            scrub_id=request.scrub_id,
        )
        return WorkflowResult.ok(data=scrub)


class OverrideClaimScrubWorkflow(BaseWorkflow):
    """Override a failed scrub through the domain service."""

    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Override the scrub and return its result."""

        request: ScrubLifecycleRequest = context.payload
        scrub = override_scrub(
            organization_id=request.organization_id,
            tenant_id=request.tenant_id,
            scrub_id=request.scrub_id,
            reason=request.reason,
        )
        return WorkflowResult.ok(data=scrub)


__all__ = ("RunClaimScrubWorkflow", "OverrideClaimScrubWorkflow")

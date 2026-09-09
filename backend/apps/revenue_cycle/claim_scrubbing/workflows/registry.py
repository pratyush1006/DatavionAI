"""Workflow registration for claim scrubbing."""

from __future__ import annotations

from apps.core.workflows import workflow_registry
from apps.revenue_cycle.claim_scrubbing.workflows.workflows import (
    OverrideClaimScrubWorkflow,
    RunClaimScrubWorkflow,
)


def register_claim_scrubbing_workflows() -> None:
    """Register claim scrubbing workflows idempotently."""

    entries = (
        ("claim_scrub.run", RunClaimScrubWorkflow),
        ("claim_scrub.override", OverrideClaimScrubWorkflow),
    )
    for name, workflow in entries:
        if not workflow_registry.is_registered(name):
            workflow_registry.register(name=name, workflow=workflow)


__all__ = ("register_claim_scrubbing_workflows",)

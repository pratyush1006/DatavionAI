"""Workflow request contracts for claim scrubbing."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class CreateScrubRequest:
    """Request to create a claim scrub."""

    organization_id: str
    patient_id: str
    claim_reference: str
    idempotency_key: str
    input_snapshot: dict = field(default_factory=dict)


@dataclass(frozen=True)
class ScrubLifecycleRequest:
    """Request to execute or override a scrub."""

    organization_id: str
    tenant_id: str
    scrub_id: str
    reason: str = ""


__all__ = ("CreateScrubRequest", "ScrubLifecycleRequest")

"""Workflow request objects for claim submission."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ClaimSubmissionRequest:
    """Carry claim submission command data."""

    organization_id: str
    tenant_id: str
    user_id: str
    patient_id: str = ""
    submission_id: str = ""
    claim_reference: str = ""
    payer_id: str = ""
    payer_name: str = ""
    submission_method: str = "edi"
    idempotency_key: str = ""
    payload: dict = field(default_factory=dict)
    target_status: str = ""
    response_data: dict = field(default_factory=dict)
    external_submission_id: str = ""
    rejection_code: str = ""
    rejection_reason: str = ""
    changes: dict = field(default_factory=dict)


__all__ = ("ClaimSubmissionRequest",)

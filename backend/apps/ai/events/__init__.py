"""AI domain event payloads."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AIRequestCompleted:
    request_id: str
    tenant_id: str
    organization_id: str
    application_code: str
    provider: str
    model: str


__all__ = ("AIRequestCompleted",)

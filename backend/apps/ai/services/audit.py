"""Append-only AI governance event helpers."""

from __future__ import annotations

import hashlib
from typing import Any

from apps.ai.services.observability import sanitize_metadata


def event_fingerprint(
    *,
    event_type: str,
    tenant_id: Any = None,
    organization_id: Any = None,
    actor_id: Any = None,
    request_id: Any = None,
    artifact_id: Any = None,
    metadata=None,
) -> str:
    payload = {
        "event_type": str(event_type),
        "tenant_id": str(tenant_id or ""),
        "organization_id": str(organization_id or ""),
        "actor_id": str(actor_id or ""),
        "request_id": str(request_id or ""),
        "artifact_id": str(artifact_id or ""),
        "metadata": sanitize_metadata(metadata),
    }
    return hashlib.sha256(repr(sorted(payload.items())).encode("utf-8")).hexdigest()


def build_audit_event(
    event_type: str,
    *,
    tenant_id=None,
    organization_id=None,
    actor_id=None,
    request_id=None,
    artifact_id=None,
    metadata=None,
):
    safe = sanitize_metadata(metadata)
    return {
        "event_type": str(event_type),
        "tenant_id": str(tenant_id) if tenant_id is not None else None,
        "organization_id": (
            str(organization_id) if organization_id is not None else None
        ),
        "actor_id": str(actor_id) if actor_id is not None else None,
        "request_id": str(request_id) if request_id is not None else None,
        "artifact_id": str(artifact_id) if artifact_id is not None else None,
        "metadata": safe,
        "fingerprint": event_fingerprint(
            event_type=event_type,
            tenant_id=tenant_id,
            organization_id=organization_id,
            actor_id=actor_id,
            request_id=request_id,
            artifact_id=artifact_id,
            metadata=safe,
        ),
    }

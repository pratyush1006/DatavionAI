"""Revenue Cycle audit metadata helpers."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any


def build_audit_metadata(
    *,
    actor: Any,
    action: str,
    request_id: str | None = None,
    changes: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build serializable audit metadata."""
    actor_id = getattr(actor, "id", None)

    return {
        "actor_id": str(actor_id) if actor_id is not None else None,
        "action": action.strip(),
        "request_id": request_id,
        "changes": dict(changes or {}),
        "occurred_at": datetime.now(UTC).isoformat(),
    }


__all__ = ("build_audit_metadata",)

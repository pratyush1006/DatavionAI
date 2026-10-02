"""Revenue Cycle permission conventions."""

from __future__ import annotations

PERMISSION_PREFIX = "revenue_cycle"


def permission_code(
    action: str,
    resource: str,
) -> str:
    """Build a normalized Revenue Cycle permission code."""
    return f"{PERMISSION_PREFIX}.{resource.strip().lower()}.{action.strip().lower()}"


__all__ = (
    "PERMISSION_PREFIX",
    "permission_code",
)

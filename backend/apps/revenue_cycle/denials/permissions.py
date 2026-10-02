"""Platform RBAC permissions for Denials."""

from __future__ import annotations

DENIALS_LIST = "revenue_cycle.denials.list"
DENIALS_CREATE = "revenue_cycle.denials.create"
DENIALS_UPDATE = "revenue_cycle.denials.update"
DENIALS_DELETE = "revenue_cycle.denials.delete"
DENIALS_RESTORE = "revenue_cycle.denials.restore"
DENIALS_TRANSITION = "revenue_cycle.denials.transition"
__all__ = (
    "DENIALS_LIST",
    "DENIALS_CREATE",
    "DENIALS_UPDATE",
    "DENIALS_DELETE",
    "DENIALS_RESTORE",
    "DENIALS_TRANSITION",
)

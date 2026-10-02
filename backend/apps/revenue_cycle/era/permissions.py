"""Platform RBAC permission codes for ERA."""

from __future__ import annotations

ERA_READ = "revenue_cycle.era.read"
ERA_WRITE = "revenue_cycle.era.write"
ERA_VALIDATE = "revenue_cycle.era.validate"
ERA_POST = "revenue_cycle.era.post"
ERA_REVERSE = "revenue_cycle.era.reverse"
ERA_DELETE = "revenue_cycle.era.delete"
ERA_RESTORE = "revenue_cycle.era.restore"

__all__ = (
    "ERA_DELETE",
    "ERA_POST",
    "ERA_READ",
    "ERA_RESTORE",
    "ERA_REVERSE",
    "ERA_VALIDATE",
    "ERA_WRITE",
)

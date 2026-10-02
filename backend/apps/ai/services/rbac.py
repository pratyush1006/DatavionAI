"""Central RBAC enforcement for all AI operations."""

from __future__ import annotations

from apps.ai.exceptions import AIAuthorizationError
from apps.platform.rbac.engines import user_has_permission

AI_VIEW = "ai.view"
AI_CREATE = "ai.create"
AI_UPDATE = "ai.update"
AI_VERIFY = "ai.verify"
AI_SIGN = "ai.sign"


def require_ai_permission(*, user, organization, permission: str) -> None:
    """Fail closed unless central Platform RBAC grants the exact AI permission."""
    if not user or not getattr(user, "is_authenticated", False):
        raise AIAuthorizationError("Authentication is required.")
    if not organization or not user_has_permission(
        user=user, permission=permission, organization=organization
    ):
        raise AIAuthorizationError(f"Missing RBAC permission: {permission}")


__all__ = (
    "AI_VIEW",
    "AI_CREATE",
    "AI_UPDATE",
    "AI_VERIFY",
    "AI_SIGN",
    "require_ai_permission",
)

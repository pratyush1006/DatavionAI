"""RBAC-only DRF permission gate for the AI platform."""

from __future__ import annotations

from rest_framework.permissions import BasePermission

from apps.ai.services.rbac import AI_VIEW, require_ai_permission
from apps.datavionos.ai_control.service import can_use_department_ai


def resolve_organization(request):
    return getattr(request, "organization", None) or getattr(
        request.user, "organization", None
    )


class AIAuthenticatedPermission(BasePermission):
    """Authentication plus central Platform RBAC; no AI endpoint bypasses RBAC."""

    message = "Central RBAC permission is required for AI operations."

    def has_permission(self, request, view):
        organization = resolve_organization(request)
        try:
            require_ai_permission(
                user=request.user,
                organization=organization,
                permission=getattr(view, "required_ai_permission", AI_VIEW),
            )
        except Exception:
            return False
        application_code = (
            request.data.get("application_code") if hasattr(request, "data") else None
        )
        if (
            application_code
            and getattr(view, "required_ai_permission", AI_VIEW) != AI_VIEW
        ):
            from apps.ai.models import AIApplication

            application = AIApplication.objects.filter(
                tenant=getattr(organization, "tenant", None),
                organization=organization,
                code=application_code,
            ).first()
            if application is None or not can_use_department_ai(
                user=request.user, organization=organization, application=application
            ):
                return False
        return True


__all__ = ("AIAuthenticatedPermission",)

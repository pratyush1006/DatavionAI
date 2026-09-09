"""
Patient Timeline lifecycle API view.
"""

from __future__ import annotations

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.workflows import WorkflowContext
from apps.patient_management.timeline.permissions import (
    CanActivateTimeline,
    CanArchiveTimeline,
    CanDeactivateTimeline,
)
from apps.patient_management.timeline.workflows import (
    TimelineLifecycleRequest,
    TimelineLifecycleWorkflow,
)


class TimelineLifecycleView(APIView):
    """Expose explicit Timeline lifecycle transitions."""

    def get_permissions(self):
        """Return lifecycle-specific RBAC permission."""

        requested_status = self.request.data.get(
            "status",
        )

        permission_class = {
            "active": CanActivateTimeline,
            "draft": CanDeactivateTimeline,
            "archived": CanArchiveTimeline,
        }.get(
            requested_status,
        )

        if permission_class is None:
            permission_class = CanActivateTimeline

        return [
            IsAuthenticated(),
            permission_class(),
        ]

    def get_tenant(self):
        """Resolve the current tenant from request or organization role."""

        tenant = getattr(
            self.request,
            "tenant",
            None,
        ) or getattr(
            self,
            "current_tenant",
            None,
        )

        if tenant is None:
            role = self.request.user.organization_roles.select_related(
                "organization__tenant"
            ).first()
            tenant = role.organization.tenant if role else None

        if tenant is None:
            raise RuntimeError(
                "Tenant context is required.",
            )

        return tenant

    def post(self, request, pk):
        """Apply the requested lifecycle transition through a workflow."""

        result = TimelineLifecycleWorkflow(
            request=TimelineLifecycleRequest(
                timeline_id=pk,
                status=request.data.get("status"),
            ),
        ).execute(
            context=WorkflowContext(
                actor_id=request.user.id,
                tenant_id=self.get_tenant().id,
            ),
        )

        if not result.success:
            raise RuntimeError(
                result.message,
            )

        return Response(
            {
                "message": result.message,
                "code": result.code,
                "data": {
                    field: getattr(
                        result.data,
                        field,
                    )
                    for field in result.data.__dataclass_fields__
                },
            },
            status=status.HTTP_200_OK,
        )


__all__ = ("TimelineLifecycleView",)

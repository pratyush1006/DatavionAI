"""
Patient Timeline restore API view.
"""

from __future__ import annotations

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.workflows import WorkflowContext
from apps.patient_management.timeline.permissions import CanRestoreTimeline
from apps.patient_management.timeline.workflows import (
    TimelineRestoreRequest,
    TimelineRestoreWorkflow,
)


class TimelineRestoreView(APIView):
    """Expose explicit restoration of deleted Timeline entries."""

    permission_classes = (
        IsAuthenticated,
        CanRestoreTimeline,
    )

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
        """Restore a deleted Timeline entry through its workflow."""

        result = TimelineRestoreWorkflow(
            request=TimelineRestoreRequest(
                timeline_id=pk,
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


__all__ = ("TimelineRestoreView",)

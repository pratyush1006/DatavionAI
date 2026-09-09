"""
Patient Timeline retrieve, update, and delete API view.
"""

from __future__ import annotations

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.core.workflows import WorkflowContext
from apps.patient_management.timeline.api.serializers.detail import (
    TimelineDetailSerializer,
)
from apps.patient_management.timeline.api.serializers.update import (
    TimelineUpdateSerializer,
)
from apps.patient_management.timeline.permissions import (
    CanDeleteTimeline,
    CanUpdateTimeline,
    CanViewTimeline,
)
from apps.patient_management.timeline.selectors import (
    get_timeline,
    list_timeline,
)
from apps.patient_management.timeline.workflows import (
    TimelineDeletionRequest,
    TimelineDeletionWorkflow,
    TimelineUpdateRequest,
    TimelineUpdateWorkflow,
)


class TimelineRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView,
):
    """Provide tenant-scoped Timeline detail operations."""

    def get_permissions(self):
        """Return method-specific authentication and RBAC permissions."""

        if self.request.method in (
            "PUT",
            "PATCH",
        ):
            return [
                IsAuthenticated(),
                CanUpdateTimeline(),
            ]

        if self.request.method == "DELETE":
            return [
                IsAuthenticated(),
                CanDeleteTimeline(),
            ]

        return [
            IsAuthenticated(),
            CanViewTimeline(),
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

    def get_queryset(self):
        """Return Timeline entries inside the current tenant boundary."""

        return list_timeline(
            tenant_id=self.get_tenant().id,
        )

    def get_serializer_class(self):
        """Select the serializer for the current request method."""

        if self.request.method in (
            "PUT",
            "PATCH",
        ):
            return TimelineUpdateSerializer

        return TimelineDetailSerializer

    def update(self, request, *args, **kwargs):
        """Update a Timeline entry through its workflow."""

        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=kwargs.get("partial", False),
        )
        serializer.is_valid(
            raise_exception=True,
        )

        result = TimelineUpdateWorkflow(
            request=TimelineUpdateRequest(
                timeline_id=instance.pk,
                data=serializer.validated_data,
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

        instance = get_timeline(
            tenant_id=self.get_tenant().id,
            timeline_id=instance.pk,
        )

        return Response(
            TimelineDetailSerializer(
                instance,
                context={"request": request},
            ).data,
        )

    def destroy(self, request, *args, **kwargs):
        """Delete a Timeline entry through its workflow."""

        instance = self.get_object()

        result = TimelineDeletionWorkflow(
            request=TimelineDeletionRequest(
                timeline_id=instance.pk,
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
            status=status.HTTP_204_NO_CONTENT,
        )


__all__ = ("TimelineRetrieveUpdateDestroyAPIView",)

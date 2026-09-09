"""
Patient Timeline list and create API view.
"""

from __future__ import annotations

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.core.workflows import WorkflowContext
from apps.patient_management.timeline.api.filters import TimelineFilter
from apps.patient_management.timeline.api.serializers.create import (
    TimelineCreateSerializer,
)
from apps.patient_management.timeline.api.serializers.detail import (
    TimelineDetailSerializer,
)
from apps.patient_management.timeline.api.serializers.list import (
    TimelineListSerializer,
)
from apps.patient_management.timeline.permissions import (
    CanCreateTimeline,
    CanListTimeline,
)
from apps.patient_management.timeline.selectors import list_timeline
from apps.patient_management.timeline.workflows import (
    TimelineCreationRequest,
    TimelineCreationWorkflow,
)


class TimelineListCreateAPIView(generics.ListCreateAPIView):
    """Provide tenant-scoped Timeline collection operations."""

    filterset_class = TimelineFilter

    def get_permissions(self):
        """Return method-specific authentication and RBAC permissions."""

        if self.request.method == "POST":
            return [
                IsAuthenticated(),
                CanCreateTimeline(),
            ]
        return [
            IsAuthenticated(),
            CanListTimeline(),
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
            patient_id=self.request.query_params.get("patient_id"),
            organization_id=self.request.query_params.get("organization_id"),
        )

    def get_serializer_class(self):
        """Select the serializer for the current request method."""

        if self.request.method == "POST":
            return TimelineCreateSerializer
        return TimelineListSerializer

    def create(self, request, *args, **kwargs):
        """Create a Timeline entry through its workflow."""

        serializer = self.get_serializer(
            data=request.data,
        )
        serializer.is_valid(
            raise_exception=True,
        )

        data = dict(
            serializer.validated_data,
        )
        organization_id = data.pop(
            "organization_id",
        )
        patient_id = data.pop(
            "patient_id",
        )

        result = TimelineCreationWorkflow(
            request=TimelineCreationRequest(
                organization_id=organization_id,
                patient_id=patient_id,
                data=data,
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

        instance = self.get_queryset().get(
            pk=result.data.timeline_id,
        )

        return Response(
            TimelineDetailSerializer(
                instance,
                context={"request": request},
            ).data,
            status=status.HTTP_201_CREATED,
        )


__all__ = ("TimelineListCreateAPIView",)

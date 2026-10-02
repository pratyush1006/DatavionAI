"""Retrieve, update and destroy Patient Communication API view."""

from __future__ import annotations

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.api.openapi import extend_schema
from apps.patient_management.communication.api.serializers.detail import (
    CommunicationDetailSerializer,
)
from apps.patient_management.communication.api.serializers.update import (
    CommunicationUpdateSerializer,
)
from apps.patient_management.communication.selectors.communication import (
    get_communication,
)
from apps.patient_management.communication.workflows.deletion import (
    CommunicationDeletionRequest,
    CommunicationDeletionWorkflow,
)
from apps.patient_management.communication.workflows.update import (
    CommunicationUpdateRequest,
    CommunicationUpdateWorkflow,
)


class CommunicationRetrieveUpdateDestroyView(APIView):
    """Handle a single tenant-scoped communication."""

    permission_classes = (IsAuthenticated,)

    def _tenant_id(self, request):
        """Resolve the active tenant."""
        if getattr(request, "tenant", None) is not None:
            return request.tenant.id
        role = request.user.organization_roles.select_related(
            "organization__tenant"
        ).first()
        if role is None:
            raise PermissionError("No organization tenant is available.")
        return role.organization.tenant_id

    @extend_schema(responses=CommunicationDetailSerializer)
    def get(self, request, communication_id):
        """Return one communication."""
        communication = get_communication(
            tenant_id=self._tenant_id(request), communication_id=communication_id
        )
        return Response(CommunicationDetailSerializer(communication).data)

    @extend_schema(
        request=CommunicationUpdateSerializer,
        responses=CommunicationDetailSerializer,
    )
    def put(self, request, communication_id):
        """Update one communication through its workflow."""
        communication = get_communication(
            tenant_id=self._tenant_id(request), communication_id=communication_id
        )
        serializer = CommunicationUpdateSerializer(communication, data=request.data)
        serializer.is_valid(raise_exception=True)
        result = CommunicationUpdateWorkflow(
            request=CommunicationUpdateRequest(
                tenant_id=self._tenant_id(request),
                communication_id=communication.id,
                validated_data=serializer.validated_data,
                actor=request.user,
            )
        ).run()
        return Response(
            CommunicationDetailSerializer(result.data["communication_updated"]).data
        )

    @extend_schema(
        request=CommunicationUpdateSerializer,
        responses=CommunicationDetailSerializer,
    )
    def patch(self, request, communication_id):
        """Partially update one communication."""
        communication = get_communication(
            tenant_id=self._tenant_id(request), communication_id=communication_id
        )
        serializer = CommunicationUpdateSerializer(
            communication, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        result = CommunicationUpdateWorkflow(
            request=CommunicationUpdateRequest(
                tenant_id=self._tenant_id(request),
                communication_id=communication.id,
                validated_data=serializer.validated_data,
                actor=request.user,
            )
        ).run()
        return Response(
            CommunicationDetailSerializer(result.data["communication_updated"]).data
        )

    @extend_schema(responses=CommunicationDetailSerializer)
    def delete(self, request, communication_id):
        """Soft-delete one communication."""
        result = CommunicationDeletionWorkflow(
            request=CommunicationDeletionRequest(
                tenant_id=self._tenant_id(request),
                communication_id=communication_id,
                actor=request.user,
            )
        ).run()
        return Response(
            CommunicationDetailSerializer(result.data["communication_deleted"]).data
        )


__all__ = ("CommunicationRetrieveUpdateDestroyView",)

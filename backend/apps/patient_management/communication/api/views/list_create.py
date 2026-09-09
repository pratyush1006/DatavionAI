"""List and create Patient Communication API view."""

from __future__ import annotations

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.patient_management.communication.api.serializers.create import (
    CommunicationCreateSerializer,
)
from apps.patient_management.communication.api.serializers.list import (
    CommunicationListSerializer,
)
from apps.patient_management.communication.selectors.communication import (
    list_communications,
)
from apps.patient_management.communication.workflows.creation import (
    CommunicationCreationRequest,
    CommunicationCreationWorkflow,
)


class CommunicationListCreateView(APIView):
    """Handle tenant-scoped communication listing and creation."""

    permission_classes = (IsAuthenticated,)

    def _tenant_id(self, request):
        """Resolve the active tenant from the authenticated organization role."""
        if getattr(request, "tenant", None) is not None:
            return request.tenant.id
        role = request.user.organization_roles.select_related(
            "organization__tenant"
        ).first()
        if role is None:
            raise PermissionError("No organization tenant is available.")
        return role.organization.tenant_id

    def get(self, request):
        """List communications for the active tenant."""
        queryset = list_communications(
            tenant_id=self._tenant_id(request),
            patient_id=request.query_params.get("patient_id"),
        )
        return Response(CommunicationListSerializer(queryset, many=True).data)

    def post(self, request):
        """Create a communication through the domain workflow."""
        serializer = CommunicationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        organization = serializer.validated_data["organization"]
        workflow = CommunicationCreationWorkflow(
            request=CommunicationCreationRequest(
                tenant_id=organization.tenant_id,
                organization=organization,
                validated_data=serializer.validated_data,
                actor=request.user,
            )
        )
        result = workflow.run()
        return Response(
            CommunicationListSerializer(result.data["communication_created"]).data,
            status=201,
        )


__all__ = ("CommunicationListCreateView",)

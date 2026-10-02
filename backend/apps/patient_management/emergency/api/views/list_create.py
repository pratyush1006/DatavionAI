"""List and create API views for emergency contacts."""

from __future__ import annotations

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.patient_management.emergency.api.serializers import (
    EmergencyCreateSerializer,
    EmergencyListSerializer,
)
from apps.patient_management.emergency.policies import EmergencyPolicy
from apps.patient_management.emergency.selectors import EmergencySelector
from apps.patient_management.emergency.workflows import (
    EmergencyCreationRequest,
    EmergencyCreationWorkflow,
)


class EmergencyListCreateView(APIView):
    """Expose organization-scoped emergency list and create operations."""

    def get(self, request):
        """Return emergency contacts visible to the current actor."""

        organization = request.user.organization
        if not EmergencyPolicy.can_view(
            actor=request.user,
            organization=organization,
        ):
            return Response(
                {"detail": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN,
            )

        queryset = EmergencySelector.queryset(
            organization=organization,
        )
        return Response(
            EmergencyListSerializer(
                queryset,
                many=True,
            ).data,
        )

    def post(self, request):
        """Create an emergency contact through the workflow layer."""

        organization = request.user.organization
        if not EmergencyPolicy.can_create(
            actor=request.user,
            organization=organization,
        ):
            return Response(
                {"detail": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = EmergencyCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        workflow = EmergencyCreationWorkflow(
            request=EmergencyCreationRequest(
                organization=organization,
                patient_id=serializer.validated_data.pop("patient_id"),
                data=serializer.validated_data,
                actor=request.user,
            ),
        )
        result = workflow.run(
            WorkflowContext(
                actor=request.user,
                request=request,
            ),
        )

        return Response(
            EmergencyListSerializer(result.value).data,
            status=status.HTTP_201_CREATED,
        )


from apps.core.workflows import WorkflowContext

__all__ = ("EmergencyListCreateView",)

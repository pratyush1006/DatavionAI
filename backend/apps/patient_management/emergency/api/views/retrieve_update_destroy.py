"""Retrieve, update, and destroy API views for emergency contacts."""

from __future__ import annotations

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.workflows import WorkflowContext
from apps.patient_management.emergency.api.serializers import (
    EmergencyDetailSerializer,
    EmergencyUpdateSerializer,
)
from apps.patient_management.emergency.policies import EmergencyPolicy
from apps.patient_management.emergency.selectors import EmergencySelector
from apps.patient_management.emergency.workflows import (
    EmergencyDeletionRequest,
    EmergencyDeletionWorkflow,
    EmergencyUpdateRequest,
    EmergencyUpdateWorkflow,
)


class EmergencyRetrieveUpdateDestroyView(APIView):
    """Expose organization-scoped emergency detail operations."""

    def get(self, request, emergency_id):
        """Return one emergency contact."""

        organization = request.user.organization
        if not EmergencyPolicy.can_view(
            actor=request.user,
            organization=organization,
        ):
            return Response(
                {"detail": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN,
            )

        record = EmergencySelector.get(
            organization=organization,
            emergency_id=emergency_id,
        )
        return Response(
            EmergencyDetailSerializer(record).data,
        )

    def patch(self, request, emergency_id):
        """Update an emergency contact through its workflow."""

        organization = request.user.organization
        if not EmergencyPolicy.can_update(
            actor=request.user,
            organization=organization,
        ):
            return Response(
                {"detail": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = EmergencyUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        workflow = EmergencyUpdateWorkflow(
            request=EmergencyUpdateRequest(
                organization=organization,
                emergency_id=emergency_id,
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
            EmergencyDetailSerializer(result.value).data,
        )

    def delete(self, request, emergency_id):
        """Soft-delete an emergency contact through its workflow."""

        organization = request.user.organization
        if not EmergencyPolicy.can_delete(
            actor=request.user,
            organization=organization,
        ):
            return Response(
                {"detail": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN,
            )

        workflow = EmergencyDeletionWorkflow(
            request=EmergencyDeletionRequest(
                organization=organization,
                emergency_id=emergency_id,
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
            EmergencyDetailSerializer(result.value).data,
            status=status.HTTP_200_OK,
        )


__all__ = ("EmergencyRetrieveUpdateDestroyView",)

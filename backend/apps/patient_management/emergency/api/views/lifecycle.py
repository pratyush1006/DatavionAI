"""Lifecycle API views for emergency contacts."""

from __future__ import annotations

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.workflows import WorkflowContext
from apps.patient_management.emergency.api.serializers import (
    EmergencyDetailSerializer,
)
from apps.patient_management.emergency.constants import (
    EmergencyRecordStatus,
)
from apps.patient_management.emergency.policies import EmergencyPolicy
from apps.patient_management.emergency.workflows import (
    EmergencyLifecycleRequest,
    EmergencyLifecycleWorkflow,
)


class EmergencyLifecycleView(APIView):
    """Expose emergency contact activation and deactivation."""

    def post(self, request, emergency_id, action):
        """Apply a lifecycle transition to an emergency contact."""

        organization = request.user.organization
        if not EmergencyPolicy.can_update(
            actor=request.user,
            organization=organization,
        ):
            return Response(
                {"detail": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if action not in (
            EmergencyRecordStatus.ACTIVE,
            EmergencyRecordStatus.INACTIVE,
        ):
            return Response(
                {"detail": "Unsupported lifecycle action."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        workflow = EmergencyLifecycleWorkflow(
            request=EmergencyLifecycleRequest(
                organization=organization,
                emergency_id=emergency_id,
                action=action,
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


__all__ = ("EmergencyLifecycleView",)

"""Patient Communication lifecycle API view."""

from __future__ import annotations

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.patient_management.communication.api.serializers.detail import (
    CommunicationDetailSerializer,
)
from apps.patient_management.communication.workflows.lifecycle import (
    CommunicationLifecycleRequest,
    CommunicationLifecycleWorkflow,
)


class CommunicationLifecycleView(APIView):
    """Apply an authorized communication status transition."""

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

    def post(self, request, communication_id):
        """Transition communication status."""
        status_value = request.data.get("status")
        if not status_value:
            return Response({"detail": "status is required."}, status=400)
        result = CommunicationLifecycleWorkflow(
            request=CommunicationLifecycleRequest(
                tenant_id=self._tenant_id(request),
                communication_id=communication_id,
                status=status_value,
                actor=request.user,
            )
        ).run()
        return Response(
            CommunicationDetailSerializer(
                result.data["communication_status_changed"]
            ).data
        )


__all__ = ("CommunicationLifecycleView",)

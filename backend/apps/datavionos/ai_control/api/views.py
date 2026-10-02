from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.ai.models import AIApplication
from apps.datavionos.ai_control.api.serializers import (
    AICapabilityToggleSerializer,
)
from apps.datavionos.ai_control.service import (
    DepartmentScopedAIControlService,
)
from apps.datavionos.selectors.bootstrap import (
    PlatformBootstrapSelector,
)


def resolve_active_organization(*, user):
    bootstrap = PlatformBootstrapSelector().get(user=user)

    organization = bootstrap.organization

    if organization is None or not organization.is_active:
        raise NotFound("Active organization context was not found.")

    return organization


class AIControlPlaneAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.Serializer

    def get(self, request):
        organization = resolve_active_organization(user=request.user)

        return Response(
            DepartmentScopedAIControlService.resolve(
                user=request.user,
                organization=organization,
            )
        )


class AIControlToggleAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AICapabilityToggleSerializer

    def post(
        self,
        request,
        application_id,
    ):
        serializer = AICapabilityToggleSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        organization = resolve_active_organization(user=request.user)

        application = get_object_or_404(
            AIApplication,
            pk=application_id,
            tenant=organization.tenant,
            organization=organization,
        )

        try:
            DepartmentScopedAIControlService.set_enabled(
                user=request.user,
                organization=organization,
                application=application,
                enabled=serializer.validated_data["enabled"],
            )
        except PermissionError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_403_FORBIDDEN,
            )

        return Response(
            DepartmentScopedAIControlService.resolve(
                user=request.user,
                organization=organization,
            )
        )

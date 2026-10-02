from __future__ import annotations

from uuid import UUID

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.datavionos.control_plane.api.serializers import (
    OrganizationCapabilityToggleSerializer,
    OrganizationControlPlaneSnapshotSerializer,
)
from apps.datavionos.control_plane.service import OrganizationControlPlaneService
from apps.datavionos.selectors.bootstrap import PlatformBootstrapSelector
from apps.platform.organizations.models import (
    OrganizationFeature,
    OrganizationModule,
)
from apps.platform.organizations.policies.organization_policy import OrganizationPolicy
from apps.platform.organizations.services.organization_feature import (
    disable_feature,
    enable_feature,
)
from apps.platform.organizations.services.organization_module import (
    disable_module,
    enable_module,
)


def resolve_active_organization(*, user):
    bootstrap = PlatformBootstrapSelector().get(user=user)
    organization = bootstrap.organization
    if organization is None:
        from rest_framework.exceptions import NotFound

        raise NotFound("Active organization context was not found.")
    if not organization.is_active:
        from rest_framework.exceptions import NotFound

        raise NotFound("Active organization context was not found.")
    return organization


class OrganizationControlPlaneAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        organization = resolve_active_organization(user=request.user)
        policy = OrganizationPolicy()
        if not (
            policy.can_manage_modules(actor=request.user, organization=organization)
            or policy.can_manage_features(actor=request.user, organization=organization)
        ):
            return Response(
                {"detail": "You do not have permission to manage this organization."},
                status=status.HTTP_403_FORBIDDEN,
            )
        snapshot = OrganizationControlPlaneService(policy=policy).resolve(
            user=request.user,
            organization=organization,
        )
        return Response(OrganizationControlPlaneSnapshotSerializer(snapshot).data)


class OrganizationModuleToggleAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def patch(self, request, module_id: UUID):
        organization = resolve_active_organization(user=request.user)
        if not OrganizationPolicy().can_manage_modules(
            actor=request.user,
            organization=organization,
        ):
            return Response(
                {
                    "detail": "You do not have permission to manage organization modules."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = OrganizationCapabilityToggleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        module = get_object_or_404(
            OrganizationModule,
            pk=module_id,
            organization=organization,
        )
        if serializer.validated_data["enabled"]:
            enable_module(instance=module)
        else:
            disable_module(instance=module)
        return Response(
            {
                "id": str(module.pk),
                "module_code": module.module_code,
                "status": module.status,
            }
        )


class OrganizationFeatureToggleAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def patch(self, request, feature_id: UUID):
        organization = resolve_active_organization(user=request.user)
        if not OrganizationPolicy().can_manage_features(
            actor=request.user,
            organization=organization,
        ):
            return Response(
                {
                    "detail": "You do not have permission to manage organization features."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = OrganizationCapabilityToggleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        feature = get_object_or_404(
            OrganizationFeature,
            pk=feature_id,
            organization=organization,
        )
        if serializer.validated_data["enabled"]:
            enable_feature(instance=feature)
        else:
            disable_feature(instance=feature)
        return Response(
            {
                "id": str(feature.pk),
                "feature_code": feature.feature_code,
                "status": feature.status,
            }
        )

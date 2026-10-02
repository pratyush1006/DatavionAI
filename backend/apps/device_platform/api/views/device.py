from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.device_platform.api.workflow import execute_device_workflow
from apps.device_platform.models import Device
from apps.device_platform.permissions import has_device_permission
from apps.device_platform.selectors import DeviceSelector
from apps.device_platform.serializers import DeviceCreateSerializer, DeviceSerializer


def require_context(request):
    tenant = getattr(request, "tenant", None)
    organization = getattr(request, "organization", None)
    if tenant is None or organization is None:
        return None, Response(
            {"detail": "Tenant and organization context are required."}, status=400
        )
    if getattr(organization, "tenant_id", None) != getattr(tenant, "tenant_id", None):
        return None, Response(
            {"detail": "Organization does not belong to the active tenant."}, status=403
        )
    return organization, None


class DeviceListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        organization, error = require_context(request)
        if error:
            return error
        if not has_device_permission(
            request.user, "device_platform.view", organization
        ):
            return Response({"detail": "Permission denied."}, status=403)
        return Response(
            DeviceSerializer(
                DeviceSelector.list_for_organization(organization_id=organization.pk),
                many=True,
            ).data
        )

    def post(self, request):
        organization, error = require_context(request)
        if error:
            return error
        if not has_device_permission(
            request.user, "device_platform.manage", organization
        ):
            return Response({"detail": "Permission denied."}, status=403)
        serializer = DeviceCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            result = execute_device_workflow(
                request=request,
                organization=organization,
                workflow_name="device.register",
                payload={
                    "organization_id": organization.pk,
                    "validated_data": serializer.validated_data,
                },
            )
            if not result.success:
                return Response(
                    {"detail": result.message or "Device registration failed."},
                    status=400,
                )
            device = result.data
        except DjangoValidationError as exc:
            return Response(
                {
                    "detail": (
                        exc.message_dict
                        if hasattr(exc, "message_dict")
                        else exc.messages
                    )
                },
                status=400,
            )
        return Response(DeviceSerializer(device).data, status=status.HTTP_201_CREATED)


class DeviceDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, request, device_id):
        organization, error = require_context(request)
        if error:
            return None, error
        try:
            return (
                DeviceSelector.get(
                    device_id=device_id, organization_id=organization.pk
                ),
                None,
            )
        except Device.DoesNotExist:
            return None, Response({"detail": "Device not found."}, status=404)

    def get(self, request, device_id):
        device, error = self.get_object(request, device_id)
        if error:
            return error
        if not has_device_permission(
            request.user, "device_platform.view", device.organization
        ):
            return Response({"detail": "Permission denied."}, status=403)
        return Response(DeviceSerializer(device).data)

    def patch(self, request, device_id):
        device, error = self.get_object(request, device_id)
        if error:
            return error
        if not has_device_permission(
            request.user, "device_platform.manage", device.organization
        ):
            return Response({"detail": "Permission denied."}, status=403)
        serializer = DeviceCreateSerializer(device, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        result = execute_device_workflow(
            request=request,
            organization=device.organization,
            workflow_name="device.update",
            payload={
                "device_id": device_id,
                "organization_id": device.organization_id,
                "validated_data": serializer.validated_data,
            },
        )
        if not result.success:
            return Response(
                {"detail": result.message or "Device update failed."}, status=409
            )
        device = result.data
        return Response(DeviceSerializer(device).data)

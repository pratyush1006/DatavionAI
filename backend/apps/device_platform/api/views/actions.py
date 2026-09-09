from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.device_platform.api.serializers import DeviceSerializer
from apps.device_platform.api.workflow import execute_device_workflow
from apps.device_platform.constants import TelemetrySource
from apps.device_platform.models import Device
from apps.device_platform.permissions import has_device_permission


def context(request):
    tenant, organization = (
        getattr(request, "tenant", None),
        getattr(request, "organization", None),
    )
    if tenant is None or organization is None:
        return None, Response(
            {"detail": "Tenant and organization context are required."}, status=400
        )
    if getattr(organization, "tenant_id", None) != (
        getattr(tenant, "tenant_id", None) or getattr(tenant, "pk", None)
    ):
        return None, Response(
            {"detail": "Organization does not belong to the active tenant."}, status=403
        )
    return organization, None


class DeviceActionAPIView(APIView):
    permission_classes = [IsAuthenticated]
    action_permission = "device_platform.manage"
    workflow_map = {
        "pair": "device.pair",
        "unpair": "device.unpair",
        "connect": "device.connect",
        "disconnect": "device.disconnect",
        "sync": "device.sync",
        "retire": "device.retire",
    }

    def post(self, request, device_id, action):
        organization, error = context(request)
        if error:
            return error
        if not has_device_permission(
            request.user, self.action_permission, organization
        ):
            return Response({"detail": "Permission denied."}, status=403)
        workflow_name = self.workflow_map.get(action)
        if workflow_name is None:
            return Response({"detail": "Unsupported device action."}, status=400)
        try:
            Device.objects.get(device_id=device_id, organization=organization)
            payload = {"device_id": device_id, "organization_id": organization.pk}
            if action in {"pair", "connect", "disconnect"}:
                payload.update(
                    {
                        "source": request.data.get("source", TelemetrySource.BLE),
                        "external_connection_id": request.data.get(
                            "external_connection_id", ""
                        ),
                    }
                )
            if action == "pair":
                payload["initiated_by_id"] = request.user.pk
                payload["pairing_method"] = request.data.get("pairing_method", "BLE")
                payload["metadata"] = request.data.get("metadata") or {}
            result = execute_device_workflow(
                request=request,
                organization=organization,
                workflow_name=workflow_name,
                payload=payload,
            )
        except Device.DoesNotExist:
            return Response({"detail": "Device not found."}, status=404)
        except (ValueError, KeyError) as exc:
            return Response({"detail": str(exc)}, status=409)
        if not result.success:
            return Response(
                {"detail": result.message or "Device operation failed."}, status=409
            )
        data = result.data
        if action in {"connect", "disconnect"}:
            return Response(
                {
                    "connection_id": str(data.connection_id),
                    "state": data.state,
                    "device_id": str(device_id),
                }
            )
        return Response(DeviceSerializer(data).data)

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.device_platform.api.serializers import PatientDeviceSerializer
from apps.device_platform.api.workflow import execute_device_workflow
from apps.device_platform.permissions import has_device_permission
from apps.device_platform.selectors import DeviceSelector


class PatientDeviceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, patient_id):
        organization = getattr(request, "organization", None)
        tenant = getattr(request, "tenant", None)
        if not organization or not tenant:
            return Response(
                {"detail": "Tenant and organization context are required."}, status=400
            )
        if organization.tenant_id != tenant.tenant_id:
            return Response(
                {"detail": "Organization does not belong to the active tenant."},
                status=403,
            )
        if not has_device_permission(
            request.user, "device_platform.view", organization
        ):
            return Response({"detail": "Permission denied."}, status=403)
        return Response(
            PatientDeviceSerializer(
                DeviceSelector.patient_devices(
                    patient_id=patient_id, organization_id=organization.pk
                ),
                many=True,
            ).data
        )

    def post(self, request, patient_id):
        organization = getattr(request, "organization", None)
        tenant = getattr(request, "tenant", None)
        if not organization or not tenant:
            return Response(
                {"detail": "Tenant and organization context are required."}, status=400
            )
        if organization.tenant_id != tenant.tenant_id:
            return Response(
                {"detail": "Organization does not belong to the active tenant."},
                status=403,
            )
        if not has_device_permission(
            request.user, "device_platform.associate", organization
        ):
            return Response({"detail": "Permission denied."}, status=403)
        device_id = request.data.get("device_id")
        try:
            result = execute_device_workflow(
                request=request,
                organization=organization,
                workflow_name="device.associate_patient",
                payload={
                    "device_id": device_id,
                    "patient_id": patient_id,
                    "organization_id": organization.pk,
                },
            )
            if not result.success:
                raise ValueError(result.message or "Association failed.")
            association = result.data
        except Exception as exc:
            return Response({"detail": str(exc)}, status=409)
        return Response(PatientDeviceSerializer(association).data, status=201)

from django.utils.dateparse import parse_datetime
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.device_platform.api.serializers import TelemetrySerializer
from apps.device_platform.api.workflow import execute_device_workflow
from apps.device_platform.permissions import has_device_permission
from apps.device_platform.telemetry.normalization import normalize_measurement
from apps.device_platform.telemetry.validation import validate_measurement


class TelemetryIngestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        organization = getattr(request, "organization", None)
        tenant = getattr(request, "tenant", None)
        if organization is None or tenant is None:
            return Response(
                {"detail": "Tenant and organization context are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if organization.tenant_id != tenant.tenant_id:
            return Response(
                {"detail": "Organization does not belong to the active tenant."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if not has_device_permission(
            request.user,
            "device_platform.telemetry_ingest",
            organization,
        ):
            return Response(
                {"detail": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN,
            )

        data = request.data
        measurement_type, value, unit = normalize_measurement(
            str(data.get("measurement_type", "")),
            data.get("value"),
            data.get("unit"),
        )
        validate_measurement(
            measurement_type=measurement_type,
            value=value,
            unit=unit,
        )

        measured_at = None
        if data.get("measured_at"):
            measured_at = parse_datetime(str(data["measured_at"]))
            if measured_at is None:
                return Response(
                    {"detail": "Invalid measured_at datetime."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        payload = {
            "organization_id": organization.pk,
            "patient_id": data.get("patient_id"),
            "device_id": data.get("device_id"),
            "measurement_type": measurement_type,
            "value": value,
            "unit": unit,
            "measured_at": measured_at,
            "source": data.get("source", "API"),
            "source_event_id": data.get("source_event_id") or None,
            "payload": data.get("payload") or {},
            "provenance": data.get("provenance") or {},
        }

        if not payload["patient_id"] or not payload["device_id"]:
            return Response(
                {"detail": "patient_id and device_id are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            result = execute_device_workflow(
                request=request,
                organization=organization,
                workflow_name="device.ingest_telemetry",
                payload=payload,
            )
        except Exception as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_409_CONFLICT,
            )

        if not result.success:
            return Response(
                {"detail": result.message or "Telemetry ingestion failed."},
                status=status.HTTP_409_CONFLICT,
            )

        return Response(
            TelemetrySerializer(result.data).data,
            status=status.HTTP_201_CREATED,
        )

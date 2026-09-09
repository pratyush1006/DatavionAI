from apps.device_platform.models import TelemetryRecord


class TelemetrySelector:
    @staticmethod
    def patient_measurements(
        *, patient_id, organization_id, measurement_type=None, limit=100
    ):
        qs = TelemetryRecord.objects.filter(
            patient_id=patient_id, organization_id=organization_id
        ).order_by("-measured_at")
        if measurement_type:
            qs = qs.filter(measurement_type=measurement_type)
        return qs[: min(max(limit, 1), 1000)]

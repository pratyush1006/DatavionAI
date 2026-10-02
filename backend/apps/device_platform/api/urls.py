from django.urls import path

from .views import (
    DeviceActionAPIView,
    DeviceDetailAPIView,
    DeviceListCreateAPIView,
    PatientDeviceAPIView,
    TelemetryIngestAPIView,
)

urlpatterns = [
    path("devices/", DeviceListCreateAPIView.as_view(), name="device-list-create"),
    path(
        "devices/<uuid:device_id>/", DeviceDetailAPIView.as_view(), name="device-detail"
    ),
    path(
        "devices/<uuid:device_id>/<str:action>/",
        DeviceActionAPIView.as_view(),
        name="device-action",
    ),
    path(
        "patients/<uuid:patient_id>/devices/",
        PatientDeviceAPIView.as_view(),
        name="patient-devices",
    ),
    path(
        "telemetry/ingest/", TelemetryIngestAPIView.as_view(), name="telemetry-ingest"
    ),
]

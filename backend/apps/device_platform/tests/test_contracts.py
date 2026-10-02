from django.test import SimpleTestCase


class DevicePlatformContractTests(SimpleTestCase):
    def test_permission_codes_are_stable(self):
        from apps.device_platform.permissions import DEVICE_PERMISSIONS

        self.assertEqual(
            set(DEVICE_PERMISSIONS),
            {
                "device_platform.view",
                "device_platform.manage",
                "device_platform.pair",
                "device_platform.associate",
                "device_platform.telemetry_ingest",
                "device_platform.telemetry_view",
            },
        )

    def test_api_views_require_authentication(self):
        from rest_framework.permissions import IsAuthenticated

        from apps.device_platform.api.views import (
            DeviceActionAPIView,
            DeviceDetailAPIView,
            DeviceListCreateAPIView,
            PatientDeviceAPIView,
            TelemetryIngestAPIView,
        )

        for view_class in (
            DeviceListCreateAPIView,
            DeviceDetailAPIView,
            DeviceActionAPIView,
            PatientDeviceAPIView,
            TelemetryIngestAPIView,
        ):
            self.assertIn(IsAuthenticated, view_class.permission_classes)

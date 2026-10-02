from django.test import SimpleTestCase

from apps.device_platform.models import (
    Device,
    DeviceConnection,
    PatientDevice,
    TelemetryRecord,
)


class DevicePlatformModelContractTests(SimpleTestCase):
    def test_telemetry_source_event_id_is_optional(self):
        self.assertTrue(TelemetryRecord._meta.get_field("source_event_id").null)

    def test_patient_device_has_active_uniqueness(self):
        names = {c.name for c in PatientDevice._meta.constraints}
        self.assertIn("dp_patient_device_active_uniq", names)
        self.assertIn("dp_patient_device_device_active_uniq", names)

    def test_connection_is_unique_per_device_and_source(self):
        self.assertIn(
            "dp_conn_org_dev_source_uniq",
            {c.name for c in DeviceConnection._meta.constraints},
        )

    def test_device_has_tenant_scoped_nonblank_serial_uniqueness(self):
        self.assertIn(
            "dp_dev_org_serial_uniq", {c.name for c in Device._meta.constraints}
        )

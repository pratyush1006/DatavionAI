from django.test import SimpleTestCase

from apps.device_platform.telemetry.normalization import normalize_measurement
from apps.device_platform.telemetry.validation import validate_measurement


class TelemetryContractTests(SimpleTestCase):
    def test_heart_rate_normalizes(self):
        self.assertEqual(
            normalize_measurement("heart_rate", 72, None), ("HEART_RATE", 72, "bpm")
        )

    def test_invalid_measurement_type_rejected(self):
        with self.assertRaises(ValueError):
            validate_measurement(measurement_type="", value=1, unit="bpm")

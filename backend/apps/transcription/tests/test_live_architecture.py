from pathlib import Path

from django.test import SimpleTestCase


class LiveTranscriptionArchitectureTests(SimpleTestCase):
    def test_live_websocket_contract(self):
        s = Path(__file__).parents[1].joinpath("api", "live.py").read_text()
        self.assertIn("AsyncJsonWebsocketConsumer", s)
        self.assertIn("bytes_data", s)
        self.assertIn("transcript.segment", s)

    def test_related_module_boundaries(self):
        r = Path(__file__).parents[1].joinpath("integrations")
        for n in (
            "device_platform.py",
            "clinical_notes.py",
            "telemedicine.py",
            "documents.py",
            "storage.py",
            "appointments.py",
            "encounters.py",
            "contracts.py",
        ):
            self.assertTrue(r.joinpath(n).exists(), n)

    def test_live_recovery_and_concurrency(self):
        s = Path(__file__).parents[1].joinpath("workflows", "live.py").read_text()
        self.assertIn("RECONNECTING", s)
        self.assertIn("select_for_update", s)

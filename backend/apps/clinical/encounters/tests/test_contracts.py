from django.test import SimpleTestCase

from apps.clinical.encounters.constants import EncounterStatus


class EncounterContractTests(SimpleTestCase):
    def test_status_contract(self):
        self.assertEqual(
            set(EncounterStatus.values),
            {"scheduled", "in_progress", "completed", "cancelled"},
        )

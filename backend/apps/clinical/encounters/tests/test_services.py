from django.test import SimpleTestCase

from apps.clinical.encounters.constants import is_valid_encounter_transition


class EncounterServiceContractTests(SimpleTestCase):
    def test_valid_transitions(self):
        self.assertTrue(is_valid_encounter_transition("scheduled", "in_progress"))
        self.assertTrue(is_valid_encounter_transition("in_progress", "completed"))
        self.assertFalse(is_valid_encounter_transition("completed", "in_progress"))

from django.test import SimpleTestCase


class VitalE2EArchitectureTests(SimpleTestCase):
    def test_full_chain_imports(self):
        from apps.clinical.vitals.events import (
            VitalCreatedEvent,
            VitalDeletedEvent,
            VitalUpdatedEvent,
        )
        from apps.clinical.vitals.policies import VitalPolicy
        from apps.clinical.vitals.workflow_registry import VITAL_WORKFLOWS

        self.assertIsNotNone(VitalCreatedEvent)
        self.assertIsNotNone(VitalUpdatedEvent)
        self.assertIsNotNone(VitalDeletedEvent)
        self.assertIsNotNone(VitalPolicy)
        self.assertEqual(len(VITAL_WORKFLOWS), 3)

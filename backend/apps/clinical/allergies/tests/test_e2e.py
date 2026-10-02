from django.test import SimpleTestCase


class AllergyE2EArchitectureTests(SimpleTestCase):
    def test_full_chain_imports(self):
        from apps.clinical.allergies import workflow_registry
        from apps.clinical.allergies.events import AllergyCreatedEvent
        from apps.clinical.allergies.policies import AllergyPolicy
        from apps.clinical.allergies.services import delete_allergy
        from apps.clinical.allergies.workflows import AllergyDeletionWorkflow

        self.assertTrue(workflow_registry.ALLERGY_WORKFLOWS)
        self.assertIsNotNone(AllergyCreatedEvent)
        self.assertIsNotNone(AllergyPolicy)
        self.assertTrue(callable(delete_allergy))
        self.assertIsNotNone(AllergyDeletionWorkflow)

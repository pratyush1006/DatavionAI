from django.test import SimpleTestCase

from apps.clinical.allergies.workflows import (
    AllergyCreationWorkflow,
    AllergyDeletionWorkflow,
    AllergyUpdateWorkflow,
)


class AllergyWorkflowContractTests(SimpleTestCase):
    def test_workflow_surface(self):
        self.assertEqual(AllergyCreationWorkflow.workflow_name, "allergy.create")
        self.assertEqual(AllergyUpdateWorkflow.workflow_name, "allergy.update")
        self.assertEqual(AllergyDeletionWorkflow.workflow_name, "allergy.delete")

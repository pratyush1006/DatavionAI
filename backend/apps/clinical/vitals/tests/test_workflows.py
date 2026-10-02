from django.test import SimpleTestCase

from apps.clinical.vitals.workflows import (
    VitalCreationWorkflow,
    VitalDeletionWorkflow,
    VitalUpdateWorkflow,
)


class VitalWorkflowContractTests(SimpleTestCase):
    def test_workflow_surface(self):
        self.assertEqual(VitalCreationWorkflow.workflow_name, "vital.create")
        self.assertEqual(VitalUpdateWorkflow.workflow_name, "vital.update")
        self.assertEqual(VitalDeletionWorkflow.workflow_name, "vital.delete")

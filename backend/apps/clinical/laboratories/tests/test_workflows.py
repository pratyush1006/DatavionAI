from django.test import SimpleTestCase

from apps.clinical.laboratories.workflow_registry import WORKFLOWS


class LaboratoryWorkflowTests(SimpleTestCase):
    def test_order_workflow(self):
        self.assertIn("collected", WORKFLOWS["order"]["ordered"])

    def test_specimen_rejection(self):
        self.assertIn("rejected", WORKFLOWS["specimen"]["received"])

    def test_result_correction(self):
        self.assertIn("corrected", WORKFLOWS["result"]["final"])

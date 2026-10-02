from django.test import SimpleTestCase

from apps.clinical.laboratories.workflow_registry import (
    ORDER_TRANSITIONS,
    REPORT_TRANSITIONS,
    RESULT_TRANSITIONS,
    SPECIMEN_TRANSITIONS,
    assert_transition,
)


class LaboratoryWorkflowRegistryTests(SimpleTestCase):
    def test_order_graph(self):
        assert_transition(ORDER_TRANSITIONS, "ordered", "scheduled")
        with self.assertRaises(ValueError):
            assert_transition(ORDER_TRANSITIONS, "released", "processing")

    def test_specimen_graph(self):
        assert_transition(SPECIMEN_TRANSITIONS, "received", "processing")

    def test_result_graph(self):
        assert_transition(RESULT_TRANSITIONS, "preliminary", "final")
        assert_transition(RESULT_TRANSITIONS, "final", "corrected")

    def test_report_graph(self):
        assert_transition(REPORT_TRANSITIONS, "draft", "final")

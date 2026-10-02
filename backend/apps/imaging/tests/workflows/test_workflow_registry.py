from django.test import SimpleTestCase

from apps.imaging.workflow_registry import (
    ORDER_TRANSITIONS,
    REPORT_TRANSITIONS,
    STUDY_TRANSITIONS,
    assert_transition,
)


class ImagingWorkflowRegistryTests(SimpleTestCase):
    def test_happy_path_order_graph(self):
        assert_transition(ORDER_TRANSITIONS, "ordered", "ready")
        assert_transition(ORDER_TRANSITIONS, "ready", "scheduled")
        assert_transition(ORDER_TRANSITIONS, "scheduled", "in_progress")
        assert_transition(ORDER_TRANSITIONS, "in_progress", "completed")

    def test_illegal_transition_rejected(self):
        with self.assertRaises(ValueError):
            assert_transition(ORDER_TRANSITIONS, "ordered", "completed")

    def test_study_and_report_graphs(self):
        assert_transition(STUDY_TRANSITIONS, "acquired", "preliminary")
        assert_transition(STUDY_TRANSITIONS, "preliminary", "final")
        assert_transition(REPORT_TRANSITIONS, "draft", "final")

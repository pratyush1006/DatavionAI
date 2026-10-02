from django.test import SimpleTestCase

from apps.clinical.laboratories.models import (
    LaboratoryWorkflowState,
    LaboratoryWorkflowTransition,
)


class LaboratoryWorkflowPersistenceTests(SimpleTestCase):
    def test_workflow_models_are_persistent_contracts(self):
        self.assertEqual(
            LaboratoryWorkflowState._meta.db_table,
            "laboratories_workflow_states",
        )
        self.assertEqual(
            LaboratoryWorkflowTransition._meta.db_table,
            "laboratories_workflow_transitions",
        )
        self.assertEqual(
            LaboratoryWorkflowState._meta.get_field("version").default,
            1,
        )

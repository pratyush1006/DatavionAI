from django.test import SimpleTestCase


class VitalContractTests(SimpleTestCase):
    def test_canonical_dependencies(self):
        from apps.clinical.vitals.models import Vital

        modules = [
            f"{field.remote_field.model.__module__}"
            for field in Vital._meta.fields
            if getattr(field, "remote_field", None)
        ]
        joined = " ".join(modules)
        self.assertIn("apps.patient_management.patients.models", joined)
        self.assertIn("apps.clinical.providers.models", joined)
        self.assertIn("apps.clinical.encounters.models", joined)
        self.assertIn("apps.platform.organizations.models", joined)

    def test_policy_uses_canonical_rbac(self):
        from apps.clinical.vitals.policies import VitalPolicy

        self.assertTrue(hasattr(VitalPolicy, "can_create"))
        self.assertTrue(hasattr(VitalPolicy, "can_update"))
        self.assertTrue(hasattr(VitalPolicy, "can_delete"))

    def test_workflow_registry(self):
        from apps.clinical.vitals.workflow_registry import VITAL_WORKFLOWS

        self.assertEqual(
            set(VITAL_WORKFLOWS), {"vital.create", "vital.update", "vital.delete"}
        )

from django.test import SimpleTestCase

from apps.clinical.vitals.policies import VitalPolicy


class VitalPolicyContractTests(SimpleTestCase):
    def test_policy_surface(self):
        self.assertTrue(callable(VitalPolicy.can_view))
        self.assertTrue(callable(VitalPolicy.can_create))
        self.assertTrue(callable(VitalPolicy.can_update))
        self.assertTrue(callable(VitalPolicy.can_delete))

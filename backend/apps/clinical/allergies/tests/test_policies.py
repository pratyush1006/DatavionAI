from django.test import SimpleTestCase

from apps.clinical.allergies.policies import AllergyPolicy


class AllergyPolicyContractTests(SimpleTestCase):
    def test_policy_surface(self):
        for name in ("can_view", "can_create", "can_update", "can_delete"):
            self.assertTrue(callable(getattr(AllergyPolicy, name)))

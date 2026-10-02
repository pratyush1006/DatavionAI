from django.test import SimpleTestCase

from apps.clinical.laboratories.services import laboratory_readiness


class LaboratoryProductionControlTests(SimpleTestCase):
    databases = {"default"}

    def test_readiness_contract(self):
        result = laboratory_readiness()
        self.assertEqual(result.get("status"), "ready")
        self.assertTrue(result.get("checks", {}).get("database"))
        self.assertTrue(result.get("checks", {}).get("outbox"))

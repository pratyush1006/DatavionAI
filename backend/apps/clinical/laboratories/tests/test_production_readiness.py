from django.test import SimpleTestCase


class LaboratoryProductionReadinessTests(SimpleTestCase):
    def test_readiness_contract_is_callable(self):
        from apps.clinical.laboratories.services.production_readiness import (
            run_production_readiness_checks,
        )

        self.assertTrue(callable(run_production_readiness_checks))

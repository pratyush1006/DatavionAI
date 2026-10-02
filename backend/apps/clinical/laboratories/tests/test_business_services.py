from django.test import SimpleTestCase

from apps.clinical.laboratories.integrations.revenue_cycle.contracts import (
    RevenueCycleIntegration,
)


class LaboratoryBusinessServiceContractTests(SimpleTestCase):
    def test_revenue_cycle_is_external_owner(self):
        self.assertTrue(RevenueCycleIntegration)

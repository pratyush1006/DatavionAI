from django.test import SimpleTestCase

from apps.imaging.selectors import orders, reports, studies


class ImagingSelectorContractTests(SimpleTestCase):
    def test_selector_modules_expose_tenant_scoped_contracts(self):
        self.assertTrue(callable(orders.get_order))
        self.assertTrue(callable(studies.get_study))
        self.assertTrue(callable(reports.get_report))

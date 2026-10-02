from django.test import SimpleTestCase
from django.urls import reverse


class ImagingAPIRouteContractTests(SimpleTestCase):
    def test_health_route_is_wired(self):
        self.assertEqual(reverse("imaging-health"), "/api/imaging/health/")

    def test_contract_route_is_wired(self):
        self.assertEqual(reverse("imaging-contract"), "/api/imaging/contract/")

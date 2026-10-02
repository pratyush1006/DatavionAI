from django.test import TestCase

from apps.pharmacy.models import Pharmacy, Supplier
from apps.pharmacy.tests.factories import create_organization


class PharmacyModelTests(TestCase):
    def test_pharmacy_string(self):
        org = create_organization("Model Test Org")
        pharmacy = Pharmacy.objects.create(
            organization=org, code="P01", name="Central Pharmacy"
        )
        self.assertEqual(str(pharmacy), "P01 | Central Pharmacy")

    def test_supplier_is_organization_scoped(self):
        org = create_organization("Supplier Org")
        supplier = Supplier.objects.create(
            organization=org, code="SUP-1", name="Supplier One"
        )
        self.assertEqual(supplier.organization_id, org.id)

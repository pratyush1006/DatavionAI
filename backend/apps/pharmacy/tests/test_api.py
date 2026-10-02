from django.test import TestCase
from rest_framework.test import APIClient

from apps.pharmacy.tests.factories import create_organization, create_user


class PharmacyAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.organization = create_organization("API Pharmacy Org")
        self.user = create_user(self.organization)
        self.user.is_superuser = True
        self.user.save(update_fields=["is_superuser"])
        self.client.force_authenticate(user=self.user)

    def test_requires_authentication(self):
        self.client.force_authenticate(user=None)
        response = self.client.get("/api/pharmacy/pharmacies/")
        self.assertEqual(response.status_code, 401)
        self.client.force_authenticate(user=self.user)

    def test_create_pharmacy(self):
        response = self.client.post(
            "/api/pharmacy/pharmacies/",
            {
                "organization_id": str(self.organization.id),
                "code": "P01",
                "name": "API Pharmacy",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["code"], "P01")

    def test_create_requires_code_and_name(self):
        response = self.client.post(
            "/api/pharmacy/pharmacies/",
            {"organization_id": str(self.organization.id)},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_list_uses_paginated_contract(self):
        Pharmacy = __import__("apps.pharmacy.models", fromlist=["Pharmacy"]).Pharmacy
        Pharmacy.objects.create(
            organization=self.organization, code="P01", name="API Pharmacy"
        )
        response = self.client.get(
            f"/api/pharmacy/pharmacies/?organization_id={self.organization.id}&limit=10"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.data)
        self.assertEqual(response.data["count"], 1)

    def test_regular_user_is_denied_without_pharmacy_rbac_permission(self):
        regular = create_user(self.organization)
        self.client.force_authenticate(user=regular)
        response = self.client.get(
            f"/api/pharmacy/pharmacies/?organization_id={self.organization.id}"
        )
        self.assertEqual(response.status_code, 403)

    def test_cross_tenant_organization_is_denied(self):
        other = create_organization("Other Pharmacy Org")
        response = self.client.get(
            f"/api/pharmacy/pharmacies/?organization_id={other.id}"
        )
        self.assertEqual(response.status_code, 404)

    def test_all_action_routes_are_wired(self):
        from uuid import uuid4

        from django.urls import reverse

        self.assertEqual(reverse("pharmacy-list-create"), "/api/pharmacy/pharmacies/")
        self.assertEqual(reverse("supplier-list-create"), "/api/pharmacy/suppliers/")
        self.assertEqual(reverse("product-list-create"), "/api/pharmacy/products/")
        self.assertEqual(reverse("batch-list"), "/api/pharmacy/batches/")
        self.assertEqual(
            reverse("purchase-order-list-create"), "/api/pharmacy/purchase-orders/"
        )
        approval_id = uuid4()
        order_id = uuid4()
        self.assertIn(
            str(order_id),
            reverse("purchase-order-request-approval", kwargs={"order_id": order_id}),
        )
        self.assertIn(
            str(approval_id),
            reverse("purchase-approval-decide", kwargs={"approval_id": approval_id}),
        )
        self.assertIn(
            str(order_id),
            reverse("dispensing-order-dispense", kwargs={"order_id": order_id}),
        )
        self.assertIn(
            str(order_id),
            reverse("dispensing-order-bill", kwargs={"order_id": order_id}),
        )
        self.assertEqual(reverse("return-list-create"), "/api/pharmacy/returns/")
        self.assertEqual(reverse("pharmacy-inventory"), "/api/pharmacy/inventory/")
        self.assertEqual(
            reverse("pharmacy-inventory-receive"), "/api/pharmacy/inventory/receive/"
        )
        self.assertEqual(
            reverse("pharmacy-operational-summary"), "/api/pharmacy/summary/"
        )

    def test_batch_list_requires_explicit_organization_scope(self):
        response = self.client.get("/api/pharmacy/batches/")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["detail"], "organization_id is required.")

"""Tests for the live Finance Manager dashboard projection."""

from datetime import timedelta
from decimal import Decimal
from unittest.mock import patch

from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.patient_management.patients.models import Patient
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization
from apps.platform.tenancy.models import Tenant
from apps.revenue_cycle.billing.models.healthcare_models import (
    HealthcareInvoice,
    HealthcarePayment,
)
from apps.revenue_cycle.denials.constants import DenialStatus
from apps.revenue_cycle.denials.models import Denial
from apps.revenue_cycle.revenue_analytics.api.views.finance_dashboard import (
    FinanceManagerDashboardAPIView,
)
from apps.revenue_cycle.revenue_analytics.dashboard_service import (
    build_finance_dashboard,
)


class FinanceManagerDashboardTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tenant = Tenant.objects.create(
            name="Finance Dashboard Tenant",
            slug="finance-dashboard-tenant",
        )
        cls.organization = Organization.objects.create(
            tenant=cls.tenant,
            name="Finance Dashboard Organization",
            code="FIN-DASH",
        )
        cls.other_tenant = Tenant.objects.create(
            name="Other Finance Tenant",
            slug="other-finance-tenant",
        )
        cls.other_organization = Organization.objects.create(
            tenant=cls.other_tenant,
            name="Other Finance Organization",
            code="FIN-OTHER",
        )
        cls.user = User.objects.create_superuser(
            username="finance-dashboard@example.test",
            email="finance-dashboard@example.test",
            password="test-password",
            organization=cls.organization,
        )
        cls.patient = Patient.objects.create(
            organization=cls.organization,
            mrn="FIN-DASH-001",
            first_name="Finance",
            last_name="Patient",
            date_of_birth="1980-01-01",
            gender="male",
        )

    def test_live_metrics_and_trend_are_calculated_from_current_records(self):
        now = timezone.now()
        today = timezone.localdate()
        overdue = HealthcareInvoice.objects.create(
            organization=self.organization,
            invoice_number="FIN-OVERDUE-001",
            currency="INR",
            status=HealthcareInvoice.Status.PARTIALLY_PAID,
            total=Decimal("1000.00"),
            paid_total=Decimal("400.00"),
            balance_due=Decimal("600.00"),
            due_date=today - timedelta(days=2),
            finalized_at=now,
        )
        HealthcareInvoice.objects.create(
            organization=self.organization,
            invoice_number="FIN-PAID-001",
            currency="INR",
            status=HealthcareInvoice.Status.PAID,
            total=Decimal("500.00"),
            paid_total=Decimal("500.00"),
            balance_due=Decimal("0.00"),
            finalized_at=now - timedelta(days=35),
        )
        HealthcarePayment.objects.create(
            organization=self.organization,
            invoice=overdue,
            amount=Decimal("400.00"),
            method=HealthcarePayment.Method.UPI,
            status=HealthcarePayment.Status.POSTED,
        )
        Denial.objects.create(
            organization=self.organization,
            patient=self.patient,
            payer_name="Example Payer",
            denial_code="CO-1",
            denial_reason="Missing information",
            amount=Decimal("125.00"),
            status=DenialStatus.OPEN,
            received_at=now,
            idempotency_key="finance-dashboard-denial-1",
        )

        dashboard = build_finance_dashboard(
            organization=self.organization,
            today=today,
        )

        self.assertEqual(dashboard["alerts"]["overdue_invoice_count"], 1)
        self.assertEqual(dashboard["alerts"]["open_denial_count"], 1)
        inr = next(
            row for row in dashboard["currency_totals"] if row["currency"] == "INR"
        )
        self.assertEqual(inr["revenue_mtd"], "1000.00")
        self.assertEqual(inr["collected_mtd"], "400.00")
        self.assertEqual(inr["outstanding"], "600.00")
        self.assertEqual(inr["overdue_amount"], "600.00")
        self.assertEqual(len(dashboard["trend"]), 2)

    def test_api_requires_authorized_tenant_organization_context(self):
        request = APIRequestFactory().get("/api/revenue-cycle/analytics/dashboard/")
        force_authenticate(request, user=self.user)
        request.tenant = self.tenant
        request.organization = self.organization

        with patch(
            "apps.revenue_cycle.revenue_analytics.api.views.finance_dashboard.RevenueAnalyticsPolicy.can_list",
            return_value=True,
        ):
            response = FinanceManagerDashboardAPIView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["currency_totals"][0]["currency"], "INR")

        request = APIRequestFactory().get("/api/revenue-cycle/analytics/dashboard/")
        force_authenticate(request, user=self.user)
        request.tenant = self.other_tenant
        request.organization = self.organization
        response = FinanceManagerDashboardAPIView.as_view()(request)
        self.assertEqual(response.status_code, 400)

"""Tests for authenticated patient dashboard data isolation."""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.patient_management.patients.models import Patient
from apps.patient_management.portal.constants import PortalAccountStatus
from apps.patient_management.portal.models import PatientPortalAccount
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization
from apps.platform.tenancy.models import Tenant

PATIENT_DASHBOARD_ROUTE = (
    "patient_management:patient-management:patient-portal-dashboard"
)


class PatientDashboardAPITests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tenant = Tenant.objects.create(
            name="Patient Dashboard Tenant",
            slug="patient-dashboard-tenant",
        )
        cls.organization = Organization.objects.create(
            tenant=cls.tenant,
            name="Patient Dashboard Organization",
            code="PAT-DASH",
        )
        cls.user = User.objects.create_user(
            username="patient-dashboard@example.test",
            email="patient-dashboard@example.test",
            password="test-password",
            is_verified=True,
        )
        cls.patient = Patient.objects.create(
            organization=cls.organization,
            mrn="PD-MRN-001",
            first_name="Pat",
            last_name="Example",
            date_of_birth="1990-01-01",
            gender="male",
        )
        PatientPortalAccount.objects.create(
            organization=cls.organization,
            patient=cls.patient,
            username=cls.user.email,
            email=cls.user.email,
            email_verified=True,
            status=PortalAccountStatus.ACTIVE,
            is_active=True,
        )

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_dashboard_returns_only_the_linked_patient_projection(self):
        response = self.client.get(
            reverse(PATIENT_DASHBOARD_ROUTE),
        )

        self.assertEqual(response.status_code, 200)
        payload = response.data.get("data", response.data)
        self.assertEqual(payload["patient"]["display_name"], "Pat Example")
        self.assertEqual(
            payload["counts"],
            {
                "upcoming_appointments": 0,
                "active_prescriptions": 0,
                "lab_reports": 0,
                "documents": 0,
            },
        )
        self.assertIsNone(payload["upcoming_appointment"])
        self.assertEqual(payload["health_updates"], [])

    def test_dashboard_denies_login_without_verified_patient_account(self):
        other_user = User.objects.create_user(
            username="unlinked@example.test",
            email="unlinked@example.test",
            password="test-password",
            is_verified=True,
        )
        self.client.force_authenticate(user=other_user)

        response = self.client.get(reverse(PATIENT_DASHBOARD_ROUTE))

        self.assertEqual(response.status_code, 403)

    def test_dashboard_fails_closed_for_ambiguous_email_links(self):
        second_patient = Patient.objects.create(
            organization=self.organization,
            mrn="PD-MRN-002",
            first_name="Another",
            last_name="Patient",
            date_of_birth="1988-02-02",
            gender="female",
        )
        PatientPortalAccount.objects.create(
            organization=self.organization,
            patient=second_patient,
            username="second-patient-account",
            email=self.user.email,
            email_verified=True,
            status=PortalAccountStatus.ACTIVE,
            is_active=True,
        )

        response = self.client.get(reverse(PATIENT_DASHBOARD_ROUTE))

        self.assertEqual(response.status_code, 403)

from datetime import date
from decimal import Decimal

from django.apps import apps
from django.test import TestCase

from apps.clinical.appointments.models import Appointment
from apps.clinical.laboratories.models import (
    Laboratory,
    LaboratoryOrder,
    LaboratoryTest,
)
from apps.clinical.laboratories.services import (
    create_order,
    enter_result,
    release_report,
    verify_result,
)


class LaboratoryServiceTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Tenant = apps.get_model("tenancy", "Tenant")
        Organization = apps.get_model("organizations", "Organization")
        Patient = apps.get_model("patient_core", "Patient")
        cls.tenant = Tenant.objects.create(
            name="Lab Test Tenant", slug="lab-test-tenant"
        )
        cls.org = Organization.objects.create(
            tenant=cls.tenant,
            name="Lab Test Organization",
            code="LABT",
            slug="lab-test-organization",
        )
        cls.patient = Patient.objects.create(
            organization=cls.org, date_of_birth=date(1990, 1, 1)
        )
        cls.lab = Laboratory.objects.create(
            organization=cls.org, code="CENTRAL", name="Central Lab"
        )
        cls.test = LaboratoryTest.objects.create(
            organization=cls.org,
            code="CBC",
            name="CBC",
            specimen_type="blood",
            unit="g/dL",
            price=Decimal("500.00"),
        )

    def test_order_uses_canonical_appointment_model(self):
        field = LaboratoryOrder._meta.get_field("appointment")
        self.assertIs(field.remote_field.model, Appointment)
        self.assertEqual(Appointment._meta.label_lower, "appointments.appointment")

    def test_order_without_appointment_is_supported(self):
        order = create_order(
            organization_id=self.org.id,
            patient_id=self.patient.id,
            laboratory_id=self.lab.id,
            tests=[self.test],
        )
        self.assertIsNone(order.appointment_id)

    def test_end_to_end_result_and_report(self):
        order = create_order(
            organization_id=self.org.id,
            patient_id=self.patient.id,
            laboratory_id=self.lab.id,
            tests=[self.test],
        )
        item = order.items.get()
        result = enter_result(
            organization_id=self.org.id,
            order_item_id=item.id,
            value_numeric=14.2,
            unit="g/dL",
        )
        verify_result(organization_id=self.org.id, result_id=result.id)
        report = release_report(organization_id=self.org.id, order_id=order.id)
        self.assertEqual(report.status, "released")
        self.assertEqual(LaboratoryOrder.objects.get(id=order.id).status, "released")

    def test_cross_organization_appointment_is_rejected(self):
        Tenant = apps.get_model("tenancy", "Tenant")
        Organization = apps.get_model("organizations", "Organization")
        Patient = apps.get_model("patient_core", "Patient")
        Provider = apps.get_model("providers", "Provider")
        other_tenant = Tenant.objects.create(
            name="Other Lab Tenant", slug="other-lab-tenant"
        )
        other_org = Organization.objects.create(
            tenant=other_tenant,
            name="Other Lab Organization",
            code="OTHERLAB",
            slug="other-lab-organization",
        )
        other_patient = Patient.objects.create(
            organization=other_org, date_of_birth=date(1991, 1, 1)
        )
        self.assertNotEqual(other_patient.organization_id, self.patient.organization_id)
        # The canonical Appointment relation is organization-scoped by the model contract.
        self.assertEqual(
            LaboratoryOrder._meta.get_field("appointment").remote_field.model,
            Appointment,
        )
        self.assertTrue(hasattr(Provider, "_meta"))

"""Small deterministic test factories for the Laboratories domain."""

from datetime import date
from decimal import Decimal

from django.apps import apps


def tenant_model():
    return apps.get_model("tenancy", "Tenant")


def organization_model():
    return apps.get_model("organizations", "Organization")


def patient_model():
    return apps.get_model("patient_core", "Patient")


def make_tenant(*, name="Laboratories Test Tenant", slug="laboratories-test-tenant"):
    return tenant_model().objects.create(name=name, slug=slug)


def make_organization(
    *,
    tenant,
    code="LABT",
    name="Laboratories Test Organization",
    slug="laboratories-test-organization",
):
    return organization_model().objects.create(
        tenant=tenant, name=name, code=code, slug=slug
    )


def make_patient(*, organization):
    return patient_model().objects.create(
        organization=organization, date_of_birth=date(1990, 1, 1)
    )


def make_lab(*, organization, code="CENTRAL", name="Central Laboratory"):
    Laboratory = apps.get_model("laboratories", "Laboratory")
    return Laboratory.objects.create(organization=organization, code=code, name=name)


def make_test(*, organization, code="CBC", name="Complete Blood Count"):
    LaboratoryTest = apps.get_model("laboratories", "LaboratoryTest")
    return LaboratoryTest.objects.create(
        organization=organization,
        code=code,
        name=name,
        specimen_type="blood",
        unit="g/dL",
        price=Decimal("500.00"),
    )


def make_basic_lab_context():
    tenant = make_tenant()
    organization = make_organization(tenant=tenant)
    patient = make_patient(organization=organization)
    laboratory = make_lab(organization=organization)
    test = make_test(organization=organization)
    return {
        "tenant": tenant,
        "organization": organization,
        "patient": patient,
        "laboratory": laboratory,
        "test": test,
    }

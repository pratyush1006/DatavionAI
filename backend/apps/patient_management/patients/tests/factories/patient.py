"""
Patient test factories.

Canonical test factory infrastructure for the Patient Management
Patients bounded context.
"""

from __future__ import annotations

from datetime import date

import factory

from apps.patient_management.patients.models import Patient
from apps.platform.organizations.tests.factories import OrganizationFactory


class PatientFactory(factory.django.DjangoModelFactory):
    """
    Factory for the canonical Patient model.

    Patients are tenant-owned through their Organization, so every
    generated patient receives a real canonical Organization unless
    the caller explicitly supplies one.
    """

    class Meta:
        model = Patient

    organization = factory.SubFactory(
        OrganizationFactory,
    )

    mrn = factory.Sequence(
        lambda n: f"MRN{n:06d}",
    )

    first_name = factory.Faker(
        "first_name",
    )

    middle_name = ""

    last_name = factory.Faker(
        "last_name",
    )

    preferred_name = ""

    date_of_birth = factory.LazyFunction(
        lambda: date(1995, 5, 20),
    )

    gender = "male"

    marital_status = ""

    blood_group = ""

    phone = ""

    email = ""

    address = ""

    city = ""

    state = ""

    country = "India"

    postal_code = ""

    status = "active"


def create_patient(**kwargs) -> Patient:
    """
    Create and persist a Patient for tests.
    """

    return PatientFactory(**kwargs)


__all__ = (
    "PatientFactory",
    "create_patient",
)

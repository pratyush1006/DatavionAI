"""
Factories for Patient tests.
"""

from __future__ import annotations

from datetime import date

import factory

from apps.clinical.patients.constants import PatientGender
from apps.clinical.patients.models import Patient
from apps.platform.organizations.tests.factories import OrganizationFactory


class PatientFactory(factory.django.DjangoModelFactory):
    """
    Factory for Patient model.
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

    gender = PatientGender.MALE


__all__ = [
    "PatientFactory",
]

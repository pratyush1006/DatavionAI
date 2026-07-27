"""
Factories for the Family Members module.
"""

from __future__ import annotations

import factory

from apps.patient_management.family_members.constants import (
    FamilyMemberGender,
    FamilyMemberRelationship,
    FamilyMemberStatus,
)
from apps.patient_management.family_members.models import (
    FamilyMember,
)
from apps.patient_management.patients.tests.factories import (
    PatientFactory,
)
from apps.platform.organizations.tests.factories import (
    OrganizationFactory,
)

__all__ = [
    "FamilyMemberFactory",
]


class FamilyMemberFactory(
    factory.django.DjangoModelFactory,
):
    """
    Factory for FamilyMember.
    """

    class Meta:
        model = FamilyMember

    organization = factory.SubFactory(
        OrganizationFactory,
    )

    patient = factory.SubFactory(
        PatientFactory,
        organization=factory.SelfAttribute(
            "..organization",
        ),
    )

    family_member_number = factory.Sequence(
        lambda n: f"FM-{n:06d}",
    )

    first_name = factory.Faker(
        "first_name",
    )

    middle_name = ""

    last_name = factory.Faker(
        "last_name",
    )

    relationship = FamilyMemberRelationship.FATHER

    gender = FamilyMemberGender.MALE

    mobile_number = factory.Sequence(
        lambda n: f"+91999999{n:04d}",
    )

    email = factory.Sequence(
        lambda n: f"family{n}@example.com",
    )

    is_living = True

    is_next_of_kin = False

    is_emergency_contact = False

    status = FamilyMemberStatus.ACTIVE

"""
Manager tests for Family Members.
"""

from __future__ import annotations

import pytest

from apps.patient_management.family_members.tests.factories import (
    FamilyMemberFactory,
)

pytestmark = pytest.mark.django_db


def test_active_manager():
    FamilyMemberFactory()

    assert FamilyMemberFactory._meta.model.objects.active().count() == 1


def test_next_of_kin_manager():
    FamilyMemberFactory(
        is_next_of_kin=True,
    )

    assert FamilyMemberFactory._meta.model.objects.next_of_kin().count() == 1


def test_emergency_contact_manager():
    FamilyMemberFactory(
        is_emergency_contact=True,
    )

    assert FamilyMemberFactory._meta.model.objects.emergency_contacts().count() == 1


def test_search_manager():
    FamilyMemberFactory(
        first_name="Robert",
    )

    assert (
        FamilyMemberFactory._meta.model.objects.search(
            "Robert",
        ).count()
        == 1
    )


def test_patient_manager():
    member = FamilyMemberFactory()

    assert (
        FamilyMemberFactory._meta.model.objects.for_patient(
            member.patient.id,
        ).count()
        == 1
    )

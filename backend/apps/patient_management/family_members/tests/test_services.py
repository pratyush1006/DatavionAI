"""
Service tests for the Family Members module.
"""

from __future__ import annotations

import pytest

from apps.patient_management.family_members.services import (
    mark_as_emergency_contact,
    mark_as_next_of_kin,
    remove_emergency_contact,
    remove_next_of_kin,
    update_family_member,
)
from apps.patient_management.family_members.tests.factories import (
    FamilyMemberFactory,
)

pytestmark = pytest.mark.django_db


def test_update_family_member():
    member = FamilyMemberFactory()

    update_family_member(
        family_member=member,
        first_name="Updated",
    )

    member.refresh_from_db()

    assert member.first_name == "Updated"


def test_mark_next_of_kin():
    member = FamilyMemberFactory()

    mark_as_next_of_kin(member)

    member.refresh_from_db()

    assert member.is_next_of_kin


def test_remove_next_of_kin():
    member = FamilyMemberFactory(
        is_next_of_kin=True,
    )

    remove_next_of_kin(member)

    member.refresh_from_db()

    assert not member.is_next_of_kin


def test_mark_emergency_contact():
    member = FamilyMemberFactory()

    mark_as_emergency_contact(member)

    member.refresh_from_db()

    assert member.is_emergency_contact


def test_remove_emergency_contact():
    member = FamilyMemberFactory(
        is_emergency_contact=True,
    )

    remove_emergency_contact(member)

    member.refresh_from_db()

    assert not member.is_emergency_contact

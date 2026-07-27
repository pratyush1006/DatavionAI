"""
Model tests for Family Members.
"""

from __future__ import annotations

import pytest

from apps.patient_management.family_members.tests.factories import (
    FamilyMemberFactory,
)

pytestmark = pytest.mark.django_db


def test_create_family_member():
    member = FamilyMemberFactory()

    assert member.id is not None


def test_full_name():
    member = FamilyMemberFactory(
        first_name="John",
        middle_name="A",
        last_name="Doe",
    )

    assert member.full_name == "John A Doe"


def test_string_representation():
    member = FamilyMemberFactory(
        first_name="John",
        last_name="Doe",
    )

    assert "John Doe" in str(member)


def test_soft_delete():
    member = FamilyMemberFactory()

    member.delete()

    assert member.is_deleted is True


def test_restore():
    member = FamilyMemberFactory()

    member.delete()

    member.restore()

    assert member.is_deleted is False

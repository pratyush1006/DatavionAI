"""
Service tests for Patient Family Members.
"""

from __future__ import annotations

import pytest
from django.core.exceptions import ValidationError

from apps.patient_management.family_members.constants import (
    FamilyMemberStatus,
)
from apps.patient_management.family_members.services import FamilyMemberService
from apps.patient_management.family_members.tests.factories import (
    FamilyMemberFactory,
)

pytestmark = pytest.mark.django_db


def test_update_family_member():
    member = FamilyMemberFactory()

    FamilyMemberService.update(
        instance=member,
        validated_data={"first_name": "Updated"},
    )

    member.refresh_from_db()

    assert member.first_name == "Updated"


def test_mark_next_of_kin():
    member = FamilyMemberFactory()

    FamilyMemberService.mark_next_of_kin(
        instance=member,
    )

    member.refresh_from_db()

    assert member.is_next_of_kin


def test_remove_next_of_kin():
    member = FamilyMemberFactory(
        is_next_of_kin=True,
    )

    FamilyMemberService.remove_next_of_kin(
        instance=member,
    )

    member.refresh_from_db()

    assert not member.is_next_of_kin


def test_mark_emergency_contact():
    member = FamilyMemberFactory()

    FamilyMemberService.mark_emergency_contact(
        instance=member,
    )

    member.refresh_from_db()

    assert member.is_emergency_contact


def test_remove_emergency_contact():
    member = FamilyMemberFactory(
        is_emergency_contact=True,
    )

    FamilyMemberService.remove_emergency_contact(
        instance=member,
    )

    member.refresh_from_db()

    assert not member.is_emergency_contact


def test_deactivate_clears_special_flags():
    member = FamilyMemberFactory(
        is_next_of_kin=True,
        is_emergency_contact=True,
    )

    FamilyMemberService.deactivate(
        instance=member,
    )

    member.refresh_from_db()

    assert member.status == FamilyMemberStatus.INACTIVE
    assert not member.is_active
    assert not member.is_next_of_kin
    assert not member.is_emergency_contact


def test_deleted_member_cannot_be_updated():
    member = FamilyMemberFactory()

    member.delete()

    with pytest.raises(ValidationError):
        FamilyMemberService.update(
            instance=member,
            validated_data={"first_name": "Updated"},
        )


def test_deleted_member_cannot_be_next_of_kin():
    member = FamilyMemberFactory()

    member.delete()

    with pytest.raises(ValidationError):
        FamilyMemberService.mark_next_of_kin(
            instance=member,
        )


def test_deleted_member_cannot_be_emergency_contact():
    member = FamilyMemberFactory()

    member.delete()

    with pytest.raises(ValidationError):
        FamilyMemberService.mark_emergency_contact(
            instance=member,
        )


def test_inactive_member_cannot_be_next_of_kin():
    member = FamilyMemberFactory(
        status=FamilyMemberStatus.INACTIVE,
        is_active=False,
    )

    with pytest.raises(ValidationError):
        FamilyMemberService.mark_next_of_kin(
            instance=member,
        )

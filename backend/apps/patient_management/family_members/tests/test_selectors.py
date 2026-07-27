"""
Selector tests for the Family Members module.
"""

from __future__ import annotations

import pytest

from apps.patient_management.family_members.selectors import (
    count_patient_family_members,
    get_family_member_by_id,
    get_next_of_kin,
    list_patient_family_members,
)
from apps.patient_management.family_members.tests.factories import (
    FamilyMemberFactory,
)

pytestmark = pytest.mark.django_db


def test_get_family_member_by_id():
    member = FamilyMemberFactory()

    result = get_family_member_by_id(
        member.id,
    )

    assert result == member


def test_list_patient_family_members():
    member = FamilyMemberFactory()

    queryset = list_patient_family_members(
        member.patient.id,
    )

    assert member in queryset


def test_count_patient_family_members():
    member = FamilyMemberFactory()

    assert (
        count_patient_family_members(
            member.patient.id,
        )
        == 1
    )


def test_get_next_of_kin():
    member = FamilyMemberFactory(
        is_next_of_kin=True,
    )

    queryset = get_next_of_kin(
        member.patient.id,
    )

    assert member in queryset

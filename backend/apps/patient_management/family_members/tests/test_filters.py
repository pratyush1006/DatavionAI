"""
Filter tests for the Family Members module.
"""

from __future__ import annotations

import pytest

from apps.patient_management.family_members.api.filters import (
    FamilyMemberFilter,
)
from apps.patient_management.family_members.models import (
    FamilyMember,
)
from apps.patient_management.family_members.tests.factories import (
    FamilyMemberFactory,
)

pytestmark = pytest.mark.django_db


def test_filter_patient():
    member = FamilyMemberFactory()

    queryset = FamilyMember.objects.all()

    filtered = FamilyMemberFilter(
        {
            "patient": member.patient.id,
        },
        queryset=queryset,
    )

    assert filtered.qs.count() == 1


def test_filter_next_of_kin():
    FamilyMemberFactory(
        is_next_of_kin=True,
    )

    queryset = FamilyMember.objects.all()

    filtered = FamilyMemberFilter(
        {
            "is_next_of_kin": True,
        },
        queryset=queryset,
    )

    assert filtered.qs.count() == 1


def test_filter_emergency_contact():
    FamilyMemberFactory(
        is_emergency_contact=True,
    )

    queryset = FamilyMember.objects.all()

    filtered = FamilyMemberFilter(
        {
            "is_emergency_contact": True,
        },
        queryset=queryset,
    )

    assert filtered.qs.count() == 1

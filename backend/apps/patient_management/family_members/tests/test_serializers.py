"""
Serializer tests for the Family Members module.
"""

from __future__ import annotations

import pytest

from apps.patient_management.family_members.api.serializers import (
    FamilyMemberCreateSerializer,
    FamilyMemberDetailSerializer,
    FamilyMemberListSerializer,
    FamilyMemberUpdateSerializer,
)
from apps.patient_management.family_members.tests.factories import (
    FamilyMemberFactory,
)

pytestmark = pytest.mark.django_db


def test_create_serializer():
    serializer = FamilyMemberCreateSerializer()

    assert serializer is not None


def test_update_serializer():
    serializer = FamilyMemberUpdateSerializer()

    assert serializer is not None


def test_list_serializer():
    member = FamilyMemberFactory()

    serializer = FamilyMemberListSerializer(member)

    assert serializer.data["id"] == str(member.id)


def test_detail_serializer():
    member = FamilyMemberFactory()

    serializer = FamilyMemberDetailSerializer(member)

    assert serializer.data["id"] == str(member.id)

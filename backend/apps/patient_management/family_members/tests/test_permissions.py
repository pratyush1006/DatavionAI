"""
Permission tests for the Family Members module.
"""

from __future__ import annotations

from apps.patient_management.family_members.permissions import (
    FamilyMemberPermission,
)


def test_permission_constants():
    assert FamilyMemberPermission.CREATE == "patient_management.family_members.create"

    assert FamilyMemberPermission.UPDATE == "patient_management.family_members.update"

    assert FamilyMemberPermission.DELETE == "patient_management.family_members.delete"

    assert FamilyMemberPermission.VIEW == "patient_management.family_members.view"

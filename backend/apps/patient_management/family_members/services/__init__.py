"""
Public Family Member service API.
"""

from .family_member import (
    FamilyMemberService,
    activate_family_member,
    create_family_member,
    deactivate_family_member,
    delete_family_member,
    mark_as_emergency_contact,
    mark_as_next_of_kin,
    remove_emergency_contact,
    remove_next_of_kin,
    restore_family_member,
    update_family_member,
)

__all__ = (
    "FamilyMemberService",
    "activate_family_member",
    "create_family_member",
    "deactivate_family_member",
    "delete_family_member",
    "mark_as_emergency_contact",
    "mark_as_next_of_kin",
    "remove_emergency_contact",
    "remove_next_of_kin",
    "restore_family_member",
    "update_family_member",
)

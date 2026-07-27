"""
Permissions for the Family Members module.
"""

from __future__ import annotations

__all__ = [
    "FamilyMemberPermission",
]


class FamilyMemberPermission:
    """
    Permission constants for the Family Members module.
    """

    MODULE = "patient_management.family_members"

    VIEW = f"{MODULE}.view"
    LIST = f"{MODULE}.list"
    CREATE = f"{MODULE}.create"
    UPDATE = f"{MODULE}.update"
    DELETE = f"{MODULE}.delete"
    RESTORE = f"{MODULE}.restore"

    VIEW_SENSITIVE = f"{MODULE}.view_sensitive"

    MANAGE_NEXT_OF_KIN = f"{MODULE}.manage_next_of_kin"
    MANAGE_EMERGENCY_CONTACT = f"{MODULE}.manage_emergency_contact"

    EXPORT = f"{MODULE}.export"
    IMPORT = f"{MODULE}.import"

    ALL = (
        VIEW,
        LIST,
        CREATE,
        UPDATE,
        DELETE,
        RESTORE,
        VIEW_SENSITIVE,
        MANAGE_NEXT_OF_KIN,
        MANAGE_EMERGENCY_CONTACT,
        EXPORT,
        IMPORT,
    )

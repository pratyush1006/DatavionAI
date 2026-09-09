"""
Permission constants for the Patient Relationships module.

Permissions are stable application-level identifiers consumed by policies
and the platform RBAC engine.
"""

from __future__ import annotations


class PatientRelationshipPermission:
    """
    Stable permissions for Patient Relationships.
    """

    MODULE = "patient_management.relationships"

    VIEW = f"{MODULE}.view"
    LIST = f"{MODULE}.list"
    CREATE = f"{MODULE}.create"
    UPDATE = f"{MODULE}.update"
    DELETE = f"{MODULE}.delete"
    RESTORE = f"{MODULE}.restore"

    VERIFY = f"{MODULE}.verify"
    TERMINATE = f"{MODULE}.terminate"
    SET_PRIMARY = f"{MODULE}.set_primary"

    EXPORT = f"{MODULE}.export"
    IMPORT = f"{MODULE}.import"

    ALL = (
        VIEW,
        LIST,
        CREATE,
        UPDATE,
        DELETE,
        RESTORE,
        VERIFY,
        TERMINATE,
        SET_PRIMARY,
        EXPORT,
        IMPORT,
    )


__all__ = ("PatientRelationshipPermission",)

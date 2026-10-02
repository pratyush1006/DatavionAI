"""
RBAC permission identifiers for Patient Consents.
"""

from __future__ import annotations


class PatientConsentPermission:
    """
    Stable RBAC permission codes for Patient Consents.
    """

    MODULE = "patient_management.consents"

    VIEW = f"{MODULE}.view"
    LIST = f"{MODULE}.list"
    CREATE = f"{MODULE}.create"
    UPDATE = f"{MODULE}.update"
    DELETE = f"{MODULE}.delete"
    RESTORE = f"{MODULE}.restore"
    GRANT = f"{MODULE}.grant"
    REVOKE = f"{MODULE}.revoke"

    ALL = (
        VIEW,
        LIST,
        CREATE,
        UPDATE,
        DELETE,
        RESTORE,
        GRANT,
        REVOKE,
    )


__all__ = ("PatientConsentPermission",)

"""
Permission constants for the Patient Consents module.
"""

from __future__ import annotations

__all__ = [
    "ConsentPermission",
]


class ConsentPermission:
    """
    Permission codes for Patient Consents.
    """

    VIEW = "patient_management.consents.view"
    LIST = "patient_management.consents.list"

    CREATE = "patient_management.consents.create"
    UPDATE = "patient_management.consents.update"
    DELETE = "patient_management.consents.delete"

    GRANT = "patient_management.consents.grant"
    REVOKE = "patient_management.consents.revoke"
    WITHDRAW = "patient_management.consents.withdraw"
    EXPIRE = "patient_management.consents.expire"

    EXPORT = "patient_management.consents.export"
    IMPORT = "patient_management.consents.import"

    ALL = (
        VIEW,
        LIST,
        CREATE,
        UPDATE,
        DELETE,
        GRANT,
        REVOKE,
        WITHDRAW,
        EXPIRE,
        EXPORT,
        IMPORT,
    )

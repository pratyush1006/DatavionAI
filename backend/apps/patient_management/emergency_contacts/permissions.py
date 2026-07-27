"""
Permissions for the Emergency Contacts module.
"""

from __future__ import annotations


class EmergencyContactPermissions:
    """
    Emergency contact permissions.
    """

    VIEW = "patient_management.view_emergencycontact"

    CREATE = "patient_management.add_emergencycontact"

    UPDATE = "patient_management.change_emergencycontact"

    DELETE = "patient_management.delete_emergencycontact"

    VERIFY = "patient_management.verify_emergencycontact"

    SET_PRIMARY = "patient_management.set_primary_emergencycontact"


__all__ = [
    "EmergencyContactPermissions",
]

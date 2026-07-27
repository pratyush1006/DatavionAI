"""
Telemedicine permission classes.
"""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


class TelemedicinePermission:
    """
    Telemedicine permission codes.
    """

    VIEW = "telemedicine.view"
    CREATE = "telemedicine.create"
    UPDATE = "telemedicine.update"
    DELETE = "telemedicine.delete"
    START = "telemedicine.start"
    END = "telemedicine.end"
    RECORD = "telemedicine.record"


class CanViewTelemedicineSession(BasePermission):
    """
    Permission required to view telemedicine sessions.
    """

    permission_code = TelemedicinePermission.VIEW


class CanCreateTelemedicineSession(BasePermission):
    """
    Permission required to create telemedicine sessions.
    """

    permission_code = TelemedicinePermission.CREATE


class CanUpdateTelemedicineSession(BasePermission):
    """
    Permission required to update telemedicine sessions.
    """

    permission_code = TelemedicinePermission.UPDATE


class CanDeleteTelemedicineSession(BasePermission):
    """
    Permission required to delete telemedicine sessions.
    """

    permission_code = TelemedicinePermission.DELETE


class CanStartTelemedicineSession(BasePermission):
    """
    Permission required to start a telemedicine session.
    """

    permission_code = TelemedicinePermission.START


class CanEndTelemedicineSession(BasePermission):
    """
    Permission required to end a telemedicine session.
    """

    permission_code = TelemedicinePermission.END


class CanRecordTelemedicineSession(BasePermission):
    """
    Permission required to record a telemedicine session.
    """

    permission_code = TelemedicinePermission.RECORD


__all__ = [
    "CanCreateTelemedicineSession",
    "CanDeleteTelemedicineSession",
    "CanEndTelemedicineSession",
    "CanRecordTelemedicineSession",
    "CanStartTelemedicineSession",
    "CanUpdateTelemedicineSession",
    "CanViewTelemedicineSession",
    "TelemedicinePermission",
]

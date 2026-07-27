"""
Permission classes for the Communication module.
"""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


class PatientCommunicationPermission:
    VIEW = "communication.view"
    CREATE = "communication.create"
    UPDATE = "communication.update"
    DELETE = "communication.delete"


class CanViewPatientCommunication(BasePermission):
    permission_code = PatientCommunicationPermission.VIEW


class CanCreatePatientCommunication(BasePermission):
    permission_code = PatientCommunicationPermission.CREATE


class CanUpdatePatientCommunication(BasePermission):
    permission_code = PatientCommunicationPermission.UPDATE


class CanDeletePatientCommunication(BasePermission):
    permission_code = PatientCommunicationPermission.DELETE


__all__ = [
    "CanCreatePatientCommunication",
    "CanDeletePatientCommunication",
    "CanUpdatePatientCommunication",
    "CanViewPatientCommunication",
    "PatientCommunicationPermission",
]

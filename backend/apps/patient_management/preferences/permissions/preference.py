"""RBAC permission adapters for Patient Preferences."""

from __future__ import annotations

from apps.platform.rbac.permissions.base import RBACPermissionBase


class PatientPreferencePermission(RBACPermissionBase):
    """Base RBAC adapter for Patient Preferences."""

    module = "patient_preferences"

    LIST = "patient_preferences.list"
    VIEW = "patient_preferences.view"
    CREATE = "patient_preferences.create"
    UPDATE = "patient_preferences.update"
    DELETE = "patient_preferences.delete"
    RESTORE = "patient_preferences.restore"
    COMMUNICATION_MANAGE = "patient_preferences.communication_manage"


class CanListPatientPreferences(PatientPreferencePermission):
    """Authorize preference listing."""

    permission = "patient_preferences.list"


class CanViewPatientPreference(PatientPreferencePermission):
    """Authorize preference viewing."""

    permission = "patient_preferences.view"


class CanCreatePatientPreference(PatientPreferencePermission):
    """Authorize preference creation."""

    permission = "patient_preferences.create"


class CanUpdatePatientPreference(PatientPreferencePermission):
    """Authorize preference updates."""

    permission = "patient_preferences.update"


class CanDeletePatientPreference(PatientPreferencePermission):
    """Authorize preference deletion."""

    permission = "patient_preferences.delete"


class CanRestorePatientPreference(PatientPreferencePermission):
    """Authorize preference restoration."""

    permission = "patient_preferences.restore"


class CanManageCommunicationPreference(PatientPreferencePermission):
    """Authorize communication preference mutations."""

    permission = "patient_preferences.communication_manage"


__all__ = (
    "CanCreatePatientPreference",
    "CanDeletePatientPreference",
    "CanListPatientPreferences",
    "CanManageCommunicationPreference",
    "CanRestorePatientPreference",
    "CanUpdatePatientPreference",
    "CanViewPatientPreference",
    "PatientPreferencePermission",
)

"""RBAC adapters for Patient Medical History APIs."""

from __future__ import annotations

from apps.platform.rbac.permissions.base import RBACPermissionBase


class CanViewMedicalHistory(RBACPermissionBase):
    """CanViewMedicalHistory implementation."""

    permission_code = "patient_medical_history.view"
    message = "You do not have permission to view medical history."


class CanListMedicalHistory(RBACPermissionBase):
    """CanListMedicalHistory implementation."""

    permission_code = "patient_medical_history.list"
    message = "You do not have permission to list medical history."


class CanCreateMedicalHistory(RBACPermissionBase):
    """CanCreateMedicalHistory implementation."""

    permission_code = "patient_medical_history.create"
    message = "You do not have permission to create medical history."


class CanUpdateMedicalHistory(RBACPermissionBase):
    """CanUpdateMedicalHistory implementation."""

    permission_code = "patient_medical_history.update"
    message = "You do not have permission to update medical history."


class CanDeleteMedicalHistory(RBACPermissionBase):
    """CanDeleteMedicalHistory implementation."""

    permission_code = "patient_medical_history.delete"
    message = "You do not have permission to delete medical history."


class CanRestoreMedicalHistory(RBACPermissionBase):
    """CanRestoreMedicalHistory implementation."""

    permission_code = "patient_medical_history.restore"
    message = "You do not have permission to restore medical history."


class CanActivateMedicalHistory(RBACPermissionBase):
    """CanActivateMedicalHistory implementation."""

    permission_code = "patient_medical_history.activate"
    message = "You do not have permission to activate medical history."


class CanDeactivateMedicalHistory(RBACPermissionBase):
    """CanDeactivateMedicalHistory implementation."""

    permission_code = "patient_medical_history.deactivate"
    message = "You do not have permission to deactivate medical history."


class CanVerifyMedicalHistory(RBACPermissionBase):
    """CanVerifyMedicalHistory implementation."""

    permission_code = "patient_medical_history.verify"
    message = "You do not have permission to verify medical history."


__all__ = (
    "CanViewMedicalHistory",
    "CanListMedicalHistory",
    "CanCreateMedicalHistory",
    "CanUpdateMedicalHistory",
    "CanDeleteMedicalHistory",
    "CanRestoreMedicalHistory",
    "CanActivateMedicalHistory",
    "CanDeactivateMedicalHistory",
    "CanVerifyMedicalHistory",
)

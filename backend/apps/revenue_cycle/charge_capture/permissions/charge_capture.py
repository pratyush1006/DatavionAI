"""
Permission classes for the Charge Capture module.
"""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


class ChargeCapturePermission:
    VIEW = "charge_capture.view"
    CREATE = "charge_capture.create"
    UPDATE = "charge_capture.update"
    DELETE = "charge_capture.delete"


class CanViewChargeCapture(BasePermission):
    permission_code = ChargeCapturePermission.VIEW


class CanCreateChargeCapture(BasePermission):
    permission_code = ChargeCapturePermission.CREATE


class CanUpdateChargeCapture(BasePermission):
    permission_code = ChargeCapturePermission.UPDATE


class CanDeleteChargeCapture(BasePermission):
    permission_code = ChargeCapturePermission.DELETE


__all__ = [
    "CanCreateChargeCapture",
    "CanDeleteChargeCapture",
    "CanUpdateChargeCapture",
    "CanViewChargeCapture",
    "ChargeCapturePermission",
]

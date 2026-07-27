"""
Permission classes for the Claim Denial module.
"""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


class ClaimDenialPermission:
    VIEW = "denials.view"
    CREATE = "denials.create"
    UPDATE = "denials.update"
    DELETE = "denials.delete"


class CanViewClaimDenial(BasePermission):
    permission_code = ClaimDenialPermission.VIEW


class CanCreateClaimDenial(BasePermission):
    permission_code = ClaimDenialPermission.CREATE


class CanUpdateClaimDenial(BasePermission):
    permission_code = ClaimDenialPermission.UPDATE


class CanDeleteClaimDenial(BasePermission):
    permission_code = ClaimDenialPermission.DELETE


__all__ = [
    "CanCreateClaimDenial",
    "CanDeleteClaimDenial",
    "CanUpdateClaimDenial",
    "CanViewClaimDenial",
    "ClaimDenialPermission",
]

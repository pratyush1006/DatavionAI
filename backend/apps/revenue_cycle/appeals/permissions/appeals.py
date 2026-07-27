"""
Permission classes for the Claim Appeal module.
"""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


class ClaimAppealPermission:
    VIEW = "appeals.view"
    CREATE = "appeals.create"
    UPDATE = "appeals.update"
    DELETE = "appeals.delete"


class CanViewClaimAppeal(BasePermission):
    permission_code = ClaimAppealPermission.VIEW


class CanCreateClaimAppeal(BasePermission):
    permission_code = ClaimAppealPermission.CREATE


class CanUpdateClaimAppeal(BasePermission):
    permission_code = ClaimAppealPermission.UPDATE


class CanDeleteClaimAppeal(BasePermission):
    permission_code = ClaimAppealPermission.DELETE


__all__ = [
    "CanCreateClaimAppeal",
    "CanDeleteClaimAppeal",
    "CanUpdateClaimAppeal",
    "CanViewClaimAppeal",
    "ClaimAppealPermission",
]

"""
Permission classes for the Prior Authorization module.
"""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


class PriorAuthorizationRequestPermission:
    VIEW = "prior_authorization.view"
    CREATE = "prior_authorization.create"
    UPDATE = "prior_authorization.update"
    DELETE = "prior_authorization.delete"


class CanViewPriorAuthorizationRequest(BasePermission):
    permission_code = PriorAuthorizationRequestPermission.VIEW


class CanCreatePriorAuthorizationRequest(BasePermission):
    permission_code = PriorAuthorizationRequestPermission.CREATE


class CanUpdatePriorAuthorizationRequest(BasePermission):
    permission_code = PriorAuthorizationRequestPermission.UPDATE


class CanDeletePriorAuthorizationRequest(BasePermission):
    permission_code = PriorAuthorizationRequestPermission.DELETE


__all__ = [
    "CanCreatePriorAuthorizationRequest",
    "CanDeletePriorAuthorizationRequest",
    "CanUpdatePriorAuthorizationRequest",
    "CanViewPriorAuthorizationRequest",
    "PriorAuthorizationRequestPermission",
]

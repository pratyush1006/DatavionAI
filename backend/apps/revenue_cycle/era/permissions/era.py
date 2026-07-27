"""
Permission classes for the Remittance Advice module.
"""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


class RemittanceAdvicePermission:
    VIEW = "era.view"
    CREATE = "era.create"
    UPDATE = "era.update"
    DELETE = "era.delete"


class CanViewRemittanceAdvice(BasePermission):
    permission_code = RemittanceAdvicePermission.VIEW


class CanCreateRemittanceAdvice(BasePermission):
    permission_code = RemittanceAdvicePermission.CREATE


class CanUpdateRemittanceAdvice(BasePermission):
    permission_code = RemittanceAdvicePermission.UPDATE


class CanDeleteRemittanceAdvice(BasePermission):
    permission_code = RemittanceAdvicePermission.DELETE


__all__ = [
    "CanCreateRemittanceAdvice",
    "CanDeleteRemittanceAdvice",
    "CanUpdateRemittanceAdvice",
    "CanViewRemittanceAdvice",
    "RemittanceAdvicePermission",
]

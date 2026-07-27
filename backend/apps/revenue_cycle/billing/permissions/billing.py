"""
Permission classes for the Billing Batch module.
"""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


class BillingBatchPermission:
    VIEW = "billing.view"
    CREATE = "billing.create"
    UPDATE = "billing.update"
    DELETE = "billing.delete"


class CanViewBillingBatch(BasePermission):
    permission_code = BillingBatchPermission.VIEW


class CanCreateBillingBatch(BasePermission):
    permission_code = BillingBatchPermission.CREATE


class CanUpdateBillingBatch(BasePermission):
    permission_code = BillingBatchPermission.UPDATE


class CanDeleteBillingBatch(BasePermission):
    permission_code = BillingBatchPermission.DELETE


__all__ = [
    "CanCreateBillingBatch",
    "CanDeleteBillingBatch",
    "CanUpdateBillingBatch",
    "CanViewBillingBatch",
    "BillingBatchPermission",
]

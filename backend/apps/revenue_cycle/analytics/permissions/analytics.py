"""
Permission classes for the RCM Metric module.
"""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


class RcmMetricPermission:
    VIEW = "analytics.view"
    CREATE = "analytics.create"
    UPDATE = "analytics.update"
    DELETE = "analytics.delete"


class CanViewRcmMetric(BasePermission):
    permission_code = RcmMetricPermission.VIEW


class CanCreateRcmMetric(BasePermission):
    permission_code = RcmMetricPermission.CREATE


class CanUpdateRcmMetric(BasePermission):
    permission_code = RcmMetricPermission.UPDATE


class CanDeleteRcmMetric(BasePermission):
    permission_code = RcmMetricPermission.DELETE


__all__ = [
    "CanCreateRcmMetric",
    "CanDeleteRcmMetric",
    "CanUpdateRcmMetric",
    "CanViewRcmMetric",
    "RcmMetricPermission",
]

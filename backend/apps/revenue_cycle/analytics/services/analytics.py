"""
RCM Metric services.
"""

from __future__ import annotations

from apps.revenue_cycle.analytics.models import RcmMetric
from apps.revenue_cycle.components import RcmService

create_metric = None
update_metric = None
delete_metric = None


class RcmMetricService(RcmService):
    """
    Write-side operations for rcm metric records.
    """

    model = RcmMetric


create_metric = RcmMetricService.create
update_metric = RcmMetricService.update
delete_metric = RcmMetricService.delete


__all__ = [
    "RcmMetricService",
    "create_metric",
    "delete_metric",
    "update_metric",
]

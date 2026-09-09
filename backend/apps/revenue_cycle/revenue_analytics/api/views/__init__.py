"""Revenue Analytics API views."""

from __future__ import annotations

from .revenue_analytics import (
    RevenueAnalyticsGenerateAPIView,
    RevenueAnalyticsListAPIView,
)

__all__ = (
    "RevenueAnalyticsGenerateAPIView",
    "RevenueAnalyticsListAPIView",
)

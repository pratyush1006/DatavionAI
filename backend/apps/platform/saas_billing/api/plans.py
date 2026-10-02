"""
DatavionOS SaaS Billing Plan Catalog API.

Canonical endpoint:

    GET /api/saas-billing/plans/

The existing canonical PlanListAPIView owns the actual
query and serialization behaviour.
"""

from __future__ import annotations

from .views.plan import PlanListAPIView

PlanCatalogAPIView = PlanListAPIView


__all__ = [
    "PlanCatalogAPIView",
    "PlanListAPIView",
]

"""Public billing routes owned by the Revenue Cycle boundary."""

from __future__ import annotations

from django.urls import include, path

urlpatterns = (
    path(
        "patient-billing/",
        include("apps.revenue_cycle.billing.patient_billing.api.urls"),
    ),
    path(
        "accounts-receivable/",
        include("apps.revenue_cycle.billing.accounts_receivable.api.urls"),
    ),
)

__all__ = ("urlpatterns",)

"""Root Revenue Cycle URL configuration."""

from __future__ import annotations

from django.urls import include, path

urlpatterns = (
    path(
        "analytics/",
        include("apps.revenue_cycle.revenue_analytics.urls"),
    ),
    path(
        "appeals/",
        include("apps.revenue_cycle.appeals.urls"),
    ),
    path(
        "ar/",
        include("apps.revenue_cycle.accounts_receivable.urls"),
    ),
    path(
        "billing/",
        include("apps.revenue_cycle.billing.api_urls"),
    ),
    path(
        "charge_capture/",
        include("apps.revenue_cycle.charge_capture.urls"),
    ),
    path(
        "claim_scrubbing/",
        include("apps.revenue_cycle.claim_scrubbing.urls"),
    ),
    path(
        "claim_submission/",
        include("apps.revenue_cycle.claim_submission.urls"),
    ),
    path(
        "coding/",
        include("apps.revenue_cycle.coding.urls"),
    ),
    path(
        "denials/",
        include("apps.revenue_cycle.denials.urls"),
    ),
    path(
        "eligibility/",
        include("apps.revenue_cycle.eligibility.urls"),
    ),
    path(
        "era/",
        include("apps.revenue_cycle.era.urls"),
    ),
    path(
        "insurance_verification/",
        include("apps.revenue_cycle.insurance_verification.urls"),
    ),
    path(
        "payment_posting/",
        include("apps.revenue_cycle.payment_posting.urls"),
    ),
    path(
        "prior_authorization/",
        include("apps.revenue_cycle.prior_authorization.urls"),
    ),
)


__all__ = ("urlpatterns",)

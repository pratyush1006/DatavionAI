"""
Revenue Cycle Management URL configuration.

Aggregates the URL patterns of every RCM submodule under a single
``revenue-cycle`` namespace prefix.
"""

from __future__ import annotations

from django.urls import include, path

app_name = "revenue_cycle"

urlpatterns = [
    path(
        "insurance-verifications/",
        include(
            "apps.revenue_cycle.insurance_verification.urls",
        ),
    ),
    path(
        "eligibilities/",
        include(
            "apps.revenue_cycle.eligibility.urls",
        ),
    ),
    path(
        "prior-authorizations/",
        include(
            "apps.revenue_cycle.prior_authorization.urls",
        ),
    ),
    path(
        "coding/",
        include(
            "apps.revenue_cycle.coding.urls",
        ),
    ),
    path(
        "charge-captures/",
        include(
            "apps.revenue_cycle.charge_capture.urls",
        ),
    ),
    path(
        "claim-scrubbing/",
        include(
            "apps.revenue_cycle.claim_scrubbing.urls",
        ),
    ),
    path(
        "claim-submissions/",
        include(
            "apps.revenue_cycle.claim_submission.urls",
        ),
    ),
    path(
        "eras/",
        include(
            "apps.revenue_cycle.era.urls",
        ),
    ),
    path(
        "payment-postings/",
        include(
            "apps.revenue_cycle.payment_posting.urls",
        ),
    ),
    path(
        "denials/",
        include(
            "apps.revenue_cycle.denials.urls",
        ),
    ),
    path(
        "appeals/",
        include(
            "apps.revenue_cycle.appeals.urls",
        ),
    ),
    path(
        "ar/",
        include(
            "apps.revenue_cycle.ar.urls",
        ),
    ),
    path(
        "billing/",
        include(
            "apps.revenue_cycle.billing.urls",
        ),
    ),
    path(
        "analytics/",
        include(
            "apps.revenue_cycle.analytics.urls",
        ),
    ),
]

__all__ = [
    "app_name",
    "urlpatterns",
]

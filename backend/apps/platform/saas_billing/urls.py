"""
Canonical SaaS Billing URL configuration.
"""

from __future__ import annotations

from django.urls import include, path

app_name = "saas-billing"


urlpatterns = [
    path(
        "",
        include(
            "apps.platform.saas_billing.api.urls",
        ),
    ),
]

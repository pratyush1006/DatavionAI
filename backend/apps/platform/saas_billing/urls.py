"""
DatavionOS SaaS Billing URLs.

Module URL entry point.

Routes:

- API
- Future web/admin routes
"""

from __future__ import annotations

from django.urls import include, path

app_name = "saas_billing"


urlpatterns = [
    path(
        "",
        include(
            "apps.platform.saas_billing.api.urls",
        ),
    ),
]

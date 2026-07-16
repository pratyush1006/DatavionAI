"""
URL configuration for the Laboratories application.
"""

from __future__ import annotations

from django.urls import (
    include,
    path,
)

urlpatterns = [
    path(
        "orders/",
        include(
            "apps.clinical.laboratories.api.urls.laboratory_order",
        ),
    ),
    path(
        "tests/",
        include(
            "apps.clinical.laboratories.api.urls.laboratory_test",
        ),
    ),
    path(
        "results/",
        include(
            "apps.clinical.laboratories.api.urls.laboratory_result",
        ),
    ),
]

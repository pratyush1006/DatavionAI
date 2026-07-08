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
            "apps.laboratories.api.urls.laboratory_order",
        ),
    ),
    path(
        "tests/",
        include(
            "apps.laboratories.api.urls.laboratory_test",
        ),
    ),
    path(
        "results/",
        include(
            "apps.laboratories.api.urls.laboratory_result",
        ),
    ),
]

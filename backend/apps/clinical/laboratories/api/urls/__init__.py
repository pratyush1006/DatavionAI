"""
URL configuration for the Laboratories application.


#from __future__ import annotations

from django.urls import (
    include,
    path,
)

app_name = "laboratories"

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

__all__ = [
    "app_name",
    "urlpatterns",
]"""

"""
URL configuration for the Laboratories application.
"""

from django.urls import include, path

app_name = "laboratories"

urlpatterns = [
    path(
        "orders/",
        include(
            (
                "apps.clinical.laboratories.api.urls.laboratory_order",
                "laboratory_order",
            ),
            namespace="laboratory_order",
        ),
    ),
    path(
        "tests/",
        include(
            ("apps.clinical.laboratories.api.urls.laboratory_test", "laboratory_test"),
            namespace="laboratory_test",
        ),
    ),
    path(
        "results/",
        include(
            (
                "apps.clinical.laboratories.api.urls.laboratory_result",
                "laboratory_result",
            ),
            namespace="laboratory_result",
        ),
    ),
]

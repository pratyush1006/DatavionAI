from django.urls import path

from .views import (
    FinanceCollectionAPIView,
    FinanceHealthAPIView,
    FinanceWorkflowAPIView,
)

urlpatterns = [
    path("health/", FinanceHealthAPIView.as_view(), name="finance-health"),
    path(
        "<str:resource>/", FinanceCollectionAPIView.as_view(), name="finance-resource"
    ),
    path(
        "<str:resource>/<uuid:object_id>/",
        FinanceWorkflowAPIView.as_view(),
        name="finance-resource-detail",
    ),
]

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .health import ImagingHealthAPIView
from .views import (
    ImagingContractAPIView,
    ImagingModalityViewSet,
    ImagingOrderViewSet,
    ImagingProcedureViewSet,
    ImagingStudyViewSet,
    RadiologyReportViewSet,
)

router = DefaultRouter()
router.register("modalities", ImagingModalityViewSet, basename="imaging-modality")
router.register("procedures", ImagingProcedureViewSet, basename="imaging-procedure")
router.register("orders", ImagingOrderViewSet, basename="imaging-order")
router.register("studies", ImagingStudyViewSet, basename="imaging-study")
router.register("reports", RadiologyReportViewSet, basename="radiology-report")

urlpatterns = [
    path("health/", ImagingHealthAPIView.as_view(), name="imaging-health"),
    path("contract/", ImagingContractAPIView.as_view(), name="imaging-contract"),
    path("", include(router.urls)),
]

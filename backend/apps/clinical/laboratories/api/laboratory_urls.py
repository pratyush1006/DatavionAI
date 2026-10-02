from rest_framework.routers import DefaultRouter

from .views import (
    LaboratoryOrderViewSet,
    LaboratoryReportViewSet,
    LaboratoryResultViewSet,
    LaboratorySpecimenViewSet,
    LaboratoryTestViewSet,
    LaboratoryViewSet,
)

router = DefaultRouter()
router.register("laboratories", LaboratoryViewSet, basename="laboratory")
router.register("orders", LaboratoryOrderViewSet, basename="laboratory-order")
router.register("tests", LaboratoryTestViewSet, basename="laboratory-test")
router.register("specimens", LaboratorySpecimenViewSet, basename="laboratory-specimen")
router.register("results", LaboratoryResultViewSet, basename="laboratory-result")
router.register("reports", LaboratoryReportViewSet, basename="laboratory-report")

urlpatterns = router.urls

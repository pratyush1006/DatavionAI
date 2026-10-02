from rest_framework.routers import DefaultRouter

from .views import (
    CarePlanViewSet,
    ClinicalAlertViewSet,
    MedicationAdministrationViewSet,
    NurseScheduleViewSet,
    NursingTaskViewSet,
    PatientAssignmentViewSet,
    ShiftHandoverViewSet,
)

router = DefaultRouter()
router.register("assignments", PatientAssignmentViewSet, basename="nursing-assignment")
router.register("tasks", NursingTaskViewSet, basename="nursing-task")
router.register(
    "medication-administrations",
    MedicationAdministrationViewSet,
    basename="medication-administration",
)
router.register("care-plans", CarePlanViewSet, basename="nursing-care-plan")
router.register("alerts", ClinicalAlertViewSet, basename="nursing-alert")
router.register("schedules", NurseScheduleViewSet, basename="nurse-schedule")
router.register("handovers", ShiftHandoverViewSet, basename="nursing-handover")
urlpatterns = router.urls

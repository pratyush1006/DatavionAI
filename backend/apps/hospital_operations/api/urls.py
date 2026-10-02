from django.urls import path

from .views import (
    AdmissionCreateView,
    AdmissionDischargeView,
    AdmissionTransferView,
    BedAssignmentCreateView,
    BedCleaningCompleteView,
    BedListCreateView,
    BedListView,
    BedReservationCreateView,
    CapacitySetupCatalogView,
    FacilityListCreateView,
    OPDQueueView,
    OPDRegistrationView,
    OperationalUnitListCreateView,
    RoomListCreateView,
    RoomListView,
)

app_name = "hospital-operations-api"

urlpatterns = [
    path(
        "capacity-catalog/", CapacitySetupCatalogView.as_view(), name="capacity-catalog"
    ),
    path("facilities/", FacilityListCreateView.as_view(), name="facilities"),
    path("units/", OperationalUnitListCreateView.as_view(), name="units"),
    path("rooms/setup/", RoomListCreateView.as_view(), name="rooms-setup"),
    path("beds/setup/", BedListCreateView.as_view(), name="beds-setup"),
    path("beds/", BedListView.as_view(), name="beds"),
    path(
        "beds/reservations/",
        BedReservationCreateView.as_view(),
        name="bed-reservations",
    ),
    path(
        "beds/assignments/", BedAssignmentCreateView.as_view(), name="bed-assignments"
    ),
    path(
        "beds/<uuid:bed_id>/clean/",
        BedCleaningCompleteView.as_view(),
        name="bed-cleaning-complete",
    ),
    path("rooms/", RoomListView.as_view(), name="rooms"),
    path("opd/queues/<uuid:queue_id>/", OPDQueueView.as_view(), name="opd-queue"),
    path("opd/visits/", OPDRegistrationView.as_view(), name="opd-register"),
    path("admissions/", AdmissionCreateView.as_view(), name="admission-create"),
    path(
        "admissions/<uuid:admission_id>/transfer/",
        AdmissionTransferView.as_view(),
        name="admission-transfer",
    ),
    path(
        "admissions/<uuid:admission_id>/discharge/",
        AdmissionDischargeView.as_view(),
        name="admission-discharge",
    ),
]

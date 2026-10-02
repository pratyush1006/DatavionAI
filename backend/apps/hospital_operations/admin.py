from django.contrib import admin

from .models import (
    Admission,
    Bed,
    BedAssignment,
    Facility,
    OPDQueue,
    OPDVisit,
    OperationalEvent,
    OperationalUnit,
    PatientMovement,
    Room,
)

admin.site.register(
    [
        Facility,
        OperationalUnit,
        Room,
        Bed,
        BedAssignment,
        Admission,
        PatientMovement,
        OPDQueue,
        OPDVisit,
        OperationalEvent,
    ]
)

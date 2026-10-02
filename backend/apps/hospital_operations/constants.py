from enum import StrEnum


class FacilityStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"


class RoomStatus(StrEnum):
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    RESERVED = "reserved"
    CLEANING = "cleaning"
    MAINTENANCE = "maintenance"
    BLOCKED = "blocked"
    OUT_OF_SERVICE = "out_of_service"


class BedStatus(StrEnum):
    AVAILABLE = "available"
    RESERVED = "reserved"
    OCCUPIED = "occupied"
    CLEANING = "cleaning"
    MAINTENANCE = "maintenance"
    BLOCKED = "blocked"
    ISOLATION = "isolation"
    OUT_OF_SERVICE = "out_of_service"


class OPDVisitStatus(StrEnum):
    REGISTERED = "registered"
    WAITING = "waiting"
    CALLED = "called"
    IN_CONSULTATION = "in_consultation"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"


class MovementType(StrEnum):
    ADMISSION = "admission"
    TRANSFER = "transfer"
    ICU_TRANSFER = "icu_transfer"
    DISCHARGE = "discharge"


class AdmissionStatus(StrEnum):
    ADMITTED = "admitted"
    DISCHARGED = "discharged"
    CANCELLED = "cancelled"


class ReservationStatus(StrEnum):
    ACTIVE = "active"
    FULFILLED = "fulfilled"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


# Canonical RBAC permission codes. The existing platform RBAC remains
# authoritative; Hospital Operations only declares its required scopes.
RBAC_PERMISSIONS = {
    "view": "hospital_operations.view",
    "manage": "hospital_operations.manage",
    "admit": "hospital_operations.admit",
    "transfer": "hospital_operations.transfer",
    "discharge": "hospital_operations.discharge",
    "manage_opd": "hospital_operations.manage_opd",
}


# Controlled capacity master data. These values are exposed through the
# authenticated API rather than duplicated in the frontend, so organizations
# configure locations using the same governed vocabulary.
CAPACITY_SETUP_CATALOG = {
    "facilities": (
        {"id": "main_hospital", "name": "Main Hospital", "code": "MAIN"},
        {"id": "specialty_center", "name": "Specialty Care Center", "code": "SPEC"},
        {"id": "community_clinic", "name": "Community Clinic", "code": "CLINIC"},
        {"id": "diagnostic_center", "name": "Diagnostic Center", "code": "DIAG"},
    ),
    "units": (
        {"id": "general_ward", "name": "General Ward", "code": "WARD"},
        {"id": "intensive_care", "name": "Intensive Care Unit", "code": "ICU"},
        {"id": "emergency", "name": "Emergency Department", "code": "ED"},
        {"id": "maternity", "name": "Maternity Ward", "code": "MAT"},
        {"id": "pediatrics", "name": "Pediatrics Ward", "code": "PEDS"},
        {"id": "operating_theatre", "name": "Operating Theatre", "code": "OT"},
    ),
    "rooms": (
        {"id": "room_101", "name": "Room 101", "code": "101"},
        {"id": "room_102", "name": "Room 102", "code": "102"},
        {"id": "room_103", "name": "Room 103", "code": "103"},
        {"id": "room_201", "name": "Room 201", "code": "201"},
        {"id": "isolation_01", "name": "Isolation Room 01", "code": "ISO-01"},
    ),
    "beds": (
        {"id": "bed_a01", "name": "Bed A-01", "code": "A-01"},
        {"id": "bed_a02", "name": "Bed A-02", "code": "A-02"},
        {"id": "bed_b01", "name": "Bed B-01", "code": "B-01"},
        {"id": "bed_b02", "name": "Bed B-02", "code": "B-02"},
        {"id": "isolation_01", "name": "Isolation Bed 01", "code": "ISO-01"},
    ),
}

from .models import Bed, BedReservation, OPDVisit, Room


def available_beds(*, tenant, organization, unit_id=None):
    qs = Bed.objects.filter(
        tenant=tenant, organization=organization, status="available", active=True
    ).select_related("room", "room__unit")
    return qs.filter(room__unit_id=unit_id) if unit_id else qs


def occupied_beds(*, tenant, organization, unit_id=None):
    qs = Bed.objects.filter(
        tenant=tenant, organization=organization, status="occupied", active=True
    ).select_related("room", "room__unit")
    return qs.filter(room__unit_id=unit_id) if unit_id else qs


def reserved_beds(*, tenant, organization, unit_id=None):
    qs = BedReservation.objects.filter(
        tenant=tenant, organization=organization, status="active"
    ).select_related("bed", "bed__room", "bed__room__unit")
    return qs.filter(bed__room__unit_id=unit_id) if unit_id else qs


def room_occupancy(*, tenant, organization, unit_id=None):
    qs = Room.objects.filter(tenant=tenant, organization=organization)
    if unit_id:
        qs = qs.filter(unit_id=unit_id)
    return qs.prefetch_related("beds")


def opd_waiting_queue(*, tenant, organization, queue_id):
    return (
        OPDVisit.objects.filter(
            tenant=tenant,
            organization=organization,
            queue_id=queue_id,
            status="waiting",
        )
        .select_related("patient")
        .order_by("token_number")
    )


def unit_occupancy_summary(*, tenant, organization, unit_id=None):
    qs = Bed.objects.filter(tenant=tenant, organization=organization, active=True)
    if unit_id:
        qs = qs.filter(room__unit_id=unit_id)
    total = qs.count()
    occupied = qs.filter(status="occupied").count()
    return {
        "total_beds": total,
        "occupied_beds": occupied,
        "available_beds": qs.filter(status="available").count(),
        "utilization_ratio": (occupied / total) if total else 0.0,
    }

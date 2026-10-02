from datetime import timedelta
from decimal import Decimal
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from apps.pharmacy.constants import ReservationStatus
from apps.pharmacy.models import InventoryReservation, MedicationBatch
from apps.pharmacy.services.events import enqueue_event


def _positive(value):
    value = Decimal(str(value))
    if value <= 0:
        raise ValidationError("Reservation quantity must be greater than zero.")
    return value


def _expire_locked(batch):
    now = timezone.now()
    qs = InventoryReservation.objects.select_for_update().filter(
        batch=batch,
        status=ReservationStatus.ACTIVE,
        expires_at__isnull=False,
        expires_at__lte=now,
    )
    expired = list(qs)
    if expired:
        total = sum((r.quantity for r in expired), Decimal("0"))
        batch.quantity_reserved = max(batch.quantity_reserved - total, Decimal("0"))
        batch.save(update_fields=["quantity_reserved", "updated_at"])
        for reservation in expired:
            reservation.status = ReservationStatus.EXPIRED
            reservation.save(update_fields=["status", "updated_at"])


@transaction.atomic
def reserve_stock(
    *,
    organization,
    batch,
    quantity,
    reservation_number=None,
    reference_type="",
    reference_id=None,
    reserved_by_id=None,
    expires_at=None,
    ttl_minutes=30,
):
    quantity = _positive(quantity)
    batch = (
        MedicationBatch.objects.select_for_update()
        .select_related("product")
        .get(pk=batch.pk)
    )
    if batch.product.organization_id != organization.id:
        raise ValidationError("Inventory item is outside the organization scope.")
    _expire_locked(batch)
    if expires_at is None:
        expires_at = timezone.now() + timedelta(minutes=ttl_minutes)
    available = batch.quantity_available - batch.quantity_reserved
    if available < quantity:
        raise ValidationError("Insufficient available stock for reservation.")
    reservation_number = reservation_number or f"RES-{uuid4().hex[:20].upper()}"
    reservation = InventoryReservation.objects.create(
        organization=organization,
        batch=batch,
        reservation_number=reservation_number,
        quantity=quantity,
        reference_type=reference_type,
        reference_id=reference_id,
        reserved_by_id=reserved_by_id,
        expires_at=expires_at,
    )
    batch.quantity_reserved += quantity
    batch.save(update_fields=["quantity_reserved", "updated_at"])
    enqueue_event(
        organization=organization,
        event_type="pharmacy.stock_reserved",
        aggregate_type="InventoryReservation",
        aggregate_id=reservation.id,
        payload={
            "reservation_id": str(reservation.id),
            "batch_id": str(batch.id),
            "quantity": str(quantity),
            "expires_at": expires_at.isoformat() if expires_at else None,
        },
    )
    return reservation


@transaction.atomic
def release_reservation(*, organization, reservation):
    reservation = (
        InventoryReservation.objects.select_for_update()
        .select_related("batch__product")
        .get(pk=reservation.pk)
    )
    if reservation.organization_id != organization.id:
        raise ValidationError("Reservation is outside the organization scope.")
    if reservation.status != ReservationStatus.ACTIVE:
        return reservation
    batch = MedicationBatch.objects.select_for_update().get(pk=reservation.batch_id)
    batch.quantity_reserved = max(
        batch.quantity_reserved - reservation.quantity, Decimal("0")
    )
    batch.save(update_fields=["quantity_reserved", "updated_at"])
    reservation.status = ReservationStatus.RELEASED
    reservation.save(update_fields=["status", "updated_at"])
    enqueue_event(
        organization=organization,
        event_type="pharmacy.reservation_released",
        aggregate_type="InventoryReservation",
        aggregate_id=reservation.id,
        payload={
            "reservation_id": str(reservation.id),
            "batch_id": str(batch.id),
            "quantity": str(reservation.quantity),
        },
    )
    return reservation


def commit_reservation(*, organization, reservation):
    # Expiry must be persisted before raising the business validation error.
    # Keeping the expiry path outside a surrounding atomic block prevents the
    # release from being rolled back together with the expected exception.
    with transaction.atomic():
        reservation = (
            InventoryReservation.objects.select_for_update()
            .select_related("batch__product")
            .get(pk=reservation.pk)
        )
        if reservation.organization_id != organization.id:
            raise ValidationError("Reservation is outside the organization scope.")
        if reservation.status != ReservationStatus.ACTIVE:
            raise ValidationError("Only active reservations can be committed.")
        if reservation.is_expired:
            batch = MedicationBatch.objects.select_for_update().get(
                pk=reservation.batch_id
            )
            batch.quantity_reserved = max(
                batch.quantity_reserved - reservation.quantity, Decimal("0")
            )
            batch.save(update_fields=["quantity_reserved", "updated_at"])
            reservation.status = ReservationStatus.EXPIRED
            reservation.save(update_fields=["status", "updated_at"])
            expired = True
        else:
            expired = False

        if expired:
            # The atomic block commits before this exception is raised.
            pass
        else:
            batch = MedicationBatch.objects.select_for_update().get(
                pk=reservation.batch_id
            )
            if batch.quantity_available < reservation.quantity:
                raise ValidationError("Reserved stock is no longer available.")
            batch.quantity_available -= reservation.quantity
            batch.quantity_reserved = max(
                batch.quantity_reserved - reservation.quantity, Decimal("0")
            )
            batch.save(
                update_fields=["quantity_available", "quantity_reserved", "updated_at"]
            )
            reservation.status = ReservationStatus.COMMITTED
            reservation.save(update_fields=["status", "updated_at"])
            enqueue_event(
                organization=organization,
                event_type="pharmacy.reservation_committed",
                aggregate_type="InventoryReservation",
                aggregate_id=reservation.id,
                payload={
                    "reservation_id": str(reservation.id),
                    "batch_id": str(batch.id),
                    "quantity": str(reservation.quantity),
                },
            )
            return reservation

    raise ValidationError("Reservation has expired.")

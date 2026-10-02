from django.db import models
from django.utils import timezone

from apps.core.models import BaseModel
from apps.pharmacy.constants import ReservationStatus
from apps.pharmacy.models.batch import MedicationBatch


class InventoryReservation(BaseModel):
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="pharmacy_inventory_reservations",
    )
    batch = models.ForeignKey(
        MedicationBatch, on_delete=models.PROTECT, related_name="inventory_reservations"
    )
    reservation_number = models.CharField(max_length=80)
    quantity = models.DecimalField(max_digits=14, decimal_places=3)
    status = models.CharField(
        max_length=20,
        choices=ReservationStatus.choices,
        default=ReservationStatus.ACTIVE,
    )
    reference_type = models.CharField(max_length=50, blank=True)
    reference_id = models.UUIDField(null=True, blank=True)
    reserved_by_id = models.UUIDField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "pharmacy_inventory_reservations"
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "reservation_number"),
                name="unique_pharmacy_reservation_number",
            ),
        ]
        indexes = [
            models.Index(fields=("organization", "status")),
            models.Index(fields=("batch", "status")),
            models.Index(fields=("expires_at", "status")),
        ]

    @property
    def is_expired(self):
        return bool(self.expires_at and self.expires_at <= timezone.now())

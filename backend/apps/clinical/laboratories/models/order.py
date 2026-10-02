from decimal import Decimal

from django.db import models

from apps.clinical.appointments.models import Appointment
from apps.clinical.providers.models import Provider
from apps.core.models import BaseManager, BaseModel
from apps.patient_management.patients.models import Patient
from apps.platform.organizations.models import Organization

from .laboratory import Laboratory
from .test import LaboratoryTest


class LaboratoryOrder(BaseModel):
    objects = BaseManager()
    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, related_name="laboratory_orders"
    )
    patient = models.ForeignKey(
        Patient, on_delete=models.PROTECT, related_name="laboratory_orders"
    )
    laboratory = models.ForeignKey(
        Laboratory, on_delete=models.PROTECT, related_name="orders"
    )
    appointment = models.ForeignKey(
        Appointment,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="laboratory_orders",
    )
    encounter = models.ForeignKey(
        "encounters.Encounter",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="laboratory_orders",
    )
    ordering_provider = models.ForeignKey(
        Provider,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="laboratory_orders",
    )
    order_number = models.CharField(max_length=64, unique=True)
    status = models.CharField(max_length=30, default="ordered")
    priority = models.CharField(max_length=30, default="routine")
    clinical_indication = models.TextField(blank=True)
    ordered_at = models.DateTimeField(auto_now_add=True)


class LaboratoryOrderItem(BaseModel):
    objects = BaseManager()
    order = models.ForeignKey(
        LaboratoryOrder, on_delete=models.CASCADE, related_name="items"
    )
    test = models.ForeignKey(
        LaboratoryTest, on_delete=models.PROTECT, related_name="order_items"
    )
    status = models.CharField(max_length=30, default="ordered")
    price = models.DecimalField(
        max_digits=14, decimal_places=2, default=Decimal("0.00")
    )
    instructions = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=("order", "test"), name="uq_lab_order_test")
        ]


# Legacy compatibility: existing rows may predate tenant linkage. New writes are service-enforced.

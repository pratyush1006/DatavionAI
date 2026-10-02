from datetime import timedelta

from django.db import models
from django.utils import timezone

from apps.pharmacy.models import MedicationBatch, PharmacyProduct


def available_batches(*, pharmacy_id):
    return MedicationBatch.objects.filter(
        product__pharmacy_id=pharmacy_id,
        product__is_active=True,
        quantity_available__gt=0,
        expiry_date__gte=timezone.localdate(),
        is_active=True,
    ).order_by("expiry_date", "created_at")


def low_stock_products(*, pharmacy_id):
    from django.db.models import Sum

    return (
        PharmacyProduct.objects.filter(pharmacy_id=pharmacy_id, is_active=True)
        .annotate(stock=Sum("batches__quantity_available"))
        .filter(stock__lt=models.F("reorder_level"))
    )


def expiring_batches(*, pharmacy_id, days=30):
    end = timezone.localdate() + timedelta(days=days)
    return MedicationBatch.objects.filter(
        product__pharmacy_id=pharmacy_id,
        expiry_date__range=(timezone.localdate(), end),
        quantity_available__gt=0,
        is_active=True,
    ).order_by("expiry_date")

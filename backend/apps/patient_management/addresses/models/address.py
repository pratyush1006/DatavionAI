"""Canonical Patient Address aggregate."""

from __future__ import annotations

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.core.models import BaseModel
from apps.patient_management.addresses.constants import (
    AddressSource,
    AddressStatus,
    AddressType,
    AddressUse,
)
from apps.patient_management.addresses.managers import AddressManager


class Address(BaseModel):
    """Tenant-scoped address; geography identity belongs to Platform Geography."""

    tenant = models.ForeignKey(
        "tenancy.Tenant", on_delete=models.PROTECT, related_name="patient_addresses"
    )
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="patient_addresses",
    )
    patient = models.ForeignKey(
        "patient_core.Patient",
        on_delete=models.CASCADE,
        related_name="addresses",
        null=True,
        blank=True,
    )

    address_type = models.CharField(
        max_length=20, choices=AddressType.choices, default=AddressType.HOME
    )
    address_use = models.CharField(
        max_length=20, choices=AddressUse.choices, default=AddressUse.PRIMARY
    )
    status = models.CharField(
        max_length=20, choices=AddressStatus.choices, default=AddressStatus.UNVERIFIED
    )
    source = models.CharField(
        max_length=20, choices=AddressSource.choices, default=AddressSource.PATIENT
    )

    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True)
    landmark = models.CharField(max_length=255, blank=True)
    district = models.CharField(max_length=150, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)

    country = models.ForeignKey(
        "geography.Country",
        on_delete=models.PROTECT,
        related_name="patient_addresses",
        null=True,
        blank=True,
    )
    region = models.ForeignKey(
        "geography.AdministrativeRegion",
        on_delete=models.PROTECT,
        related_name="patient_addresses",
        null=True,
        blank=True,
    )
    city = models.ForeignKey(
        "geography.City",
        on_delete=models.PROTECT,
        related_name="patient_addresses",
        null=True,
        blank=True,
    )

    city_name = models.CharField(max_length=150, blank=True)
    region_name = models.CharField(max_length=150, blank=True)
    country_name = models.CharField(max_length=150, blank=True)
    country_code = models.CharField(max_length=3, blank=True)
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
    )
    formatted_address = models.TextField(blank=True)
    geocoding_place_id = models.CharField(max_length=255, blank=True)
    geocoding_raw = models.JSONField(default=dict, blank=True)
    geocoded_at = models.DateTimeField(null=True, blank=True)

    is_primary = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    verification_notes = models.TextField(blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verified_patient_addresses",
    )

    objects = AddressManager()

    class Meta:
        app_label = "patient_management"
        db_table = "patient_management_address"
        ordering = ("-is_primary", "-created_at")
        indexes = [
            models.Index(
                fields=("tenant", "organization"), name="paddr_tenant_org_idx"
            ),
            models.Index(
                fields=("organization", "patient"), name="paddr_org_patient_idx"
            ),
            models.Index(
                fields=("organization", "status"), name="paddr_org_status_idx"
            ),
            models.Index(fields=("postal_code",), name="paddr_postal_idx"),
            models.Index(fields=("latitude", "longitude"), name="paddr_geo_idx"),
        ]

    def clean(self):
        super().clean()
        if (
            self.organization_id
            and self.tenant_id
            and self.organization.tenant_id != self.tenant_id
        ):
            raise ValidationError({"tenant": "Tenant must match organization tenant."})
        if (
            self.patient_id
            and self.organization_id
            and self.patient.organization_id != self.organization_id
        ):
            raise ValidationError({"patient": "Patient must belong to organization."})
        if (self.latitude is None) != (self.longitude is None):
            raise ValidationError("Latitude and longitude must be supplied together.")

    @property
    def coordinates(self):
        return (
            None
            if self.latitude is None or self.longitude is None
            else (float(self.latitude), float(self.longitude))
        )

    @property
    def full_address(self):
        parts = (
            self.address_line_1,
            self.address_line_2,
            self.landmark,
            self.city_name,
            self.district,
            self.region_name,
            self.postal_code,
            self.country_name,
        )
        return ", ".join(x.strip() for x in parts if x and x.strip())

    def __str__(self):
        return self.formatted_address or self.full_address or self.address_line_1

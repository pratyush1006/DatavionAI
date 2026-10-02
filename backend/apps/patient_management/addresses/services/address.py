"""Transactional Patient Address services."""

from __future__ import annotations

from django.db import transaction
from django.utils import timezone

from apps.patient_management.addresses.constants import AddressSource, AddressStatus
from apps.patient_management.addresses.exceptions import (
    AddressGeographyError,
    AddressScopeError,
)
from apps.patient_management.addresses.models import Address
from apps.patient_management.addresses.services.geography import reverse_geocode


def _scope(tenant, organization):
    if organization.tenant_id != tenant.id:
        raise AddressScopeError("Organization does not belong to tenant.")


def _patient_scope(patient, organization):
    if patient is not None and patient.organization_id != organization.id:
        raise AddressScopeError("Patient does not belong to organization.")


def _payload(result):
    if isinstance(result, dict):
        return result
    data = getattr(result, "__dict__", None)
    if isinstance(data, dict):
        return data
    raise AddressGeographyError(
        "Platform Geography returned an unsupported reverse-geocoding result."
    )


def _resolve_geography(data):
    """Resolve reverse-geocoding names/codes to canonical Geography records."""
    from apps.platform.geography.models import AdministrativeRegion, City, Country

    country_code = str(data.get("country_code") or "").strip().upper()
    country_name = str(data.get("country") or data.get("country_name") or "").strip()
    region_name = str(
        data.get("region") or data.get("state") or data.get("region_name") or ""
    ).strip()
    city_name = str(data.get("city") or data.get("city_name") or "").strip()

    country = None
    if country_code:
        country = Country.objects.filter(code__iexact=country_code).first()
    if country is None and country_name:
        country = Country.objects.filter(name__iexact=country_name).first()

    region = None
    if country is not None and region_name:
        region = AdministrativeRegion.objects.filter(
            country=country,
            name__iexact=region_name,
        ).first()

    city = None
    if country is not None and city_name:
        city_qs = City.objects.filter(country=country, name__iexact=city_name)
        if region is not None:
            city = city_qs.filter(region=region).first()
        if city is None:
            city = city_qs.first()

    return country, region, city


class AddressService:
    @staticmethod
    @transaction.atomic
    def create(*, tenant, organization, patient=None, **data):
        _scope(tenant, organization)
        _patient_scope(patient, organization)
        for key in ("tenant", "organization", "patient"):
            data.pop(key, None)
        obj = Address(tenant=tenant, organization=organization, patient=patient, **data)
        obj.full_clean()
        obj.save()
        if obj.is_primary and obj.patient_id:
            AddressService.set_primary(obj)
        return obj

    @staticmethod
    @transaction.atomic
    def update(obj, *, tenant, organization, **data):
        _scope(tenant, organization)
        if obj.tenant_id != tenant.id or obj.organization_id != organization.id:
            raise AddressScopeError("Address is outside the supplied scope.")
        patient = data.get("patient", obj.patient)
        _patient_scope(patient, organization)
        data.pop("tenant", None)
        data.pop("organization", None)
        for key, value in data.items():
            setattr(obj, key, value)
        obj.full_clean()
        obj.save()
        if obj.is_primary and obj.patient_id:
            AddressService.set_primary(obj)
        return obj

    @staticmethod
    @transaction.atomic
    def delete(obj):
        obj.status = AddressStatus.INACTIVE
        obj.save(update_fields=("status", "updated_at"))
        return obj

    @staticmethod
    @transaction.atomic
    def set_primary(obj):
        if obj.patient_id:
            Address.objects.filter(
                tenant=obj.tenant,
                organization=obj.organization,
                patient=obj.patient,
                is_primary=True,
            ).exclude(pk=obj.pk).update(
                is_primary=False,
                updated_at=timezone.now(),
            )
        obj.is_primary = True
        obj.save(update_fields=("is_primary", "updated_at"))
        return obj

    @staticmethod
    @transaction.atomic
    def verify(obj, *, actor=None, notes=""):
        obj.status = AddressStatus.VERIFIED
        obj.is_verified = True
        obj.verification_notes = notes
        obj.verified_at = timezone.now()
        obj.verified_by = actor
        obj.save(
            update_fields=(
                "status",
                "is_verified",
                "verification_notes",
                "verified_at",
                "verified_by",
                "updated_at",
            )
        )
        return obj

    @staticmethod
    @transaction.atomic
    def reverse_geocode(obj):
        if obj.latitude is None or obj.longitude is None:
            raise ValueError("Latitude and longitude are required.")

        result = _payload(
            reverse_geocode(
                latitude=float(obj.latitude),
                longitude=float(obj.longitude),
            )
        )

        obj.formatted_address = (
            result.get("formatted_address")
            or result.get("display_name")
            or obj.formatted_address
        )
        obj.city_name = result.get("city") or result.get("city_name") or obj.city_name
        obj.region_name = (
            result.get("region")
            or result.get("state")
            or result.get("region_name")
            or obj.region_name
        )
        obj.country_name = (
            result.get("country") or result.get("country_name") or obj.country_name
        )
        obj.country_code = str(
            result.get("country_code") or obj.country_code or ""
        ).upper()
        obj.district = result.get("district") or result.get("county") or obj.district
        obj.postal_code = (
            result.get("postal_code") or result.get("postcode") or obj.postal_code
        )
        obj.geocoding_place_id = str(
            result.get("place_id") or obj.geocoding_place_id or ""
        )
        obj.geocoding_raw = result

        country, region, city = _resolve_geography(result)
        if country is not None:
            obj.country = country
        if region is not None:
            obj.region = region
        if city is not None:
            obj.city = city

        obj.geocoded_at = timezone.now()
        obj.source = AddressSource.GEOGRAPHY
        obj.status = AddressStatus.VERIFIED
        obj.is_verified = True
        obj.save()
        return obj

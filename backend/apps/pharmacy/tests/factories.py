from __future__ import annotations

from datetime import timedelta
from decimal import Decimal
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


def _value_for_field(field, label):
    if field.has_default() or field.null:
        return None
    if isinstance(field, models.UUIDField):
        return uuid4()
    if isinstance(field, models.BooleanField):
        return False
    if isinstance(field, (models.DateTimeField,)):
        return timezone.now()
    if isinstance(field, models.DateField):
        return timezone.localdate()
    if isinstance(field, models.DecimalField):
        return Decimal("0")
    if isinstance(field, models.IntegerField):
        return 1
    if isinstance(field, models.FloatField):
        return 1.0
    if isinstance(field, models.EmailField):
        return f"{uuid4().hex[:10]}@example.test"
    if isinstance(field, models.TextField):
        return f"{label} test"
    if isinstance(field, models.CharField):
        value = f"{label}-{uuid4().hex[:8]}"
        return value[: field.max_length] if field.max_length else value
    if isinstance(field, models.ForeignKey):
        return _create_minimal(field.remote_field.model, label + " related")
    return None


def _create_minimal(model, label="Pharmacy Test"):
    fields = {}
    model_name = model._meta.label_lower

    if model_name == "medications.medication":
        from apps.clinical.medications.constants import (
            MedicationDosageForm,
            MedicationRoute,
        )

        fields["dosage_form"] = MedicationDosageForm.TABLET
        fields["route"] = MedicationRoute.ORAL

    # Appointment has a database invariant requiring scheduled_end >
    # scheduled_start. Generic field generation otherwise assigns timezone.now()
    # to both fields and violates that contract.
    if model_name == "appointments.appointment":
        now = timezone.now()
        field_names = {field.name for field in model._meta.concrete_fields}
        if "scheduled_start" in field_names:
            fields["scheduled_start"] = now
        if "scheduled_end" in field_names:
            fields["scheduled_end"] = now + timedelta(minutes=30)
        if "duration_minutes" in field_names:
            fields["duration_minutes"] = 30

    for field in model._meta.concrete_fields:
        if field.primary_key or field.auto_created or field.has_default() or field.null:
            continue
        if field.name in fields:
            continue
        if isinstance(field, models.ForeignKey):
            related = _create_minimal(field.remote_field.model, label + " related")
            fields[field.name] = related
            continue
        value = _value_for_field(field, label)
        if value is not None:
            fields[field.name] = value
    try:
        return model.objects.create(**fields)
    except Exception:
        # Retry with the smallest safe set. This deliberately surfaces the
        # original model contract instead of weakening production models.
        minimal = {}
        for field in model._meta.concrete_fields:
            if (
                field.primary_key
                or field.auto_created
                or field.has_default()
                or field.null
            ):
                continue
            if isinstance(field, models.ForeignKey):
                minimal[field.name] = _create_minimal(
                    field.remote_field.model, label + " related"
                )
            else:
                value = _value_for_field(field, label)
                if value is not None:
                    minimal[field.name] = value
        return model.objects.create(**minimal)


def create_organization(label="Pharmacy Test Org"):
    from django.apps import apps as django_apps

    Organization = django_apps.get_model("organizations", "Organization")
    tenant_field = (
        Organization._meta.get_field("tenant")
        if any(f.name == "tenant" for f in Organization._meta.concrete_fields)
        else None
    )
    kwargs = (
        {"name": label}
        if any(f.name == "name" for f in Organization._meta.concrete_fields)
        else {}
    )
    if tenant_field is not None and not tenant_field.null:
        kwargs["tenant"] = _create_minimal(
            tenant_field.remote_field.model, "Pharmacy Tenant"
        )
    elif any(f.name == "tenant_id" for f in Organization._meta.concrete_fields):
        raw = Organization._meta.get_field("tenant_id")
        if isinstance(raw, models.UUIDField):
            kwargs["tenant_id"] = uuid4()
    return Organization.objects.create(**kwargs)


def create_user(organization=None):
    User = get_user_model()
    fields = {f.name for f in User._meta.concrete_fields}
    data = {}
    for name in ("username", "email", "first_name", "last_name"):
        if name in fields:
            data[name] = {
                "username": "pharmacy-test",
                "email": f"pharmacy-{uuid4().hex[:8]}@example.test",
                "first_name": "Pharmacy",
                "last_name": "Tester",
            }[name]
    for name in ("is_active", "is_staff", "is_superuser"):
        if name in fields:
            data[name] = name == "is_active"
    if "password" in fields:
        data["password"] = "unused"
    if organization is not None:
        for name in ("organization", "organization_id"):
            if name in fields:
                data[name] = organization if name == "organization" else organization.id
        tenant_id = getattr(organization, "tenant_id", None)
        if tenant_id is not None and "tenant_id" in fields:
            data["tenant_id"] = tenant_id
    for field in User._meta.concrete_fields:
        if (
            field.primary_key
            or field.auto_created
            or field.has_default()
            or field.null
            or field.name in data
        ):
            continue
        value = _value_for_field(field, "Pharmacy User")
        if value is not None:
            data[field.name] = value
    user = User.objects.create(**data)
    if hasattr(user, "set_password"):
        user.set_password("PharmacyTest123!")
        user.save(update_fields=["password"])
    return user


def create_medication(organization):
    from django.apps import apps as django_apps

    from apps.clinical.medications.constants import (
        MedicationDosageForm,
        MedicationRoute,
    )

    Medication = django_apps.get_model("medications", "Medication")
    fields = {f.name for f in Medication._meta.concrete_fields}
    data = {}
    values = {
        "organization": organization,
        "organization_id": organization.id,
        "medication_code": f"MED-{uuid4().hex[:10].upper()}",
        "generic_name": "Amoxicillin",
        "strength": "500",
        "strength_unit": "mg",
        "dosage_form": MedicationDosageForm.TABLET,
        "route": MedicationRoute.ORAL,
        "title": "Amoxicillin 500 mg",
        "name": "Amoxicillin",
    }
    for key, value in values.items():
        if key in fields:
            data[key] = value
    for field in Medication._meta.concrete_fields:
        if (
            field.primary_key
            or field.auto_created
            or field.has_default()
            or field.null
            or field.name in data
        ):
            continue
        value = _value_for_field(field, "Medication")
        if value is not None:
            data[field.name] = value
    return Medication.objects.create(**data)


def create_pharmacy(organization):
    from apps.pharmacy.models import Pharmacy

    return Pharmacy.objects.create(
        organization=organization,
        code=f"TEST-{uuid4().hex[:8].upper()}",
        name="Test Pharmacy",
    )


def create_prescription(organization):
    from django.apps import apps as django_apps

    Prescription = django_apps.get_model("prescriptions", "Prescription")
    fields = {f.name for f in Prescription._meta.concrete_fields}
    data = {}
    if "organization" in fields:
        data["organization"] = organization
    elif "organization_id" in fields:
        data["organization_id"] = organization.id
    for field in Prescription._meta.concrete_fields:
        if (
            field.primary_key
            or field.auto_created
            or field.has_default()
            or field.null
            or field.name in data
        ):
            continue
        if isinstance(field, models.ForeignKey):
            data[field.name] = _create_minimal(field.remote_field.model, "Prescription")
        else:
            value = _value_for_field(field, "Prescription")
            if value is not None:
                data[field.name] = value
    return Prescription.objects.create(**data)

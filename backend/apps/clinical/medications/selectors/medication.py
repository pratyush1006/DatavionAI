from __future__ import annotations

from uuid import UUID

from django.core.exceptions import ValidationError

from apps.clinical.medications.models import Medication


def medication_queryset(*, organization, include_deleted=False):
    queryset = Medication.objects.filter(organization_id=organization.id)
    if not include_deleted:
        queryset = queryset.filter(is_deleted=False)
    return queryset.order_by("generic_name", "brand_name", "strength")


def get_medication(*, organization, medication_id: UUID, include_deleted=False):
    queryset = medication_queryset(
        organization=organization,
        include_deleted=include_deleted,
    )
    try:
        return queryset.get(pk=medication_id)
    except Medication.DoesNotExist as exc:
        raise ValidationError(
            "Medication was not found in the organization scope."
        ) from exc


def search_medications(*, organization, query="", include_deleted=False):
    queryset = medication_queryset(
        organization=organization,
        include_deleted=include_deleted,
    )
    query = str(query or "").strip()
    if query:
        from django.db.models import Q

        queryset = queryset.filter(
            Q(medication_code__icontains=query)
            | Q(generic_name__icontains=query)
            | Q(brand_name__icontains=query)
            | Q(manufacturer__icontains=query)
        )
    return queryset

from __future__ import annotations

"""Documents-backed storage boundary for RCM billing."""

from dataclasses import dataclass
from typing import Any

from django.apps import apps
from django.core.exceptions import ImproperlyConfigured
from django.db import transaction


@dataclass(frozen=True)
class BillingDocumentReference:
    document_id: str
    organization_id: str | None
    metadata: dict[str, Any]


def _document_model():
    try:
        return apps.get_model("documents", "Document")
    except LookupError as exc:
        raise ImproperlyConfigured(
            "RCM billing requires the canonical apps.documents Document model"
        ) from exc


def _supported_fields(model) -> set[str]:
    return {
        field.name
        for field in model._meta.get_fields()
        if getattr(field, "concrete", False)
    }


def store_billing_document(
    *,
    organization=None,
    uploaded_file=None,
    title: str | None = None,
    metadata: dict[str, Any] | None = None,
    actor=None,
    **extra,
) -> BillingDocumentReference:
    """Store a billing document through the canonical Documents domain."""
    model = _document_model()
    fields = _supported_fields(model)
    payload: dict[str, Any] = {}
    organization_id = getattr(organization, "pk", organization)
    if "organization" in fields and organization is not None:
        payload["organization"] = organization
    elif "organization_id" in fields and organization_id is not None:
        payload["organization_id"] = organization_id
    if title is not None:
        for name in ("title", "name", "filename"):
            if name in fields:
                payload[name] = title
                break
    for name in ("file", "document", "attachment"):
        if uploaded_file is not None and name in fields:
            payload[name] = uploaded_file
            break
    for name in ("metadata", "extra_data", "properties"):
        if name in fields:
            payload[name] = metadata or {}
            break
    for name in ("created_by", "uploaded_by", "actor"):
        if actor is not None and name in fields:
            payload[name] = actor
            break
    for key, value in extra.items():
        if key in fields:
            payload[key] = value
    if uploaded_file is not None and not any(
        k in payload for k in ("file", "document", "attachment")
    ):
        raise ImproperlyConfigured(
            "Canonical Documents model has no supported file field; billing cannot bypass Documents storage"
        )
    with transaction.atomic():
        instance = model.objects.create(**payload)
    return BillingDocumentReference(
        document_id=str(instance.pk),
        organization_id=str(organization_id) if organization_id is not None else None,
        metadata=metadata or {},
    )


def get_billing_document(document_id, *, organization=None):
    model = _document_model()
    queryset = model.objects.filter(pk=document_id)
    if organization is not None:
        if hasattr(model, "organization_id"):
            queryset = queryset.filter(
                organization_id=getattr(organization, "pk", organization)
            )
        elif hasattr(model, "organization"):
            queryset = queryset.filter(organization=organization)
    return queryset.first()

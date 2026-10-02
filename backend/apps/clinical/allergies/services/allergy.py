"""
Allergy services.
"""

from __future__ import annotations

from apps.clinical.allergies.models import Allergy


def create_allergy(
    organization=None,
    patient=None,
    provider=None,
    encounter=None,
    *,
    actor=None,
    performed_by=None,
    data=None,
    validated_data=None,
    **kwargs,
):
    """Create an Allergy using the canonical service contract."""
    # Relationship fields may arrive inside serializer validated_data.
    # Preserve them; explicit keyword arguments take precedence.
    payload = dict(validated_data or data or kwargs)
    if organization is not None:
        payload["organization"] = organization
    if patient is not None:
        payload["patient"] = patient
    if provider is not None:
        payload["provider"] = provider
    if encounter is not None:
        payload["encounter"] = encounter
    payload.pop("actor", None)
    payload.pop("performed_by", None)
    return Allergy.objects.create(**payload)


def update_allergy(
    instance=None,
    *,
    allergy=None,
    organization=None,
    actor=None,
    performed_by=None,
    data=None,
    validated_data=None,
    **kwargs,
):
    """Update an Allergy using the canonical service contract."""
    obj = instance or allergy
    if obj is None:
        raise ValueError("Allergy instance is required for update.")
    if organization is not None and getattr(obj, "organization_id", None) != getattr(
        organization, "id", None
    ):
        raise ValueError("Allergy does not belong to the organization.")
    payload = dict(validated_data or data or kwargs)
    for field in ("organization", "patient", "provider", "encounter"):
        payload.pop(field, None)
    allowed = {
        field.name
        for field in obj._meta.concrete_fields
        if field.name not in {"id", "organization", "patient", "provider", "encounter"}
    }
    for field, value in payload.items():
        if field in allowed:
            setattr(obj, field, value)
    obj.save()
    return obj


def delete_allergy(
    instance=None,
    *,
    allergy=None,
    organization=None,
    actor=None,
    performed_by=None,
    user=None,
    **kwargs,
):
    """Soft-delete an Allergy through the bounded-context service boundary."""
    obj = instance or allergy
    if obj is None:
        raise ValueError("Allergy instance is required for deletion.")
    if organization is not None and getattr(obj, "organization_id", None) != getattr(
        organization, "id", None
    ):
        raise ValueError("Allergy does not belong to the organization.")
    resolved_actor = actor or performed_by or user
    delete_method = getattr(obj, "delete", None)
    if not callable(delete_method):
        raise RuntimeError("Allergy model does not expose a delete operation.")
    user_id = (
        getattr(resolved_actor, "id", None) if resolved_actor is not None else None
    )
    try:
        delete_method(user_id=user_id)
    except TypeError:
        delete_method()
    return obj


__all__ = [
    "create_allergy",
    "delete_allergy",
    "update_allergy",
]

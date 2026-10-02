from django.db import transaction
from django.utils import timezone

from apps.insurance.exceptions import InsuranceValidationError
from apps.insurance.models import Enrollment, PlanProduct
from apps.insurance.selectors import get


def create(*, model, organization, data):
    clean = dict(data)
    if any(field.name == "organization" for field in model._meta.fields):
        clean["organization"] = organization
    if (
        model is Enrollment
        and clean.get("product") is not None
        and clean["product"].plan_id != clean["plan"].id
    ):
        raise InsuranceValidationError(
            "Enrollment product must belong to enrollment plan."
        )
    if model is PlanProduct and clean["plan"].organization_id != organization.id:
        raise InsuranceValidationError("Plan product belongs to another organization.")
    with transaction.atomic():
        return model.objects.create(**clean)


def update(*, model, object_id, organization, data):
    obj = get(model, object_id, organization.id)
    for key, value in data.items():
        setattr(obj, key, value)
    obj.save()
    return obj


def soft_delete(*, model, object_id, organization, actor):
    obj = get(model, object_id, organization.id)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.deleted_by_id = getattr(actor, "pk", None)
    obj.save(update_fields=["is_deleted", "deleted_at", "deleted_by_id"])
    return obj


def restore(*, model, object_id, organization):
    obj = get(model, object_id, organization.id)
    obj.is_deleted = False
    obj.deleted_at = None
    obj.deleted_by_id = None
    obj.save(update_fields=["is_deleted", "deleted_at", "deleted_by_id"])
    return obj


def resolve_route(*, enrollment, service):
    payer = enrollment.plan.payer
    relationship = (
        payer.tpa_relationships.filter(
            status="active", effective_date__lte=timezone.localdate()
        )
        .order_by("-effective_date")
        .select_related("tpa")
        .first()
    )
    return {
        "payer": payer,
        "tpa": relationship.tpa if relationship else None,
        "relationship": relationship,
        "service": service,
    }

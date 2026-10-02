"""Organization boundary shared by HR selectors and API permissions."""

from django.db.models import QuerySet

from apps.common.middleware.context import get_current_organization


def organization_lookup(model) -> str:
    fields = {field.name for field in model._meta.fields}
    if "organization" in fields:
        return "organization_id"
    if "employee" in fields:
        return "employee__organization_id"
    if "process" in fields:
        return "process__organization_id"
    if "review" in fields:
        return "review__cycle__organization_id"
    if "cycle" in fields:
        return "cycle__organization_id"
    raise ValueError(f"No HR organization boundary for {model._meta.label}")


def scope_queryset(queryset: QuerySet) -> QuerySet:
    organization = get_current_organization()
    if organization is None:
        return queryset.none()
    return queryset.filter(**{organization_lookup(queryset.model): organization.pk})

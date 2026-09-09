from rest_framework.exceptions import (
    NotAuthenticated,
    PermissionDenied,
    ValidationError,
)


def require_tenant_organization(request):
    tenant = getattr(request, "tenant", None)
    organization = getattr(request, "organization", None)
    if tenant is None or organization is None:
        raise ValidationError("Active tenant and organization context are required.")
    if getattr(organization, "tenant_id", None) != getattr(tenant, "id", tenant):
        raise PermissionDenied("Organization does not belong to the active tenant.")
    if not request.user or not request.user.is_authenticated:
        raise NotAuthenticated()
    return tenant, organization

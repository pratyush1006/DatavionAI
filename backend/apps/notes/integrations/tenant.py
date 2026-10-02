from __future__ import annotations

from apps.platform.organizations.models import Organization


def resolve_tenant(*, organization):
    if organization is None or not getattr(organization, "tenant_id", None):
        raise ValueError("Clinical Notes requires an organization with a tenant.")
    return organization.tenant


def validate_organization_tenant(*, organization_id, tenant_id):
    organization = (
        Organization.objects.filter(pk=organization_id).select_related("tenant").first()
    )
    if organization is None:
        raise ValueError("Organization was not found.")
    if str(organization.tenant_id) != str(tenant_id):
        raise ValueError("Organization does not belong to the supplied tenant.")
    return organization

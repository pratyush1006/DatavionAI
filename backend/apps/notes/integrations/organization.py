from __future__ import annotations

from apps.platform.organizations.models import Organization


def get_organization(*, organization_id):
    organization = (
        Organization.objects.select_related("tenant").filter(pk=organization_id).first()
    )
    if organization is None:
        raise ValueError("Organization was not found.")
    return organization

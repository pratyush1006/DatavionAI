from django.shortcuts import get_object_or_404

from apps.organizations.models import Organization


def get_organizations():
    """
    Return all organizations.
    """
    return (
        Organization.objects
        .order_by("name")
    )


def get_organization_by_id(organization_id):
    """
    Return a single organization.
    """
    return get_object_or_404(
        Organization,
        id=organization_id,
    )
"""
Create serializer for the Organization Domain API.
"""

from __future__ import annotations

from apps.platform.organizations.api.organization_domain.serializers.base import (
    OrganizationDomainBaseSerializer,
)
from apps.platform.organizations.api.organization_domain.serializers.fields import (
    _WRITE_FIELDS,
)


class OrganizationDomainCreateSerializer(
    OrganizationDomainBaseSerializer,
):
    """
    Serializer used when creating an organization domain.
    """

    class Meta(
        OrganizationDomainBaseSerializer.Meta,
    ):
        fields = _WRITE_FIELDS


__all__ = [
    "OrganizationDomainCreateSerializer",
]

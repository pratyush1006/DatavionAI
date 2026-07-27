"""
Detail serializer for the Organization Domain API.
"""

from __future__ import annotations

from apps.platform.organizations.api.organization_domain.serializers.base import (
    OrganizationDomainBaseSerializer,
)
from apps.platform.organizations.api.organization_domain.serializers.fields import (
    _DETAIL_FIELDS,
)


class OrganizationDomainDetailSerializer(
    OrganizationDomainBaseSerializer,
):
    """
    Serializer used for retrieving a single organization domain.
    """

    class Meta(
        OrganizationDomainBaseSerializer.Meta,
    ):
        fields = _DETAIL_FIELDS
        read_only_fields = _DETAIL_FIELDS


__all__ = [
    "OrganizationDomainDetailSerializer",
]

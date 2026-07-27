"""
List serializer for the Organization Domain API.
"""

from __future__ import annotations

from apps.platform.organizations.api.organization_domain.serializers.base import (
    OrganizationDomainBaseSerializer,
)
from apps.platform.organizations.api.organization_domain.serializers.fields import (
    _LIST_FIELDS,
)


class OrganizationDomainListSerializer(
    OrganizationDomainBaseSerializer,
):
    """
    Serializer used for listing organization domains.
    """

    class Meta(
        OrganizationDomainBaseSerializer.Meta,
    ):
        fields = _LIST_FIELDS


__all__ = [
    "OrganizationDomainListSerializer",
]

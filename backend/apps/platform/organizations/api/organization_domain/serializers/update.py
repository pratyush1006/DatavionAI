"""
Update serializer for the Organization Domain API.
"""

from __future__ import annotations

from apps.platform.organizations.api.organization_domain.serializers.base import (
    OrganizationDomainBaseSerializer,
)
from apps.platform.organizations.api.organization_domain.serializers.fields import (
    _UPDATE_FIELDS,
)


class OrganizationDomainUpdateSerializer(
    OrganizationDomainBaseSerializer,
):
    """
    Serializer used when updating an organization domain.

    Business validation and persistence are handled by
    the organization domain service layer.
    """

    class Meta(
        OrganizationDomainBaseSerializer.Meta,
    ):
        fields = _UPDATE_FIELDS


__all__: tuple[str, ...] = ("OrganizationDomainUpdateSerializer",)

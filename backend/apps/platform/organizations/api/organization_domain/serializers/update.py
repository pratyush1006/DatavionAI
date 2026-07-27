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
    """

    class Meta(
        OrganizationDomainBaseSerializer.Meta,
    ):
        fields = _UPDATE_FIELDS

    def validate(
        self,
        attrs,
    ):
        """
        Hook for update-specific validation.
        """

        return super().validate(attrs)


__all__ = [
    "OrganizationDomainUpdateSerializer",
]

"""
Base serializers for the Domain application.
"""

from __future__ import annotations

from apps.common.api.serializers.base import BaseModelSerializer
from apps.platform.organizations.models import OrganizationDomain


class OrganizationDomainBaseSerializer(
    BaseModelSerializer,
):
    """
    Base serializer for Domain serializers.
    """

    class Meta:
        model = OrganizationDomain
        fields: tuple[str, ...] = ()


__all__ = [
    "OrganizationDomainBaseSerializer",
]

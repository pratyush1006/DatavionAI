"""
Base serializer for Permission.
"""

from __future__ import annotations

from apps.common.api.serializers import (
    BaseModelSerializer,
)
from apps.platform.rbac.models import (
    Permission,
)

PERMISSION_FIELDS = (
    "id",
    "name",
    "code",
    "module",
    "action",
    "scope",
    "description",
    "display_order",
    "is_system",
    "is_assignable",
    "is_delegable",
    "is_active",
)


class PermissionBaseSerializer(
    BaseModelSerializer,
):
    """
    Base serializer for Permission.
    """

    class Meta:
        model = Permission

        fields = PERMISSION_FIELDS

        read_only_fields = (
            "id",
            "code",
        )

        extra_kwargs = {
            "name": {
                "required": False,
                "allow_blank": True,
            },
            "description": {
                "required": False,
                "allow_blank": True,
            },
            "display_order": {
                "required": False,
            },
            "is_system": {
                "required": False,
            },
            "is_assignable": {
                "required": False,
            },
            "is_delegable": {
                "required": False,
            },
            "is_active": {
                "required": False,
            },
        }


__all__ = [
    "PERMISSION_FIELDS",
    "PermissionBaseSerializer",
]

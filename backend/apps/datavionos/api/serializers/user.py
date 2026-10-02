"""
Bootstrap user serializer.
"""

from __future__ import annotations

from rest_framework import serializers


class BootstrapUserSerializer(
    serializers.Serializer,
):
    """
    User information returned during DatavionOS bootstrap.
    """

    id = serializers.UUIDField()

    email = serializers.EmailField()

    username = serializers.CharField(
        read_only=True,
    )

    first_name = serializers.CharField(
        read_only=True,
    )

    last_name = serializers.CharField(
        read_only=True,
    )

    full_name = serializers.CharField(
        read_only=True,
    )

    # Keep the UI visibility rule aligned with IsPlatformAdmin, which is the
    # backend permission boundary for platform-wide tenancy operations.
    is_platform_admin = serializers.BooleanField(
        source="is_staff",
        read_only=True,
    )


__all__ = ("BootstrapUserSerializer",)

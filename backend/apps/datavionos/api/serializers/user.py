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


__all__ = ("BootstrapUserSerializer",)

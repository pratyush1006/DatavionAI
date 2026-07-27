"""
JWT token response serializer.
"""

from rest_framework import serializers


class TokenResponseSerializer(
    serializers.Serializer,
):
    """
    JWT token response.
    """

    access = serializers.CharField()

    refresh = serializers.CharField()


__all__ = ("TokenResponseSerializer",)

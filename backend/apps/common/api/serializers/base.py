"""
Base serializers used across the Datavion AI platform.
"""

from __future__ import annotations

from rest_framework import serializers


class BaseModelSerializer(
    serializers.ModelSerializer,
):
    """
    Base model serializer for the Datavion AI platform.

    This class serves as the common parent for all ModelSerializer
    implementations and provides a centralized extension point for
    future platform-wide serializer behavior.
    """


__all__ = [
    "BaseModelSerializer",
]

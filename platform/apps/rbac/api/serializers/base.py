"""
Base serializers for the RBAC app.
"""

from __future__ import annotations

from rest_framework import serializers


class RBACSerializer(serializers.ModelSerializer):
    """
    Base serializer for all RBAC serializers.
    """

    class Meta:
        abstract = True

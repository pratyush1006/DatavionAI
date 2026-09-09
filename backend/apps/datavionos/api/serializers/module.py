"""
DatavionOS module serializer.

Serializes canonical DatavionOS ModuleContract instances.
"""

from __future__ import annotations

from rest_framework import serializers


class ModuleContractSerializer(
    serializers.Serializer,
):
    """
    Serializer for the canonical DatavionOS module contract.

    The serializer intentionally mirrors the public runtime fields
    exposed by ModuleContract.

    Business rules such as:

    - module availability
    - tenant eligibility
    - SaaS entitlement
    - RBAC authorization
    - feature authorization

    are resolved before serialization.
    """

    identifier = serializers.CharField(
        read_only=True,
    )

    name = serializers.CharField(
        read_only=True,
    )

    display_name = serializers.CharField(
        read_only=True,
    )

    description = serializers.CharField(
        read_only=True,
    )

    version = serializers.CharField(
        read_only=True,
    )

    category = serializers.CharField(
        read_only=True,
    )

    route = serializers.CharField(
        read_only=True,
    )

    api_prefix = serializers.CharField(
        read_only=True,
    )

    icon = serializers.CharField(
        read_only=True,
    )

    permissions = serializers.ListField(
        child=serializers.CharField(),
        read_only=True,
    )

    enabled = serializers.BooleanField(
        read_only=True,
    )

    system = serializers.BooleanField(
        read_only=True,
    )

    tenant_scoped = serializers.BooleanField(
        read_only=True,
    )

    order = serializers.IntegerField(
        read_only=True,
    )

    tags = serializers.ListField(
        child=serializers.CharField(),
        read_only=True,
    )

    feature_flags = serializers.ListField(
        child=serializers.CharField(),
        read_only=True,
    )


__all__ = ("ModuleContractSerializer",)

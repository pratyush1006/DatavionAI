from __future__ import annotations

from rest_framework import serializers


class OrganizationControlPlaneSnapshotSerializer(serializers.Serializer):
    organization = serializers.DictField()
    subscription = serializers.DictField(allow_null=True)
    modules = serializers.ListField(child=serializers.DictField())
    features = serializers.ListField(child=serializers.DictField())
    can_manage_modules = serializers.BooleanField()
    can_manage_features = serializers.BooleanField()


class OrganizationCapabilityToggleSerializer(serializers.Serializer):
    enabled = serializers.BooleanField()

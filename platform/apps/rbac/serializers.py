from django.contrib.auth.models import Group, Permission
from rest_framework import serializers


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = (
            "id",
            "name",
            "codename",
        )


class RoleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            "id",
            "name",
        )


class RoleDetailSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Group
        fields = (
            "id",
            "name",
            "permissions",
        )


class RoleCreateSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(),
        many=True,
        required=False,
    )

    class Meta:
        model = Group
        fields = (
            "name",
            "permissions",
        )


class RoleUpdateSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(),
        many=True,
        required=False,
    )

    class Meta:
        model = Group
        fields = (
            "name",
            "permissions",
        )
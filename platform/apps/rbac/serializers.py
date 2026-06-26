from django.contrib.auth.models import Group, Permission
from rest_framework import serializers

from apps.accounts.models import User


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


class UserRoleSerializer(serializers.Serializer):
    role_id = serializers.IntegerField()


class UserRoleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            "id",
            "name",
        )


class UserRoleDetailSerializer(serializers.ModelSerializer):
    roles = UserRoleListSerializer(
        source="groups",
        many=True,
        read_only=True,
    )

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "roles",
        )


class PermissionListSerializer(serializers.ModelSerializer):
    app = serializers.CharField(
        source="content_type.app_label",
        read_only=True,
    )

    model = serializers.CharField(
        source="content_type.model",
        read_only=True,
    )

    class Meta:
        model = Permission
        fields = (
            "id",
            "name",
            "codename",
            "app",
            "model",
        )


class RolePermissionSerializer(serializers.Serializer):
    permission_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
    )

from django.contrib.auth import authenticate
from rest_framework import serializers

from apps.accounts.models import User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(
            username=attrs["username"],
            password=attrs["password"],
        )

        if not user:
            raise serializers.ValidationError(
                "Invalid username or password."
            )

        attrs["user"] = user
        return attrs


class LoginResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


class MeSerializer(serializers.ModelSerializer):
    organization = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User

        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "department",
            "designation",
            "organization",
            "roles",
            "is_verified",
            "is_active_employee",
        ]

    def get_organization(self, obj):
        return obj.organization.name if obj.organization else None

    def get_roles(self, obj):
        return list(
            obj.groups.values_list(
                "name",
                flat=True,
            )
        )


class UserListSerializer(serializers.ModelSerializer):
    organization = serializers.CharField(
        source="organization.name",
        read_only=True,
    )

    class Meta:
        model = User

        fields = [
            "id",
            "username",
            "email",
            "organization",
        ]

class UserDetailSerializer(serializers.ModelSerializer):
    organization = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User

        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "department",
            "designation",
            "organization",
            "roles",
            "is_verified",
            "is_active_employee",
        ]

    def get_organization(self, obj):
        return obj.organization.name if obj.organization else None

    def get_roles(self, obj):
        return list(
            obj.groups.values_list(
                "name",
                flat=True,
            )
        )
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
    )

    class Meta:
        model = User

        fields = [
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "phone",
            "department",
            "designation",
            "organization",
        ]

class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        required=False,
        write_only=True,
    )

    class Meta:
        model = User

        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "department",
            "designation",
            "organization",
            "password",
        ]
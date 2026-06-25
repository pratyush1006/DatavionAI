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


class UserSerializer(serializers.ModelSerializer):
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
        if obj.organization:
            return obj.organization.name
        return None

    def get_roles(self, obj):
        return list(
            obj.groups.values_list(
                "name",
                flat=True
            )
        )
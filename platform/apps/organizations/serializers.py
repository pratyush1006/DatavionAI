from rest_framework import serializers

from apps.organizations.models import Organization


class OrganizationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization

        fields = (
            "id",
            "name",
            "code",
            "organization_type",
            "city",
            "country",
            "is_active",
        )


class OrganizationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization

        fields = (
            "id",
            "name",
            "code",
            "organization_type",
            "email",
            "phone",
            "address",
            "city",
            "state",
            "country",
            "is_active",
            "created_at",
            "updated_at",
        )


class OrganizationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization

        fields = (
            "name",
            "code",
            "organization_type",
            "email",
            "phone",
            "address",
            "city",
            "state",
            "country",
            "is_active",
        )


class OrganizationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization

        fields = (
            "name",
            "organization_type",
            "email",
            "phone",
            "address",
            "city",
            "state",
            "country",
            "is_active",
        )

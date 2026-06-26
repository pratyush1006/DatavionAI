from rest_framework import serializers

from apps.departments.models import Department


class DepartmentListSerializer(serializers.ModelSerializer):
    organization = serializers.CharField(
        source="organization.name",
        read_only=True,
    )

    class Meta:
        model = Department

        fields = (
            "id",
            "name",
            "code",
            "organization",
            "is_active",
        )


class DepartmentDetailSerializer(serializers.ModelSerializer):
    organization = serializers.CharField(
        source="organization.name",
        read_only=True,
    )

    organization_id = serializers.IntegerField(
        source="organization.id",
        read_only=True,
    )

    class Meta:
        model = Department

        fields = (
            "id",
            "organization",
            "organization_id",
            "name",
            "code",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        )


class DepartmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department

        fields = (
            "organization",
            "name",
            "code",
            "description",
            "is_active",
        )


class DepartmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department

        fields = (
            "organization",
            "name",
            "code",
            "description",
            "is_active",
        )

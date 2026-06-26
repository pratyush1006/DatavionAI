from rest_framework import serializers

from apps.teams.models import Team


class TeamListSerializer(serializers.ModelSerializer):
    department = serializers.CharField(
        source="department.name",
        read_only=True,
    )

    organization = serializers.CharField(
        source="department.organization.name",
        read_only=True,
    )

    class Meta:
        model = Team

        fields = (
            "id",
            "name",
            "code",
            "department",
            "organization",
            "is_active",
        )


class TeamDetailSerializer(serializers.ModelSerializer):
    department = serializers.CharField(
        source="department.name",
        read_only=True,
    )

    department_id = serializers.IntegerField(
        source="department.id",
        read_only=True,
    )

    organization = serializers.CharField(
        source="department.organization.name",
        read_only=True,
    )

    organization_id = serializers.IntegerField(
        source="department.organization.id",
        read_only=True,
    )

    class Meta:
        model = Team

        fields = (
            "id",
            "organization",
            "organization_id",
            "department",
            "department_id",
            "name",
            "code",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        )


class TeamCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team

        fields = (
            "department",
            "name",
            "code",
            "description",
            "is_active",
        )


class TeamUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team

        fields = (
            "department",
            "name",
            "code",
            "description",
            "is_active",
        )

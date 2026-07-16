from rest_framework import serializers

from .base import EmployeeBaseSerializer
from .fields import DETAIL_FIELDS


class EmployeeDetailSerializer(
    EmployeeBaseSerializer,
):
    organization = serializers.CharField(
        source="organization.name",
        read_only=True,
    )

    organization_id = serializers.IntegerField(
        source="organization.id",
        read_only=True,
    )

    department = serializers.CharField(
        source="department.name",
        read_only=True,
    )

    department_id = serializers.IntegerField(
        source="department.id",
        read_only=True,
    )

    team = serializers.CharField(
        source="team.name",
        read_only=True,
    )

    team_id = serializers.IntegerField(
        source="team.id",
        read_only=True,
    )

    user_id = serializers.IntegerField(
        source="user.id",
        read_only=True,
    )

    manager = serializers.SerializerMethodField()

    manager_id = serializers.IntegerField(
        source="manager.id",
        read_only=True,
    )

    class Meta(EmployeeBaseSerializer.Meta):
        fields = DETAIL_FIELDS
        read_only_fields = DETAIL_FIELDS

    def get_manager(
        self,
        obj,
    ):
        if obj.manager:
            return obj.manager.user.get_full_name()
        return None

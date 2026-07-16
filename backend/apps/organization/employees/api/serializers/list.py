from rest_framework import serializers

from .base import EmployeeBaseSerializer
from .fields import LIST_FIELDS


class EmployeeListSerializer(
    EmployeeBaseSerializer,
):
    organization = serializers.CharField(
        source="organization.name",
        read_only=True,
    )

    department = serializers.CharField(
        source="department.name",
        read_only=True,
    )

    team = serializers.CharField(
        source="team.name",
        read_only=True,
    )

    class Meta(EmployeeBaseSerializer.Meta):
        fields = LIST_FIELDS
        read_only_fields = LIST_FIELDS

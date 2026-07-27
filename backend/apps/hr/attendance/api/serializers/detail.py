from rest_framework import serializers

from .base import AttendanceRecordBaseSerializer
from .fields import DETAIL_FIELDS


class AttendanceRecordDetailSerializer(
    AttendanceRecordBaseSerializer,
):
    organization = serializers.CharField(
        source="organization.name",
        read_only=True,
    )

    organization_id = serializers.IntegerField(
        source="organization.id",
        read_only=True,
    )

    employee = serializers.CharField(
        source="employee.employee_code",
        read_only=True,
    )

    employee_id = serializers.IntegerField(
        source="employee.id",
        read_only=True,
    )

    class Meta(AttendanceRecordBaseSerializer.Meta):
        fields = DETAIL_FIELDS
        read_only_fields = DETAIL_FIELDS

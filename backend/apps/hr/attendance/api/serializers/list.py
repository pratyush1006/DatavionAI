from rest_framework import serializers

from .base import AttendanceRecordBaseSerializer
from .fields import LIST_FIELDS


class AttendanceRecordListSerializer(
    AttendanceRecordBaseSerializer,
):
    employee = serializers.CharField(
        source="employee.employee_code",
        read_only=True,
    )

    class Meta(AttendanceRecordBaseSerializer.Meta):
        fields = LIST_FIELDS
        read_only_fields = LIST_FIELDS

from rest_framework import serializers

from apps.hr.attendance.models import AttendanceRecord


class AttendanceRecordBaseSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()

    class Meta:
        model = AttendanceRecord
        fields: tuple[str, ...] = ()

    def get_employee_name(
        self,
        obj: AttendanceRecord,
    ) -> str:
        return str(obj.employee.full_name)

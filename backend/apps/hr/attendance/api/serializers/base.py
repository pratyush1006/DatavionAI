from rest_framework import serializers

from apps.hr.attendance.models import AttendanceRecord


class AttendanceRecordBaseSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()

    class Meta:
        model = AttendanceRecord
        fields = ()

    def get_employee_name(
        self,
        obj: AttendanceRecord,
    ) -> str:
        return obj.employee.full_name

from django.contrib import admin

from apps.hr.attendance.models import AttendanceRecord


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = (
        "employee",
        "work_date",
        "check_in",
        "check_out",
        "hours_worked",
        "status",
    )

    list_filter = (
        "organization",
        "status",
        "work_date",
    )

    search_fields = (
        "employee__employee_code",
        "employee__user__first_name",
        "employee__user__last_name",
    )

    ordering = ("-work_date",)

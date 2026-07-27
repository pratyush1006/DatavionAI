from django.contrib import admin

from apps.hr.shifts.models import Shift, ShiftAssignment


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "organization",
        "start_time",
        "end_time",
        "is_night_shift",
        "is_active",
    )

    list_filter = ("organization", "is_night_shift", "is_active")

    search_fields = ("name", "code")

    ordering = ("start_time",)


@admin.register(ShiftAssignment)
class ShiftAssignmentAdmin(admin.ModelAdmin):
    list_display = (
        "employee",
        "shift",
        "work_date",
        "status",
    )

    list_filter = ("organization", "shift", "status")

    search_fields = ("employee__employee_code",)

    ordering = ("-work_date",)

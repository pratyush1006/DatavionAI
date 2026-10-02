from django.contrib import admin

from apps.hr.leave.models import LeaveBalance, LeaveRequest, LeaveType


@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "organization",
        "is_paid",
        "requires_approval",
        "is_active",
    )

    list_filter = ("organization", "is_paid", "is_active")

    search_fields = ("name", "code")

    ordering = ("name",)


@admin.register(LeaveBalance)
class LeaveBalanceAdmin(admin.ModelAdmin):
    list_display = (
        "employee",
        "leave_type",
        "year",
        "allocated_days",
        "used_days",
        "remaining_days",
    )

    list_filter = ("leave_type", "year")

    search_fields = ("employee__employee_code",)

    ordering = ("-year",)


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = (
        "employee",
        "leave_type",
        "start_date",
        "end_date",
        "number_of_days",
        "status",
    )

    list_filter = ("organization", "leave_type", "status")

    search_fields = ("employee__employee_code", "reason")

    ordering = ("-start_date",)

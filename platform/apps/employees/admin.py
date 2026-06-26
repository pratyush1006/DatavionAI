from django.contrib import admin

# Register your models here.
from apps.employees.models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "employee_code",
        "user",
        "organization",
        "department",
        "team",
        "designation",
        "is_active",
    )

    list_filter = (
        "organization",
        "department",
        "team",
        "is_active",
    )

    search_fields = (
        "employee_code",
        "user__first_name",
        "user__last_name",
        "user__email",
    )

    ordering = ("employee_code",)

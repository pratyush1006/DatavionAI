# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.accounts.models import User, OrganizationRole


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "organization",
        "is_staff",
        "is_active",
    )

    search_fields = (
        "username",
        "email",
        "employee_id",
    )

    list_filter = (
        "organization",
        "is_staff",
        "is_active",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "Datavion AI",
            {
                "fields": (
                    "organization",
                    "employee_id",
                    "phone",
                    "department",
                    "designation",
                    "is_verified",
                    "is_active_employee",
                )
            },
        ),
    )


@admin.register(OrganizationRole)
class OrganizationRoleAdmin(admin.ModelAdmin):
    list_display = (
        "organization",
        "group",
        "is_active",
    )

    list_filter = (
        "organization",
        "group",
    )
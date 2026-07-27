from django.contrib import admin

from apps.hr.holidays.models import Holiday


@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "organization",
        "date",
        "holiday_type",
        "is_recurring_yearly",
    )

    list_filter = ("organization", "holiday_type", "is_recurring_yearly")

    search_fields = ("name",)

    ordering = ("date",)

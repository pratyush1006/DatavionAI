from django.contrib import admin

from apps.hr.onboarding.models import (
    LifecycleProcess,
    LifecycleTask,
    LifecycleTaskTemplate,
)


class LifecycleTaskInline(admin.TabularInline):
    model = LifecycleTask
    extra = 0


@admin.register(LifecycleTaskTemplate)
class LifecycleTaskTemplateAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "organization",
        "process_type",
        "category",
        "is_mandatory",
        "order",
        "is_active",
    )

    list_filter = ("organization", "process_type", "category", "is_active")

    search_fields = ("title",)

    ordering = ("process_type", "order")


@admin.register(LifecycleProcess)
class LifecycleProcessAdmin(admin.ModelAdmin):
    list_display = (
        "employee",
        "process_type",
        "status",
        "start_date",
        "target_completion_date",
    )

    list_filter = ("organization", "process_type", "status")

    search_fields = ("employee__employee_code",)

    ordering = ("-start_date",)

    inlines = (LifecycleTaskInline,)


@admin.register(LifecycleTask)
class LifecycleTaskAdmin(admin.ModelAdmin):
    list_display = (
        "process",
        "title",
        "category",
        "status",
        "assigned_to",
        "due_date",
    )

    list_filter = ("category", "status")

    search_fields = ("title",)

    ordering = ("order",)

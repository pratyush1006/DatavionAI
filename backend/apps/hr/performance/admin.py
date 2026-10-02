from django.contrib import admin

from apps.hr.performance.models import (
    PerformanceGoal,
    PerformanceReview,
    PerformanceReviewCycle,
)


class PerformanceGoalInline(admin.TabularInline):
    model = PerformanceGoal
    extra = 0


@admin.register(PerformanceReviewCycle)
class PerformanceReviewCycleAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "organization",
        "start_date",
        "end_date",
        "status",
    )

    list_filter = ("organization", "status")

    search_fields = ("name",)

    ordering = ("-start_date",)


@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = (
        "employee",
        "cycle",
        "reviewer",
        "status",
        "overall_rating",
    )

    list_filter = ("cycle", "status")

    search_fields = ("employee__employee_code",)

    ordering = ("-created_at",)

    inlines = (PerformanceGoalInline,)


@admin.register(PerformanceGoal)
class PerformanceGoalAdmin(admin.ModelAdmin):
    list_display = (
        "review",
        "title",
        "weight",
        "status",
        "rating",
        "target_date",
    )

    list_filter = ("status",)

    search_fields = ("title",)

    ordering = ("-target_date",)

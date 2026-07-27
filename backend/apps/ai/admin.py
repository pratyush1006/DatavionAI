"""
Admin configuration for the AI application.
"""

from __future__ import annotations

from django.contrib import admin

from apps.ai.models import AIModel, Prediction, Recommendation


@admin.register(AIModel)
class AIModelAdmin(admin.ModelAdmin):
    """
    Django admin configuration for AIModel.
    """

    list_display = (
        "name",
        "model_type",
        "version",
        "status",
        "organization",
        "accuracy",
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "version",
        "description",
    )

    list_filter = (
        "organization",
        "model_type",
        "status",
        "is_active",
        "created_at",
    )

    ordering = (
        "name",
        "-version",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = ("organization",)

    list_select_related = ("organization",)

    list_per_page = 25

    date_hierarchy = "created_at"

    preserve_filters = True

    empty_value_display = "-"

    fieldsets = (
        (
            "Model Information",
            {
                "fields": (
                    "organization",
                    "name",
                    "model_type",
                    "version",
                    "status",
                ),
            },
        ),
        (
            "Performance",
            {
                "fields": (
                    "accuracy",
                    "description",
                    "metadata",
                ),
            },
        ),
        (
            "Audit Information",
            {
                "fields": (
                    "id",
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    """
    Django admin configuration for Prediction.
    """

    list_display = (
        "prediction_type",
        "risk_level",
        "risk_score",
        "patient",
        "ai_model",
        "organization",
        "is_reviewed",
        "predicted_at",
    )

    search_fields = (
        "prediction_type",
        "risk_level",
        "explanation",
    )

    list_filter = (
        "organization",
        "prediction_type",
        "risk_level",
        "is_reviewed",
        "predicted_at",
    )

    ordering = ("-predicted_at",)

    readonly_fields = (
        "id",
        "predicted_at",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "organization",
        "patient",
        "ai_model",
        "reviewed_by",
    )

    list_select_related = (
        "organization",
        "patient",
        "ai_model",
    )

    list_per_page = 25

    date_hierarchy = "predicted_at"

    preserve_filters = True

    empty_value_display = "-"

    fieldsets = (
        (
            "Prediction Information",
            {
                "fields": (
                    "organization",
                    "patient",
                    "ai_model",
                    "prediction_type",
                    "predicted_at",
                ),
            },
        ),
        (
            "Results",
            {
                "fields": (
                    "risk_score",
                    "risk_level",
                    "result",
                    "explanation",
                ),
            },
        ),
        (
            "Input",
            {
                "fields": ("input_data",),
            },
        ),
        (
            "Review",
            {
                "fields": (
                    "is_reviewed",
                    "reviewed_by",
                    "reviewed_at",
                ),
            },
        ),
        (
            "Audit Information",
            {
                "fields": (
                    "id",
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    """
    Django admin configuration for Recommendation.
    """

    list_display = (
        "title",
        "recommendation_type",
        "status",
        "priority",
        "patient",
        "organization",
        "confidence_score",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
        "source",
    )

    list_filter = (
        "organization",
        "recommendation_type",
        "status",
        "priority",
        "created_at",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "organization",
        "patient",
    )

    list_select_related = (
        "organization",
        "patient",
    )

    list_per_page = 25

    date_hierarchy = "created_at"

    preserve_filters = True

    empty_value_display = "-"

    fieldsets = (
        (
            "Recommendation Information",
            {
                "fields": (
                    "organization",
                    "patient",
                    "recommendation_type",
                    "title",
                    "description",
                ),
            },
        ),
        (
            "Metadata",
            {
                "fields": (
                    "confidence_score",
                    "source",
                    "status",
                    "priority",
                    "expires_at",
                ),
            },
        ),
        (
            "Audit Information",
            {
                "fields": (
                    "id",
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )


__all__ = [
    "AIModelAdmin",
    "PredictionAdmin",
    "RecommendationAdmin",
]

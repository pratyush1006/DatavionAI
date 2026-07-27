"""
Admin configuration for the Imaging application.
"""

from __future__ import annotations

from django.contrib import admin

from apps.imaging.models import AIAnalysis, ImageInstance, Report, Series, Study


@admin.register(Study)
class StudyAdmin(admin.ModelAdmin):
    """
    Django admin configuration for Study.
    """

    list_display = (
        "study_instance_uid",
        "accession_number",
        "patient",
        "organization",
        "study_date",
        "modality",
        "status",
        "created_at",
    )

    search_fields = (
        "study_instance_uid",
        "accession_number",
        "study_description",
        "referring_physician",
    )

    list_filter = (
        "organization",
        "modality",
        "status",
        "study_date",
    )

    ordering = (
        "-study_date",
        "-created_at",
    )

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

    date_hierarchy = "study_date"

    preserve_filters = True

    empty_value_display = "-"

    fieldsets = (
        (
            "Study Information",
            {
                "fields": (
                    "organization",
                    "patient",
                    "study_instance_uid",
                    "accession_number",
                ),
            },
        ),
        (
            "Study Details",
            {
                "fields": (
                    "study_date",
                    "modality",
                    "study_description",
                    "referring_physician",
                ),
            },
        ),
        (
            "Status",
            {
                "fields": ("status",),
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


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    """
    Django admin configuration for Series.
    """

    list_display = (
        "series_instance_uid",
        "study",
        "series_number",
        "modality",
        "number_of_instances",
        "created_at",
    )

    search_fields = (
        "series_instance_uid",
        "series_description",
    )

    list_filter = (
        "modality",
        "created_at",
    )

    ordering = (
        "study",
        "series_number",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = ("study",)

    list_select_related = ("study",)

    list_per_page = 25

    preserve_filters = True

    empty_value_display = "-"


@admin.register(ImageInstance)
class ImageInstanceAdmin(admin.ModelAdmin):
    """
    Django admin configuration for ImageInstance.
    """

    list_display = (
        "sop_instance_uid",
        "series",
        "instance_number",
        "rows",
        "columns",
        "bits_allocated",
        "file_size",
        "created_at",
    )

    search_fields = (
        "sop_instance_uid",
        "storage_path",
        "thumbnail_path",
    )

    list_filter = ("created_at",)

    ordering = (
        "series",
        "instance_number",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = ("series",)

    list_select_related = ("series",)

    list_per_page = 25

    preserve_filters = True

    empty_value_display = "-"


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """
    Django admin configuration for Report.
    """

    list_display = (
        "study",
        "status",
        "reported_by",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "report_text",
        "findings",
        "impression",
        "recommendations",
    )

    list_filter = (
        "status",
        "created_at",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "study",
        "reported_by",
    )

    list_select_related = (
        "study",
        "reported_by",
    )

    list_per_page = 25

    date_hierarchy = "created_at"

    preserve_filters = True

    empty_value_display = "-"

    fieldsets = (
        (
            "Report Information",
            {
                "fields": (
                    "study",
                    "reported_by",
                    "status",
                ),
            },
        ),
        (
            "Report Content",
            {
                "fields": (
                    "report_text",
                    "findings",
                    "impression",
                    "recommendations",
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


@admin.register(AIAnalysis)
class AIAnalysisAdmin(admin.ModelAdmin):
    """
    Django admin configuration for AIAnalysis.
    """

    list_display = (
        "study",
        "ai_model",
        "analysis_type",
        "confidence_score",
        "is_reviewed",
        "reviewed_by",
        "created_at",
    )

    search_fields = (
        "analysis_type",
        "result",
        "findings",
    )

    list_filter = (
        "analysis_type",
        "is_reviewed",
        "created_at",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "study",
        "ai_model",
        "reviewed_by",
    )

    list_select_related = (
        "study",
        "ai_model",
        "reviewed_by",
    )

    list_per_page = 25

    date_hierarchy = "created_at"

    preserve_filters = True

    empty_value_display = "-"


__all__ = [
    "AIAnalysisAdmin",
    "ImageInstanceAdmin",
    "ReportAdmin",
    "SeriesAdmin",
    "StudyAdmin",
]

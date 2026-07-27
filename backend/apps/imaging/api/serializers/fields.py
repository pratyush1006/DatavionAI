"""
Serializer field definitions for the Imaging application.
"""

from __future__ import annotations

from typing import Final

STUDY_LIST_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "study_instance_uid",
    "accession_number",
    "study_date",
    "modality",
    "study_description",
    "referring_physician",
    "status",
    "created_at",
)

STUDY_DETAIL_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "organization",
    "patient",
    "study_instance_uid",
    "accession_number",
    "study_date",
    "modality",
    "study_description",
    "referring_physician",
    "status",
    "created_at",
    "updated_at",
)

STUDY_WRITE_FIELDS: Final[tuple[str, ...]] = (
    "organization",
    "patient",
    "study_instance_uid",
    "accession_number",
    "study_date",
    "modality",
    "study_description",
    "referring_physician",
    "status",
)

STUDY_UPDATE_FIELDS: Final[tuple[str, ...]] = (
    "accession_number",
    "study_date",
    "modality",
    "study_description",
    "referring_physician",
    "status",
)

STUDY_READ_ONLY_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "created_at",
    "updated_at",
)

REPORT_LIST_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "study",
    "status",
    "reported_by",
    "created_at",
)

REPORT_DETAIL_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "study",
    "report_text",
    "findings",
    "impression",
    "recommendations",
    "reported_by",
    "status",
    "created_at",
    "updated_at",
)

REPORT_WRITE_FIELDS: Final[tuple[str, ...]] = (
    "study",
    "report_text",
    "findings",
    "impression",
    "recommendations",
    "reported_by",
    "status",
)

REPORT_UPDATE_FIELDS: Final[tuple[str, ...]] = (
    "report_text",
    "findings",
    "impression",
    "recommendations",
    "reported_by",
    "status",
)

REPORT_READ_ONLY_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "created_at",
    "updated_at",
)

AI_ANALYSIS_LIST_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "study",
    "ai_model",
    "analysis_type",
    "confidence_score",
    "is_reviewed",
    "reviewed_by",
    "created_at",
)

AI_ANALYSIS_DETAIL_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "study",
    "ai_model",
    "analysis_type",
    "input_image_ids",
    "result",
    "confidence_score",
    "findings",
    "is_reviewed",
    "reviewed_by",
    "reviewed_at",
    "created_at",
    "updated_at",
)

AI_ANALYSIS_WRITE_FIELDS: Final[tuple[str, ...]] = (
    "study",
    "ai_model",
    "analysis_type",
    "input_image_ids",
    "result",
    "confidence_score",
    "findings",
)

AI_ANALYSIS_UPDATE_FIELDS: Final[tuple[str, ...]] = (
    "is_reviewed",
    "reviewed_by",
    "reviewed_at",
    "result",
    "confidence_score",
    "findings",
)

AI_ANALYSIS_READ_ONLY_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "created_at",
    "updated_at",
)

LIST_FIELDS = STUDY_LIST_FIELDS
DETAIL_FIELDS = STUDY_DETAIL_FIELDS
WRITE_FIELDS = STUDY_WRITE_FIELDS
UPDATE_FIELDS = STUDY_UPDATE_FIELDS
READ_ONLY_FIELDS = STUDY_READ_ONLY_FIELDS

__all__ = [
    "AI_ANALYSIS_DETAIL_FIELDS",
    "AI_ANALYSIS_LIST_FIELDS",
    "AI_ANALYSIS_READ_ONLY_FIELDS",
    "AI_ANALYSIS_UPDATE_FIELDS",
    "AI_ANALYSIS_WRITE_FIELDS",
    "DETAIL_FIELDS",
    "LIST_FIELDS",
    "READ_ONLY_FIELDS",
    "REPORT_DETAIL_FIELDS",
    "REPORT_LIST_FIELDS",
    "REPORT_READ_ONLY_FIELDS",
    "REPORT_UPDATE_FIELDS",
    "REPORT_WRITE_FIELDS",
    "STUDY_DETAIL_FIELDS",
    "STUDY_LIST_FIELDS",
    "STUDY_READ_ONLY_FIELDS",
    "STUDY_UPDATE_FIELDS",
    "STUDY_WRITE_FIELDS",
    "UPDATE_FIELDS",
    "WRITE_FIELDS",
]

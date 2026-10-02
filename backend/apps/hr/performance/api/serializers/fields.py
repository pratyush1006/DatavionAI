"""
Serializer field definitions for Performance.
"""

from __future__ import annotations

from typing import Final

REVIEW_CYCLE_LIST_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "name",
    "start_date",
    "end_date",
    "status",
)

REVIEW_CYCLE_DETAIL_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "organization",
    "organization_id",
    "name",
    "start_date",
    "end_date",
    "status",
    "created_at",
    "updated_at",
)

REVIEW_CYCLE_WRITE_FIELDS: Final[tuple[str, ...]] = (
    "organization",
    "name",
    "start_date",
    "end_date",
    "status",
)

PERFORMANCE_REVIEW_LIST_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "cycle",
    "employee",
    "employee_name",
    "reviewer",
    "status",
    "overall_rating",
)

PERFORMANCE_REVIEW_DETAIL_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "cycle",
    "cycle_id",
    "employee",
    "employee_id",
    "employee_name",
    "reviewer",
    "reviewer_id",
    "status",
    "overall_rating",
    "strengths",
    "areas_for_improvement",
    "employee_comments",
    "reviewer_comments",
    "submitted_at",
    "goals",
    "created_at",
    "updated_at",
)

PERFORMANCE_REVIEW_WRITE_FIELDS: Final[tuple[str, ...]] = (
    "cycle",
    "employee",
    "reviewer",
    "overall_rating",
    "strengths",
    "areas_for_improvement",
    "reviewer_comments",
    "goals",
)

PERFORMANCE_GOAL_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "review",
    "title",
    "description",
    "weight",
    "target_date",
    "status",
    "rating",
    "created_at",
    "updated_at",
)

PERFORMANCE_GOAL_WRITE_FIELDS: Final[tuple[str, ...]] = (
    "review",
    "title",
    "description",
    "weight",
    "target_date",
    "status",
    "rating",
)

__all__ = [
    "REVIEW_CYCLE_LIST_FIELDS",
    "REVIEW_CYCLE_DETAIL_FIELDS",
    "REVIEW_CYCLE_WRITE_FIELDS",
    "PERFORMANCE_REVIEW_LIST_FIELDS",
    "PERFORMANCE_REVIEW_DETAIL_FIELDS",
    "PERFORMANCE_REVIEW_WRITE_FIELDS",
    "PERFORMANCE_GOAL_FIELDS",
    "PERFORMANCE_GOAL_WRITE_FIELDS",
]

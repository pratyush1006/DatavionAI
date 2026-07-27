"""
Serializer field definitions for Onboarding.
"""

from __future__ import annotations

from typing import Final

TASK_TEMPLATE_LIST_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "process_type",
    "title",
    "category",
    "is_mandatory",
    "order",
    "is_active",
)

TASK_TEMPLATE_DETAIL_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "organization",
    "organization_id",
    "process_type",
    "title",
    "description",
    "category",
    "is_mandatory",
    "order",
    "is_active",
    "created_at",
    "updated_at",
)

TASK_TEMPLATE_WRITE_FIELDS: Final[tuple[str, ...]] = (
    "organization",
    "process_type",
    "title",
    "description",
    "category",
    "is_mandatory",
    "order",
    "is_active",
)

LIFECYCLE_TASK_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "process",
    "title",
    "description",
    "category",
    "is_mandatory",
    "assigned_to",
    "assigned_to_name",
    "status",
    "due_date",
    "completed_at",
    "order",
    "notes",
    "created_at",
    "updated_at",
)

LIFECYCLE_TASK_WRITE_FIELDS: Final[tuple[str, ...]] = (
    "process",
    "title",
    "description",
    "category",
    "is_mandatory",
    "assigned_to",
    "status",
    "due_date",
    "order",
    "notes",
)

LIFECYCLE_PROCESS_LIST_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "employee",
    "employee_name",
    "process_type",
    "status",
    "start_date",
    "target_completion_date",
    "completion_percentage",
)

LIFECYCLE_PROCESS_DETAIL_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "organization",
    "organization_id",
    "employee",
    "employee_id",
    "employee_name",
    "process_type",
    "status",
    "initiated_by",
    "initiated_by_id",
    "start_date",
    "target_completion_date",
    "completed_at",
    "completion_percentage",
    "notes",
    "tasks",
    "created_at",
    "updated_at",
)

LIFECYCLE_PROCESS_WRITE_FIELDS: Final[tuple[str, ...]] = (
    "organization",
    "employee",
    "process_type",
    "initiated_by",
    "start_date",
    "target_completion_date",
    "notes",
)

LIFECYCLE_PROCESS_UPDATE_FIELDS: Final[tuple[str, ...]] = (
    "target_completion_date",
    "notes",
)

__all__ = [
    "TASK_TEMPLATE_LIST_FIELDS",
    "TASK_TEMPLATE_DETAIL_FIELDS",
    "TASK_TEMPLATE_WRITE_FIELDS",
    "LIFECYCLE_TASK_FIELDS",
    "LIFECYCLE_TASK_WRITE_FIELDS",
    "LIFECYCLE_PROCESS_LIST_FIELDS",
    "LIFECYCLE_PROCESS_DETAIL_FIELDS",
    "LIFECYCLE_PROCESS_WRITE_FIELDS",
    "LIFECYCLE_PROCESS_UPDATE_FIELDS",
]

from rest_framework import serializers

from apps.employees.models import Employee

# List of fields for different serializer operations
BASE_FIELDS = (
    "id",
    "employee_code",
    "employee_name",
    "designation",
    "is_active",
    "created_at",
    "updated_at",
)

LIST_FIELDS = BASE_FIELDS + (
    "organization",
    "department",
    "team",
)

DETAIL_FIELDS = LIST_FIELDS + (
    "organization_id",
    "department_id",
    "team_id",
    "user_id",
    "manager",
    "manager_id",
    "hire_date",
)

CREATE_FIELDS = (
    "organization",
    "department",
    "team",
    "user",
    "employee_code",
    "designation",
    "manager",
    "hire_date",
    "is_active",
)

UPDATE_FIELDS = (
    "organization",
    "department",
    "team",
    "designation",
    "manager",
    "hire_date",
    "is_active",
)

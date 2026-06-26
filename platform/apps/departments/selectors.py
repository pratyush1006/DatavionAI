from django.shortcuts import get_object_or_404

from apps.departments.models import Department


def get_departments():
    """
    Return all departments ordered by name.
    """

    return Department.objects.select_related("organization").order_by("name")


def get_department_by_id(
    department_id: int,
) -> Department:
    """
    Return a department by ID.
    """

    return get_object_or_404(
        Department.objects.select_related("organization"),
        id=department_id,
    )

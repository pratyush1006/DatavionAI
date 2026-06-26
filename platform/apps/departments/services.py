from apps.departments.models import Department


def create_department(
    validated_data: dict,
) -> Department:
    """
    Create a new department.
    """

    department = Department.objects.create(
        **validated_data
    )

    return department


def update_department(
    department: Department,
    validated_data: dict,
) -> Department:
    """
    Update an existing department.
    """

    for field, value in validated_data.items():
        setattr(
            department,
            field,
            value,
        )

    department.save()

    return department


def delete_department(
    department: Department,
) -> None:
    """
    Delete a department.
    """

    department.delete()
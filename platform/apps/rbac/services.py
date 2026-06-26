from django.contrib.auth.models import Group


def create_role(validated_data):
    """
    Create a new role.
    """

    permissions = validated_data.pop(
        "permissions",
        [],
    )

    role = Group.objects.create(
        **validated_data
    )

    if permissions:
        role.permissions.set(
            permissions
        )

    return role


def update_role(role, validated_data):
    """
    Update an existing role.
    """

    permissions = validated_data.pop(
        "permissions",
        None,
    )

    for field, value in validated_data.items():
        setattr(
            role,
            field,
            value,
        )

    role.save()

    if permissions is not None:
        role.permissions.set(
            permissions
        )

    return role


def delete_role(role):
    """
    Delete an existing role.
    """

    role.delete()
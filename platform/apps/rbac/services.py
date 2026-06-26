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


# ======================================================
# User Role Management
# ======================================================

def assign_role_to_user(user, role):
    """
    Assign a role to a user.
    """
    user.groups.add(role)
    return user


def remove_role_from_user(user, role):
    """
    Remove a role from a user.
    """
    user.groups.remove(role)
    return user


def get_user_roles(user):
    """
    Return all roles assigned to a user.
    """
    return (
        user.groups
        .all()
        .order_by("name")
    )
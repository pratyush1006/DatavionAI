from apps.insurance.rbac import has_permission


def can_view(*, user, organization):
    return has_permission(
        user=user, permission="insurance.view", organization=organization
    )


def can_manage(*, user, organization):
    return has_permission(
        user=user, permission="insurance.manage", organization=organization
    )


def can_delete(*, user, organization):
    return has_permission(
        user=user, permission="insurance.delete", organization=organization
    )

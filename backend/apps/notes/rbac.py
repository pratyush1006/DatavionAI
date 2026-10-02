from apps.platform.rbac.resolvers import resolve_permissions


def has_permission(*, user, organization, permission: str) -> bool:
    if not user or not getattr(user, "is_authenticated", False) or not organization:
        return False
    return permission in resolve_permissions(user=user, organization=organization)

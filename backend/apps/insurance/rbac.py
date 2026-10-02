from typing import Any

from apps.platform.rbac.resolvers import resolve_permissions


def has_permission(*, user: Any, permission: str, organization: Any) -> bool:
    return permission in resolve_permissions(user=user, organization=organization)

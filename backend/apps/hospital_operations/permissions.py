from rest_framework.permissions import BasePermission

from .constants import RBAC_PERMISSIONS


class HospitalOperationsPermission(BasePermission):
    """Adapter to the canonical platform RBAC permission contract."""

    permission_key = "view"

    def has_permission(self, request, view):
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            return False

        # Platform staff access is already established at the platform RBAC
        # boundary. Do not reject it here merely because these legacy views
        # still consult Django's per-model permission table.
        if user.is_superuser or user.is_staff:
            return True

        key = getattr(view, "rbac_permission", self.permission_key)
        permission = RBAC_PERMISSIONS.get(key)
        return bool(permission and user.has_perm(permission))

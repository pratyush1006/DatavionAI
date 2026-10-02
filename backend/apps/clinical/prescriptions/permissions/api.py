"""DRF permission adapter for prescription endpoints."""

from apps.platform.rbac.permissions.base import RBACPermissionBase


class PrescriptionAPIPermission(RBACPermissionBase):
    """Require explicit prescription RBAC for every endpoint operation."""

    actions = {
        "GET": "view",
        "HEAD": "view",
        "POST": "create",
        "PATCH": "update",
        "PUT": "update",
        "DELETE": "delete",
    }

    def __init__(self, action=None):
        super().__init__()
        self.action = action

    def has_permission(self, request, view):
        action = self.action or self.actions.get(request.method)
        if not action:
            return False
        self.permission_code = f"prescription.{action}"
        return super().has_permission(request, view)

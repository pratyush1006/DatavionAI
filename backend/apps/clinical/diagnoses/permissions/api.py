"""DRF permission adapter for diagnosis endpoints."""

from apps.platform.rbac.permissions.base import RBACPermissionBase


class DiagnosisAPIPermission(RBACPermissionBase):
    """Require a diagnosis permission for every API method."""

    actions = {
        "GET": "view",
        "HEAD": "view",
        "POST": "create",
        "PATCH": "update",
        "PUT": "update",
        "DELETE": "delete",
    }

    def has_permission(self, request, view):
        action = self.actions.get(request.method)
        if action is None:
            return False
        self.permission_code = f"diagnosis.{action}"
        return super().has_permission(request, view)

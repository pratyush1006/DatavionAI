"""DRF permission adapter for encounter endpoints."""

from apps.platform.rbac.permissions.base import RBACPermissionBase


class EncounterAPIPermission(RBACPermissionBase):
    """Require a domain permission for every encounter API method."""

    actions = {
        "GET": "view",
        "HEAD": "view",
        "POST": "create",
        "PATCH": "update",
        "PUT": "update",
        "DELETE": "delete",
    }
    lifecycle_actions = {"start", "complete", "cancel"}

    def has_permission(self, request, view):
        if getattr(view, "action", None) == "lifecycle":
            if getattr(view, "kwargs", {}).get("action") not in self.lifecycle_actions:
                return False
            action = "transition"
        else:
            action = self.actions.get(request.method)
        if action is None:
            return False
        self.permission_code = f"encounter.{action}"
        return super().has_permission(request, view)

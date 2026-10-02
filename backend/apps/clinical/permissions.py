"""Shared fail-closed RBAC helper for clinical domain API views."""

from apps.platform.rbac.permissions.base import RBACPermissionBase


class ClinicalAPIPermission(RBACPermissionBase):
    """Require the configured clinical domain action at the API boundary."""

    domain = "clinical"
    actions = {
        "GET": "view",
        "HEAD": "view",
        "POST": "create",
        "PATCH": "update",
        "PUT": "update",
        "DELETE": "delete",
    }
    action_aliases = {}

    def __init__(self, action=None, domain=None, action_aliases=None):
        super().__init__()
        self.action = action
        self.domain = domain or type(self).domain
        self.action_aliases = (
            action_aliases if action_aliases is not None else type(self).action_aliases
        )

    def has_permission(self, request, view):
        view_action = getattr(view, "action", None)
        action = self.action
        if action is None:
            action = self.actions.get(request.method)
        if view_action in self.action_aliases:
            action = self.action_aliases[view_action]
        elif view_action in {"list", "retrieve"}:
            action = "view"
        elif view_action == "create":
            action = "create"
        elif view_action in {"update", "partial_update"}:
            action = "update"
        elif view_action == "destroy":
            action = "delete"
        elif view_action:
            action = "transition"
        if action is None or not self.domain:
            return False
        self.permission_code = f"{self.domain}.{action}"
        return super().has_permission(request, view)

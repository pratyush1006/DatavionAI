"""DRF permission adapters for appointment API operations."""

from apps.platform.rbac.permissions.base import RBACPermissionBase


class AppointmentAPIPermission(RBACPermissionBase):
    """Resolve the operation permission before an appointment view runs."""

    action_by_method = {
        "GET": "view",
        "HEAD": "view",
        "POST": "transition",
        "PATCH": "update",
        "DELETE": "delete",
    }
    message = "You do not have permission to perform this appointment operation."

    def __init__(self, action=None):
        super().__init__()
        self.action = action

    def has_permission(self, request, view):
        workflow_name = getattr(view, "workflow_name", "")
        action = (
            self.action
            or {
                "appointment.create": "create",
                "appointment.update": "update",
                "appointment.delete": "delete",
            }.get(workflow_name)
            or self.action_by_method.get(request.method)
        )
        if not action:
            return False
        self.permission_code = f"appointment.{action}"
        return super().has_permission(request, view)

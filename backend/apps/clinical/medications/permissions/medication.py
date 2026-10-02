from rest_framework.permissions import BasePermission


class MedicationPermission(BasePermission):
    """RBAC-compatible permission boundary.

    Superusers/staff are accepted for the existing platform administration
    flow. Other users must expose one of the canonical Django permission
    codenames or a project-level has_perm implementation.
    """

    action_map = {
        "GET": "medications.view_medication",
        "POST": "medications.add_medication",
        "PUT": "medications.change_medication",
        "PATCH": "medications.change_medication",
        "DELETE": "medications.delete_medication",
    }

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if getattr(user, "is_superuser", False) or getattr(user, "is_staff", False):
            return True
        codename = self.action_map.get(request.method)
        return bool(codename and user.has_perm(codename))

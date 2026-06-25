from rest_framework.permissions import BasePermission


class IsOrganizationAdmin(BasePermission):
    """
    Allows access only to organization admins.
    """

    def has_permission(self, request, view):
        return request.user.is_staff
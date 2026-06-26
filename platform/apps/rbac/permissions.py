from rest_framework.permissions import BasePermission


class HasPermission(BasePermission):
    """
    Base RBAC permission class.
    """

    permission_codename = None

    def has_permission(
        self,
        request,
        view,
    ):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        return request.user.has_perm(self.permission_codename)


# =====================================================
# User Permissions
# =====================================================


class CanViewUsers(HasPermission):
    permission_codename = "accounts.view_user"


class CanAddUsers(HasPermission):
    permission_codename = "accounts.add_user"


class CanChangeUsers(HasPermission):
    permission_codename = "accounts.change_user"


class CanDeleteUsers(HasPermission):
    permission_codename = "accounts.delete_user"


# =====================================================
# Organization Permissions
# =====================================================


class CanViewOrganizations(HasPermission):
    permission_codename = "organizations.view_organization"


class CanAddOrganizations(HasPermission):
    permission_codename = "organizations.add_organization"


class CanChangeOrganizations(HasPermission):
    permission_codename = "organizations.change_organization"


class CanDeleteOrganizations(HasPermission):
    permission_codename = "organizations.delete_organization"


# =====================================================
# RBAC Permissions
# =====================================================


class CanManageRoles(HasPermission):
    permission_codename = "auth.change_group"


class CanManagePermissions(HasPermission):
    permission_codename = "auth.change_permission"


class CanViewDepartments(BasePermission):
    """
    Permission to view departments.
    """

    def has_permission(self, request, view):
        return request.user.has_perm("departments.view_department")


class CanAddDepartments(BasePermission):
    """
    Permission to create departments.
    """

    def has_permission(self, request, view):
        return request.user.has_perm("departments.add_department")


class CanChangeDepartments(BasePermission):
    """
    Permission to update departments.
    """

    def has_permission(self, request, view):
        return request.user.has_perm("departments.change_department")


class CanDeleteDepartments(BasePermission):
    """
    Permission to delete departments.
    """

    def has_permission(self, request, view):
        return request.user.has_perm("departments.delete_department")

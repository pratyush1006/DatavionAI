from rest_framework.permissions import IsAuthenticated


class BasePermission(IsAuthenticated):
    """
    Base permission class.

    Future enhancements:
    - Organization-level access
    - Role-based permissions
    - Audit logging
    - Feature flags
    """

    pass

def require_authenticated(request):
    if not getattr(request.user, "is_authenticated", False):
        raise PermissionError("Authentication is required.")


def require_organization(request, organization_id):
    user_org = getattr(request.user, "organization_id", None)
    if user_org is not None and str(user_org) != str(organization_id):
        raise PermissionError("Cross-organization access denied.")

"""
Billing Core API request-context helpers.
"""

from __future__ import annotations

from rest_framework.permissions import IsAuthenticated


class BillingAPIViewMixin:
    """Require explicit tenant and organization context."""

    permission_classes = (IsAuthenticated,)

    def get_organization(self, request):
        """Return the explicit request organization after tenant verification."""
        organization = getattr(request, "organization", None)
        tenant = getattr(request, "tenant", None)
        if organization is None or tenant is None:
            raise PermissionError(
                "Billing requests require explicit tenant and organization context."
            )
        if organization.tenant_id != tenant.pk:
            raise PermissionError("Organization does not belong to the active tenant.")
        return organization

    def workflow_context(self, request, workflow_name: str):
        """Build the shared workflow context."""
        from apps.core.workflows import WorkflowContext

        organization = self.get_organization(request)
        return WorkflowContext(
            tenant_id=organization.tenant_id,
            actor_id=request.user.pk,
            workflow_name=workflow_name,
        )


__all__ = ("BillingAPIViewMixin",)

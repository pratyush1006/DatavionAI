"""HR RBAC adapter with organization and relationship validation."""

from django.apps import apps
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError

from apps.common.middleware.context import set_current_organization
from apps.datavionos.services.saas_capability_control_plane import get_provider
from apps.hr.scope import organization_lookup
from apps.platform.rbac.permissions.base import RBACPermissionBase

RELATIONS = {
    "department": ("departments", "Department"),
    "job": ("hr_recruitment", "JobOpening"),
    "candidate": ("hr_recruitment", "Candidate"),
    "interviewer": ("employees", "Employee"),
    "employee": ("employees", "Employee"),
    "reviewer": ("employees", "Employee"),
    "assigned_to": ("employees", "Employee"),
    "initiated_by": ("employees", "Employee"),
    "leave_type": ("hr_leave", "LeaveType"),
    "shift": ("hr_shifts", "Shift"),
    "process": ("hr_onboarding", "LifecycleProcess"),
    "cycle": ("hr_performance", "PerformanceReviewCycle"),
    "review": ("hr_performance", "PerformanceReview"),
}


class HrPermission(RBACPermissionBase):
    def has_permission(self, request, view) -> bool:
        organization = self._get_organization(request)
        if organization is None or not super().has_permission(request, view):
            return False
        snapshot = get_provider().resolve(user=request.user, organization=organization)
        if not snapshot.modules.get("hr", False):
            return False
        # Keep selectors and workflow lookups on the same resolved boundary.
        set_current_organization(organization)
        if request.method in ("POST", "PUT", "PATCH"):
            submitted = request.data.get("organization")
            if submitted is not None and str(submitted) != str(organization.pk):
                raise ValidationError(
                    {"organization": "Must match the selected organization."}
                )
            for name, (app_label, model_name) in RELATIONS.items():
                value = request.data.get(name)
                if value in (None, ""):
                    continue
                model = apps.get_model(app_label, model_name)
                try:
                    valid = model.objects.filter(
                        pk=value,
                        **{organization_lookup(model): organization.pk},
                    ).exists()
                except (ValueError, TypeError, DjangoValidationError):
                    valid = False
                if not valid:
                    raise ValidationError(
                        {name: "Select a record from the current organization."}
                    )
        return True

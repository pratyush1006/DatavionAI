from __future__ import annotations

from django.db import transaction
from django.db.models import Q

from apps.ai.models import AIApplication
from apps.organization.departments.models import DepartmentMember
from apps.organization.employees.models import Employee
from apps.platform.organizations.models import OrganizationFeature, OrganizationModule
from apps.platform.rbac.engines import user_has_permission
from apps.platform.saas_billing.services.entitlement_service import EntitlementService

AI_CATALOG = {
    "CLINICAL_AI": (
        "Clinical AI",
        "Clinical",
        "clinical",
        "clinical.ai",
        "clinical.ai.view",
    ),
    "LABORATORY_AI": (
        "Laboratory AI",
        "Laboratory",
        "laboratory",
        "laboratory.ai",
        "laboratory.ai.view",
    ),
    "PHARMACY_AI": (
        "Pharmacy AI",
        "Pharmacy",
        "pharmacy",
        "pharmacy.ai",
        "pharmacy.ai.view",
    ),
    "IMAGING_AI": (
        "Imaging AI",
        "Imaging",
        "imaging",
        "imaging.ai",
        "imaging.ai.view",
    ),
    "REVENUE_CYCLE_AI": (
        "Revenue Cycle AI",
        "Revenue Cycle",
        "rcm",
        "rcm.ai",
        "rcm.ai.view",
    ),
}


class DepartmentScopedAIControlService:
    """
    Canonical organization-scoped AI control plane.

    Effective AI access is determined by:

        SaaS entitlement
            -> organization module
            -> organization feature
            -> organization AI switch
            -> RBAC
            -> department membership
            -> AI application ownership
    """

    @staticmethod
    def descriptor(application):
        default = AI_CATALOG.get(
            str(application.code),
            (
                application.name,
                application.department,
                "",
                "",
                "ai.view",
            ),
        )

        configuration = dict(getattr(application, "configuration", {}) or {})

        return {
            "name": configuration.get("name", default[0]),
            "department": configuration.get(
                "owner_department",
                application.department or default[1],
            ),
            "module": configuration.get(
                "required_module",
                default[2],
            ),
            "feature": configuration.get(
                "required_feature",
                default[3],
            ),
            "permission": configuration.get(
                "required_permission",
                default[4],
            ),
            "human_review_required": bool(
                configuration.get(
                    "human_review_required",
                    False,
                )
            ),
            "governance": dict(
                configuration.get(
                    "governance",
                    {},
                )
                or {}
            ),
        }

    @staticmethod
    def module_enabled(organization, code):
        if not code:
            return False

        return OrganizationModule.objects.filter(
            organization=organization,
            module_code=str(code).strip().upper(),
            status=OrganizationModule.ModuleStatus.ENABLED,
        ).exists()

    @staticmethod
    def feature_enabled(organization, code):
        if not code:
            return False

        return OrganizationFeature.objects.filter(
            organization=organization,
            feature_code=str(code).strip(),
            status=OrganizationFeature.FeatureStatus.ENABLED,
            is_active=True,
        ).exists()

    @staticmethod
    def department_access(
        user,
        organization,
        department,
    ):
        if not user or not getattr(user, "is_authenticated", False) or not department:
            return False

        employees = Employee.objects.filter(
            organization=organization,
            user_id=user.pk,
        )

        return (
            DepartmentMember.objects.filter(
                employee__in=employees,
                department__organization=organization,
                department__is_active=True,
                is_active=True,
            )
            .filter(
                Q(department__code__iexact=department)
                | Q(department__name__iexact=department)
            )
            .exists()
        )

    @classmethod
    def entitlement_state(
        cls,
        organization,
        descriptor,
    ):
        try:
            entitled = EntitlementService.has_module(
                organization=organization,
                module=descriptor["module"],
            ) and EntitlementService.has_feature(
                organization=organization,
                feature=descriptor["feature"],
            )
        except Exception:
            entitled = False

        return bool(entitled)

    @classmethod
    def can_use(
        cls,
        *,
        user,
        organization,
        application,
    ):
        if application is None:
            return False

        if application.organization_id != organization.pk:
            return False

        if application.tenant_id != organization.tenant_id:
            return False

        if str(application.status).lower() != "active":
            return False

        descriptor = cls.descriptor(application)

        entitled = cls.entitlement_state(
            organization,
            descriptor,
        )

        if not entitled:
            return False

        if not cls.module_enabled(
            organization,
            descriptor["module"],
        ):
            return False

        if not cls.feature_enabled(
            organization,
            descriptor["feature"],
        ):
            return False

        if not user_has_permission(
            user=user,
            permission=descriptor["permission"],
            organization=organization,
        ):
            return False

        if not cls.department_access(
            user,
            organization,
            descriptor["department"],
        ):
            return False

        return True

    @classmethod
    def resolve(
        cls,
        *,
        user,
        organization,
    ):
        capabilities = []

        applications = AIApplication.objects.filter(
            tenant=organization.tenant,
            organization=organization,
        ).order_by("name", "code")

        for application in applications:
            descriptor = cls.descriptor(application)

            entitled = cls.entitlement_state(
                organization,
                descriptor,
            )

            module_on = cls.module_enabled(
                organization,
                descriptor["module"],
            )

            feature_on = cls.feature_enabled(
                organization,
                descriptor["feature"],
            )

            permission = user_has_permission(
                user=user,
                permission=descriptor["permission"],
                organization=organization,
            )

            department = cls.department_access(
                user,
                organization,
                descriptor["department"],
            )

            organization_enabled = str(application.status).lower() == "active"

            can_use = bool(
                organization_enabled
                and entitled
                and module_on
                and feature_on
                and permission
                and department
            )

            capabilities.append(
                {
                    "id": str(application.pk),
                    "code": str(application.code),
                    "name": descriptor["name"],
                    "department": descriptor["department"],
                    "status": str(application.status),
                    "organization_enabled": organization_enabled,
                    "entitled": bool(entitled),
                    "module_enabled": module_on,
                    "feature_enabled": feature_on,
                    "user_permission": bool(permission),
                    "department_access": bool(department),
                    "can_use": can_use,
                    "required_module": descriptor["module"],
                    "required_feature": descriptor["feature"],
                    "required_permission": descriptor["permission"],
                    "human_review_required": descriptor["human_review_required"],
                    "governance": descriptor["governance"],
                }
            )

        return {
            "organization": {
                "id": str(organization.pk),
                "name": organization.name,
                "code": organization.code,
            },
            "capabilities": capabilities,
            "can_manage_ai": user_has_permission(
                user=user,
                permission="ai.update",
                organization=organization,
            ),
        }

    @classmethod
    @transaction.atomic
    def set_enabled(
        cls,
        *,
        user,
        organization,
        application,
        enabled,
    ):
        if application.organization_id != organization.pk:
            raise PermissionError("AI application is outside organization scope.")

        if application.tenant_id != organization.tenant_id:
            raise PermissionError("AI application is outside tenant scope.")

        if not user_has_permission(
            user=user,
            permission="ai.update",
            organization=organization,
        ):
            raise PermissionError("Missing RBAC permission: ai.update.")

        descriptor = cls.descriptor(application)

        if enabled:
            if not EntitlementService.has_module(
                organization=organization,
                module=descriptor["module"],
            ):
                raise PermissionError("AI requires an entitled organization module.")

            if not EntitlementService.has_feature(
                organization=organization,
                feature=descriptor["feature"],
            ):
                raise PermissionError("AI requires an entitled organization feature.")

            if not cls.module_enabled(
                organization,
                descriptor["module"],
            ):
                raise PermissionError("Required organization module is disabled.")

            if not cls.feature_enabled(
                organization,
                descriptor["feature"],
            ):
                raise PermissionError("Required organization feature is disabled.")

        application.status = "active" if enabled else "inactive"

        application.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        return application


def can_use_department_ai(
    *,
    user,
    organization,
    application,
):
    """
    Canonical AI execution guard.

    All department-scoped AI execution must pass
    through this boundary.
    """

    return DepartmentScopedAIControlService.can_use(
        user=user,
        organization=organization,
        application=application,
    )

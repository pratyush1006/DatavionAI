from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from apps.platform.organizations.models import OrganizationModule
from apps.platform.saas_billing.services.entitlement_service import EntitlementService


class ModuleEntitlementError(ValidationError):
    """
    Raised when an organization attempts to activate a module that is not
    included in its current SaaS subscription entitlement.
    """

    default_code = "module_not_entitled"

    def __init__(
        self,
        message: str = (
            "Module is not included in the organization's active SaaS entitlement."
        ),
    ) -> None:
        super().__init__(message, code=self.default_code)


type OrganizationModuleData = Mapping[str, Any]


MUTABLE_FIELDS: frozenset[str] = frozenset(
    {
        "status",
        "settings",
        "enabled_at",
        "disabled_at",
    }
)


def _audit(event: str, module: OrganizationModule) -> None:
    _ = (event, module)


def _publish_event(event: str, module: OrganizationModule) -> None:
    _ = (event, module)


def _module_is_entitled(*, organization: Any, module_code: str) -> bool:
    if organization is None:
        return False
    code = str(module_code).strip()
    if not code:
        return False
    return EntitlementService.has_module(
        organization=organization,
        module=code,
    )


def _ensure_module_can_be_enabled(
    *,
    organization: Any,
    module_code: str,
) -> None:
    if not _module_is_entitled(
        organization=organization,
        module_code=module_code,
    ):
        raise ModuleEntitlementError(
            {
                "module_code": (
                    f"Module '{module_code}' is not included in the "
                    "organization's current SaaS subscription."
                ),
                "code": "module_not_entitled",
            }
        )


def _status_is_enabled(status: Any) -> bool:
    return status in (
        OrganizationModule.Status.ENABLED,
        OrganizationModule.Status.TRIAL,
    )


@transaction.atomic
def create_module(
    *,
    validated_data: OrganizationModuleData,
) -> OrganizationModule:
    data = dict(validated_data)
    organization = data.get("organization")
    module_code = str(data.get("module_code", "")).strip()
    requested_status = data.get(
        "status",
        OrganizationModule.Status.ENABLED,
    )

    if _status_is_enabled(requested_status):
        _ensure_module_can_be_enabled(
            organization=organization,
            module_code=module_code,
        )

    module = OrganizationModule.objects.create(**data)
    _audit("organization.module.created", module)
    _publish_event("organization.module.created", module)
    return module


@transaction.atomic
def update_module(
    *,
    instance: OrganizationModule,
    validated_data: OrganizationModuleData,
) -> OrganizationModule:
    if not validated_data:
        return instance

    data = dict(validated_data)
    requested_status = data.get("status")

    if requested_status is not None and _status_is_enabled(requested_status):
        _ensure_module_can_be_enabled(
            organization=instance.organization,
            module_code=instance.module_code,
        )

    update_fields: list[str] = []
    for field, value in data.items():
        if field not in MUTABLE_FIELDS:
            continue
        setattr(instance, field, value)
        update_fields.append(field)

    if update_fields:
        instance.save(update_fields=update_fields)
        _audit("organization.module.updated", instance)
        _publish_event("organization.module.updated", instance)

    return instance


@transaction.atomic
def enable_module(
    *,
    instance: OrganizationModule,
) -> OrganizationModule:
    _ensure_module_can_be_enabled(
        organization=instance.organization,
        module_code=instance.module_code,
    )

    if instance.status == OrganizationModule.Status.ENABLED:
        return instance

    instance.status = OrganizationModule.Status.ENABLED
    instance.enabled_at = timezone.now()
    instance.disabled_at = None
    instance.save(
        update_fields=[
            "status",
            "enabled_at",
            "disabled_at",
        ],
    )
    _audit("organization.module.enabled", instance)
    _publish_event("organization.module.enabled", instance)
    return instance


@transaction.atomic
def disable_module(
    *,
    instance: OrganizationModule,
) -> OrganizationModule:
    if instance.status == OrganizationModule.Status.DISABLED:
        return instance

    instance.status = OrganizationModule.Status.DISABLED
    instance.disabled_at = timezone.now()
    instance.save(
        update_fields=[
            "status",
            "disabled_at",
        ],
    )
    _audit("organization.module.disabled", instance)
    _publish_event("organization.module.disabled", instance)
    return instance


__all__: tuple[str, ...] = (
    "ModuleEntitlementError",
    "OrganizationModuleData",
    "create_module",
    "disable_module",
    "enable_module",
    "update_module",
)

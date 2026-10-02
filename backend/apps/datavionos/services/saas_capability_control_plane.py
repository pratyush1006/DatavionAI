from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from apps.datavionos.resolvers.entitlement import EntitlementResolver
from apps.datavionos.resolvers.permissions import PermissionResolver
from apps.platform.organizations.models import OrganizationFeature, OrganizationModule
from apps.platform.rbac.selectors.user_role import get_user_roles_for_user


@dataclass(frozen=True)
class SaaSCapabilitySnapshot:
    """Effective upstream capability inputs for one user and organization."""

    modules: dict[str, bool]
    features: dict[str, bool]
    permissions: frozenset[str]
    roles: frozenset[str] = frozenset()
    tenant_id: str | None = None
    organization_id: str | None = None
    user_id: str | None = None
    departments: frozenset[str] = frozenset()
    ai_capabilities: dict[str, bool] | None = None


class SaaSCapabilityProvider:
    """Canonical composition of SaaS, organization controls and RBAC.

    Billing is the upper bound.
    Organization controls may only reduce purchased entitlement.
    RBAC remains user-scoped.
    """

    MODULE_ON_STATES = frozenset(
        {
            OrganizationModule.Status.ENABLED,
            OrganizationModule.Status.TRIAL,
        }
    )

    FEATURE_ON_STATES = frozenset(
        {
            OrganizationFeature.FeatureStatus.ENABLED,
            OrganizationFeature.FeatureStatus.TRIAL,
        }
    )

    def resolve(
        self,
        *,
        user: Any,
        organization: Any,
    ) -> SaaSCapabilitySnapshot:
        if organization is None:
            return SaaSCapabilitySnapshot(
                modules={},
                features={},
                permissions=frozenset(),
                roles=frozenset(),
                ai_capabilities={},
            )

        capabilities = EntitlementResolver.resolve(
            organization=organization,
        )

        entitled_modules = self._boolean_map(capabilities.get("modules", {}))
        entitled_features = self._boolean_map(capabilities.get("features", {}))

        modules, departments, ai_capabilities = self._apply_module_overrides(
            organization=organization,
            entitled_modules=entitled_modules,
        )

        features = self._apply_feature_overrides(
            organization=organization,
            entitled_features=entitled_features,
        )

        # AI cannot be activated by local settings unless the
        # corresponding SaaS feature is purchased and enabled.
        ai_capabilities = {
            key: enabled
            for key, enabled in ai_capabilities.items()
            if enabled and features.get(key, False)
        }

        permissions = frozenset()

        if user is not None and getattr(
            user,
            "is_authenticated",
            False,
        ):
            permissions = frozenset(
                PermissionResolver().resolve(
                    user=user,
                    organization=organization,
                )
            )

        roles = self._resolve_role_codes(user)

        tenant_id = getattr(
            organization,
            "tenant_id",
            None,
        )

        if tenant_id is None:
            tenant_id = getattr(
                getattr(
                    organization,
                    "tenant",
                    None,
                ),
                "pk",
                None,
            )

        return SaaSCapabilitySnapshot(
            modules=modules,
            features=features,
            permissions=permissions,
            roles=roles,
            tenant_id=str(tenant_id or "") or None,
            organization_id=str(
                getattr(
                    organization,
                    "pk",
                    "",
                )
                or ""
            )
            or None,
            user_id=str(
                getattr(
                    user,
                    "pk",
                    "",
                )
                or ""
            )
            or None,
            departments=frozenset(departments),
            ai_capabilities=ai_capabilities,
        )

    @staticmethod
    def _resolve_role_codes(
        user: Any,
    ) -> frozenset[str]:
        """Resolve active canonical RBAC role codes for the user."""

        if user is None:
            return frozenset()

        if not getattr(
            user,
            "is_authenticated",
            False,
        ):
            return frozenset()

        assignments = get_user_roles_for_user(
            user=user,
        )

        role_codes: set[str] = set()

        for assignment in assignments:
            if not getattr(
                assignment,
                "is_active",
                True,
            ):
                continue

            role = getattr(
                assignment,
                "role",
                None,
            )

            if role is None:
                continue

            if not getattr(
                role,
                "is_active",
                True,
            ):
                continue

            code = getattr(
                role,
                "code",
                None,
            )

            if code:
                role_codes.add(str(code))

        return frozenset(role_codes)

    @classmethod
    def resolve_organization_modules(
        cls,
        *,
        organization: Any,
        entitled_modules: Mapping[str, bool],
    ) -> dict[str, bool]:
        modules, _, _ = cls._apply_module_overrides(
            organization=organization,
            entitled_modules=cls._boolean_map(entitled_modules),
        )
        return modules

    @classmethod
    def resolve_organization_features(
        cls,
        *,
        organization: Any,
        entitled_features: Mapping[str, bool],
    ) -> dict[str, bool]:
        return cls._apply_feature_overrides(
            organization=organization,
            entitled_features=cls._boolean_map(entitled_features),
        )

    @classmethod
    def resolve_organization_scopes(
        cls,
        *,
        organization: Any,
        entitled_modules: Mapping[str, bool],
        entitled_features: Mapping[str, bool] | None = None,
    ) -> tuple[set[str], dict[str, bool]]:
        _, departments, ai_capabilities = cls._apply_module_overrides(
            organization=organization,
            entitled_modules=cls._boolean_map(entitled_modules),
        )

        if entitled_features is not None:
            features = cls._boolean_map(entitled_features)

            ai_capabilities = {
                key: enabled
                for key, enabled in ai_capabilities.items()
                if enabled and features.get(key, False)
            }

        return departments, ai_capabilities

    @classmethod
    def _apply_module_overrides(
        cls,
        *,
        organization: Any,
        entitled_modules: Mapping[str, bool],
    ) -> tuple[
        dict[str, bool],
        set[str],
        dict[str, bool],
    ]:
        effective = {
            str(key).strip(): bool(value)
            for key, value in entitled_modules.items()
            if str(key).strip()
        }

        departments: set[str] = set()
        ai_capabilities: dict[str, bool] = {}

        for override in OrganizationModule.objects.filter(
            organization=organization,
        ):
            code = str(
                getattr(
                    override,
                    "module_code",
                    "",
                )
            ).strip()

            if not code:
                continue

            matching_key = next(
                (key for key in effective if key.casefold() == code.casefold()),
                None,
            )

            if matching_key is None:
                # Organization rows can never manufacture
                # billing entitlement.
                continue

            enabled = (
                getattr(
                    override,
                    "status",
                    None,
                )
                in cls.MODULE_ON_STATES
                and effective[matching_key]
            )

            effective[matching_key] = bool(enabled)

            settings = getattr(
                override,
                "settings",
                None,
            )

            if not enabled or not isinstance(
                settings,
                Mapping,
            ):
                continue

            department = settings.get("department_code") or settings.get("department")

            if isinstance(department, str) and department.strip():
                departments.add(department.strip().upper())

            configured_ai = settings.get("ai_capabilities")

            if isinstance(
                configured_ai,
                Mapping,
            ):
                for ai_key, ai_enabled in configured_ai.items():
                    if isinstance(ai_enabled, bool) and str(ai_key).strip():
                        ai_capabilities[str(ai_key).strip()] = ai_enabled

        return (
            effective,
            departments,
            ai_capabilities,
        )

    @classmethod
    def _apply_feature_overrides(
        cls,
        *,
        organization: Any,
        entitled_features: Mapping[str, bool],
    ) -> dict[str, bool]:
        effective = {
            str(key).strip(): bool(value)
            for key, value in entitled_features.items()
            if str(key).strip()
        }

        for override in OrganizationFeature.objects.filter(
            organization=organization,
        ):
            code = str(
                getattr(
                    override,
                    "feature_code",
                    "",
                )
            ).strip()

            if not code:
                continue

            matching_key = next(
                (key for key in effective if key.casefold() == code.casefold()),
                None,
            )

            if matching_key is None:
                continue

            effective[matching_key] = bool(
                getattr(
                    override,
                    "status",
                    None,
                )
                in cls.FEATURE_ON_STATES
                and effective[matching_key]
            )

        return effective

    @staticmethod
    def _boolean_map(
        value: object,
    ) -> dict[str, bool]:
        if not isinstance(
            value,
            Mapping,
        ):
            return {}

        return {
            str(key).strip(): enabled
            for key, enabled in value.items()
            if (str(key).strip() and isinstance(enabled, bool))
        }


_provider = SaaSCapabilityProvider()


def register_provider(
    provider: SaaSCapabilityProvider,
) -> None:
    global _provider
    _provider = provider


def get_provider() -> SaaSCapabilityProvider:
    return _provider


__all__ = (
    "SaaSCapabilityProvider",
    "SaaSCapabilitySnapshot",
    "get_provider",
    "register_provider",
)


class DefaultSaaSCapabilityProvider:
    """Concrete adapter for existing SaaS, organization and RBAC authorities."""

    ENABLED_MODULE_STATES = frozenset({"enabled", "trial"})

    ENABLED_FEATURE_STATES = frozenset({"enabled", "trial"})

    def resolve(
        self,
        *,
        user,
        organization,
    ):
        if organization is None:
            return SaaSCapabilitySnapshot(
                modules={},
                features={},
                permissions=frozenset(),
                roles=frozenset(),
            )

        capabilities = EntitlementResolver.resolve(
            organization=organization,
        )

        if not isinstance(
            capabilities,
            dict,
        ):
            capabilities = {}

        modules = self._merge(
            organization,
            capabilities.get(
                "modules",
                {},
            ),
            OrganizationModule,
            "module_code",
            self.ENABLED_MODULE_STATES,
        )

        features = self._merge(
            organization,
            capabilities.get(
                "features",
                {},
            ),
            OrganizationFeature,
            "feature_code",
            self.ENABLED_FEATURE_STATES,
        )

        permissions = (
            frozenset(
                PermissionResolver().resolve(
                    user=user,
                    organization=organization,
                )
            )
            if user is not None
            and getattr(
                user,
                "is_authenticated",
                True,
            )
            else frozenset()
        )

        roles = SaaSCapabilityProvider._resolve_role_codes(user)

        return SaaSCapabilitySnapshot(
            modules=modules,
            features=features,
            permissions=permissions,
            roles=roles,
            tenant_id=str(
                getattr(
                    organization,
                    "tenant_id",
                    "",
                )
                or ""
            )
            or None,
            organization_id=str(
                getattr(
                    organization,
                    "pk",
                    getattr(
                        organization,
                        "id",
                        "",
                    ),
                )
            ),
            user_id=str(
                getattr(
                    user,
                    "pk",
                    getattr(
                        user,
                        "id",
                        "",
                    ),
                )
            ),
        )

    @staticmethod
    def _merge(
        organization,
        entitled,
        model,
        code_field,
        enabled_states,
    ):
        effective = {str(k): bool(v) for k, v in (entitled or {}).items()}

        for item in model.objects.filter(organization=organization).only(
            code_field,
            "status",
        ):
            code = str(
                getattr(
                    item,
                    code_field,
                    "",
                )
                or ""
            ).strip()

            if not code:
                continue

            if code in effective:
                effective[code] = (
                    effective[code]
                    and str(
                        getattr(
                            item,
                            "status",
                            "",
                        )
                    ).lower()
                    in enabled_states
                )
            else:
                # Organization settings can disable
                # plan entitlement, never grant it.
                effective[code] = False

        return effective


def register_default_provider() -> None:
    global _provider

    if _provider is None:
        register_provider(DefaultSaaSCapabilityProvider())


register_default_provider()

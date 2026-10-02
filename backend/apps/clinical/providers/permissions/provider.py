"""Provider permission boundary using canonical RBAC resolution."""

from __future__ import annotations

from typing import Any

from apps.platform.rbac.resolvers import resolve_permissions


class ProviderPermission:
    """Stateless Provider permission checks."""

    @staticmethod
    def _organization(*, organization: Any = None, provider: Any = None) -> Any:
        if organization is not None:
            return organization
        if provider is not None:
            return getattr(provider, "organization", None)
        return None

    @classmethod
    def has_permission(
        cls,
        *,
        user: Any,
        permission: str,
        organization: Any = None,
        provider: Any = None,
    ) -> bool:
        organization = cls._organization(
            organization=organization,
            provider=provider,
        )
        return permission in resolve_permissions(
            user=user,
            organization=organization,
        )

    @classmethod
    def can_view(
        cls,
        *,
        user: Any,
        organization: Any = None,
        provider: Any = None,
    ) -> bool:
        return cls.has_permission(
            user=user,
            permission="providers.view",
            organization=organization,
            provider=provider,
        )

    @classmethod
    def can_create(
        cls,
        *,
        user: Any,
        organization: Any = None,
    ) -> bool:
        return cls.has_permission(
            user=user,
            permission="providers.create",
            organization=organization,
        )

    @classmethod
    def can_update(
        cls,
        *,
        user: Any,
        organization: Any = None,
        provider: Any = None,
    ) -> bool:
        return cls.has_permission(
            user=user,
            permission="providers.update",
            organization=organization,
            provider=provider,
        )

    @classmethod
    def can_delete(
        cls,
        *,
        user: Any,
        organization: Any = None,
        provider: Any = None,
    ) -> bool:
        return cls.has_permission(
            user=user,
            permission="providers.delete",
            organization=organization,
            provider=provider,
        )

    @classmethod
    def can_activate(
        cls,
        *,
        user: Any,
        organization: Any = None,
        provider: Any = None,
    ) -> bool:
        return cls.has_permission(
            user=user,
            permission="providers.activate",
            organization=organization,
            provider=provider,
        )

    @classmethod
    def can_deactivate(
        cls,
        *,
        user: Any,
        organization: Any = None,
        provider: Any = None,
    ) -> bool:
        return cls.has_permission(
            user=user,
            permission="providers.deactivate",
            organization=organization,
            provider=provider,
        )

    @classmethod
    def can_verify(
        cls,
        *,
        user: Any,
        organization: Any = None,
        provider: Any = None,
    ) -> bool:
        return cls.has_permission(
            user=user,
            permission="providers.verify",
            organization=organization,
            provider=provider,
        )

    @classmethod
    def can_assign(
        cls,
        *,
        user: Any,
        organization: Any = None,
        provider: Any = None,
    ) -> bool:
        return cls.has_permission(
            user=user,
            permission="providers.assign",
            organization=organization,
            provider=provider,
        )


__all__ = ("ProviderPermission",)


class _ProviderDRFPermissionBase:
    """Django REST Framework permission adapter for Provider RBAC."""

    permission_name = ""

    def has_permission(self, request, view):
        user = getattr(request, "user", None)
        organization = getattr(request, "organization", None)
        if organization is None:
            organization = getattr(view, "organization", None)
        return ProviderPermission.has_permission(
            user=user,
            permission=self.permission_name,
            organization=organization,
        )


class CanViewProvider(_ProviderDRFPermissionBase):
    permission_name = "providers.view"


class CanCreateProvider(_ProviderDRFPermissionBase):
    permission_name = "providers.create"


class CanUpdateProvider(_ProviderDRFPermissionBase):
    permission_name = "providers.update"


class CanDeleteProvider(_ProviderDRFPermissionBase):
    permission_name = "providers.delete"


class CanActivateProvider(_ProviderDRFPermissionBase):
    permission_name = "providers.activate"


class CanDeactivateProvider(_ProviderDRFPermissionBase):
    permission_name = "providers.deactivate"


class CanVerifyProvider(_ProviderDRFPermissionBase):
    permission_name = "providers.verify"


class CanAssignProvider(_ProviderDRFPermissionBase):
    permission_name = "providers.assign"


__all__ = (
    "ProviderPermission",
    "CanViewProvider",
    "CanCreateProvider",
    "CanUpdateProvider",
    "CanDeleteProvider",
    "CanActivateProvider",
    "CanDeactivateProvider",
    "CanVerifyProvider",
    "CanAssignProvider",
)

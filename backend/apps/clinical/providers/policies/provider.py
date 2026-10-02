"""Authorization policy for Clinical Providers."""

from __future__ import annotations

from typing import Any

from apps.platform.rbac.resolvers import resolve_permissions


class ProviderPolicy:
    """Organization-scoped Provider authorization policy."""

    @staticmethod
    def _organization(*, organization: Any = None, provider: Any = None) -> Any:
        if organization is not None:
            return organization
        if provider is not None:
            return getattr(provider, "organization", None)
        return None

    @classmethod
    def _check(
        cls,
        *,
        actor: Any,
        permission: str,
        organization: Any = None,
        provider: Any = None,
    ) -> bool:
        organization = cls._organization(
            organization=organization,
            provider=provider,
        )
        return permission in resolve_permissions(
            user=actor,
            organization=organization,
        )

    @classmethod
    def can_view(
        cls, *, actor: Any, organization: Any = None, provider: Any = None
    ) -> bool:
        return cls._check(
            actor=actor,
            permission="providers.view",
            organization=organization,
            provider=provider,
        )

    @classmethod
    def can_create(cls, *, actor: Any, organization: Any) -> bool:
        return cls._check(
            actor=actor, permission="providers.create", organization=organization
        )

    @classmethod
    def can_update(
        cls, *, actor: Any, provider: Any = None, organization: Any = None
    ) -> bool:
        return cls._check(
            actor=actor,
            permission="providers.update",
            organization=organization,
            provider=provider,
        )

    @classmethod
    def can_manage(
        cls, *, actor: Any, provider: Any = None, organization: Any = None
    ) -> bool:
        return cls.can_update(actor=actor, provider=provider, organization=organization)

    @classmethod
    def can_delete(
        cls, *, actor: Any, provider: Any = None, organization: Any = None
    ) -> bool:
        return cls._check(
            actor=actor,
            permission="providers.delete",
            organization=organization,
            provider=provider,
        )

    @classmethod
    def can_activate(
        cls, *, actor: Any, provider: Any = None, organization: Any = None
    ) -> bool:
        return cls._check(
            actor=actor,
            permission="providers.activate",
            organization=organization,
            provider=provider,
        )

    @classmethod
    def can_deactivate(
        cls, *, actor: Any, provider: Any = None, organization: Any = None
    ) -> bool:
        return cls._check(
            actor=actor,
            permission="providers.deactivate",
            organization=organization,
            provider=provider,
        )

    @classmethod
    def can_verify(
        cls, *, actor: Any, provider: Any = None, organization: Any = None
    ) -> bool:
        return cls._check(
            actor=actor,
            permission="providers.verify",
            organization=organization,
            provider=provider,
        )

    @classmethod
    def can_assign(
        cls, *, actor: Any, provider: Any = None, organization: Any = None
    ) -> bool:
        return cls._check(
            actor=actor,
            permission="providers.assign",
            organization=organization,
            provider=provider,
        )


__all__ = ("ProviderPolicy",)

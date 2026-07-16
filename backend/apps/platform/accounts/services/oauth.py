"""
OAuth authentication services.
"""

from __future__ import annotations

from django.db import transaction

from apps.common.exceptions import ValidationException
from apps.platform.accounts.constants import OAuthProvider
from apps.platform.accounts.models import (
    OAuthAccount,
    User,
)


class OAuthService:
    """
    Business services for OAuth authentication.

    This service orchestrates OAuth authentication workflows.
    Provider-specific token validation should be implemented
    by dedicated provider adapters.
    """

    @staticmethod
    def validate_token(
        *,
        provider: OAuthProvider,
        token: str,
    ) -> dict:
        """
        Validate an OAuth token.

        Provider-specific validation will be implemented
        later.
        """

        raise NotImplementedError(
            f"{provider.label} OAuth validation is not implemented.",
        )

    @staticmethod
    def get_oauth_account(
        *,
        provider: OAuthProvider,
        provider_user_id: str,
    ) -> OAuthAccount | None:
        """
        Return an OAuth account.
        """

        return (
            OAuthAccount.objects.filter(
                provider=provider,
                provider_user_id=provider_user_id,
                is_active=True,
            )
            .select_related("user")
            .first()
        )

    @classmethod
    @transaction.atomic
    def login(
        cls,
        *,
        provider: OAuthProvider,
        token: str,
    ) -> User:
        """
        Authenticate using an OAuth provider.
        """

        profile = cls.validate_token(
            provider=provider,
            token=token,
        )

        account = cls.get_oauth_account(
            provider=provider,
            provider_user_id=profile["provider_user_id"],
        )

        if account is None:
            raise ValidationException(
                "OAuth account is not linked.",
            )

        return account.user

    @staticmethod
    @transaction.atomic
    def link_account(
        *,
        user: User,
        provider: OAuthProvider,
        provider_user_id: str,
        email: str,
        metadata: dict | None = None,
    ) -> OAuthAccount:
        """
        Link an OAuth account to a user.
        """

        account, _ = OAuthAccount.objects.update_or_create(
            provider=provider,
            provider_user_id=provider_user_id,
            defaults={
                "user": user,
                "email": email,
                "metadata": metadata or {},
                "is_active": True,
            },
        )

        return account

    @staticmethod
    @transaction.atomic
    def unlink_account(
        *,
        account: OAuthAccount,
    ) -> None:
        """
        Deactivate an OAuth account.
        """

        account.is_active = False

        account.save(
            update_fields=[
                "is_active",
                "updated_at",
            ],
        )


__all__ = [
    "OAuthService",
]

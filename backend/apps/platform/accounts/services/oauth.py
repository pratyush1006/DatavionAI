"""
OAuth authentication services.

Handles:

- OAuth token validation
- OAuth account linking
- OAuth login
- OAuth identity lifecycle

Provider-specific validation is delegated
to OAuth adapters.
"""

from __future__ import annotations

from typing import Any

from django.db import transaction
from django.utils import timezone

from apps.common.exceptions import (
    ValidationException,
)
from apps.platform.accounts.constants import (
    OAuthProvider,
)
from apps.platform.accounts.models import (
    OAuthAccount,
    User,
)
from apps.platform.accounts.services.authentication import (
    AuthenticationService,
)


class OAuthService:
    """
    OAuth authentication business service.

    Responsibilities:

    - Resolve OAuth identity
    - Link provider accounts
    - Issue authentication tokens
    - Maintain OAuth lifecycle
    """

    @staticmethod
    def validate_token(
        *,
        provider: OAuthProvider,
        token: str,
    ) -> dict[str, Any]:
        """
        Validate OAuth token.

        Provider adapters implement
        actual verification.
        """

        raise NotImplementedError(
            (f"{provider.label} OAuth validation adapter is not configured."),
        )

    @staticmethod
    def get_oauth_account(
        *,
        provider: OAuthProvider,
        provider_user_id: str,
    ) -> OAuthAccount | None:
        """
        Retrieve active OAuth identity.
        """

        return (
            OAuthAccount.objects.filter(
                provider=provider,
                provider_user_id=provider_user_id,
                is_active=True,
            )
            .select_related(
                "user",
            )
            .first()
        )

    @classmethod
    @transaction.atomic
    def login(
        cls,
        *,
        provider: OAuthProvider,
        token: str,
        ip_address: str = "",
        device: str = "Unknown Device",
        location: str = "Unknown Location",
    ) -> dict[str, str]:
        """
        Authenticate using OAuth provider.
        """

        profile = cls.validate_token(
            provider=provider,
            token=token,
        )

        provider_user_id = profile.get(
            "provider_user_id",
        )

        if not provider_user_id:
            raise ValidationException(
                message=("OAuth provider identity is missing."),
            )

        account = cls.get_oauth_account(
            provider=provider,
            provider_user_id=provider_user_id,
        )

        if account is None:
            raise ValidationException(
                message=("OAuth account is not linked to a DatavionOS account."),
            )

        if not account.user.is_active:
            raise ValidationException(
                message=("User account is inactive."),
            )

        now = timezone.now()

        account.last_login_at = now

        account.save(
            update_fields=[
                "last_login_at",
                "updated_at",
            ],
        )

        account.user.last_login = now

        account.user.save(
            update_fields=[
                "last_login",
                "updated_at",
            ],
        )

        transaction.on_commit(
            lambda: AuthenticationService._send_login_alert(
                user=account.user,
                ip_address=ip_address,
                device=device,
                location=location,
            ),
        )

        return AuthenticationService.issue_tokens(
            user=account.user,
        )

    @staticmethod
    @transaction.atomic
    def link_account(
        *,
        user: User,
        provider: OAuthProvider,
        provider_user_id: str,
        email: str,
        metadata: dict[str, Any] | None = None,
    ) -> OAuthAccount:
        """
        Link OAuth identity with user.
        """

        return OAuthAccount.objects.update_or_create(
            provider=provider,
            provider_user_id=provider_user_id,
            defaults={
                "user": user,
                "email": email.strip().lower(),
                "metadata": metadata or {},
                "is_active": True,
                "last_synced_at": timezone.now(),
            },
        )[0]

    @staticmethod
    @transaction.atomic
    def unlink_account(
        *,
        account: OAuthAccount,
    ) -> None:
        """
        Disable OAuth identity.
        """

        account.is_active = False

        account.save(
            update_fields=[
                "is_active",
                "updated_at",
            ],
        )


__all__ = ("OAuthService",)

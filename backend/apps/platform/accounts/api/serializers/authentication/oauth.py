"""
OAuth authentication serializers.

Handles:

- Google OAuth login
- Microsoft OAuth login
- Provider validation
- OAuth authentication workflow
"""

from __future__ import annotations

from typing import Any

from rest_framework import serializers

from apps.platform.accounts.constants import (
    OAuthProvider,
)
from apps.platform.accounts.services import (
    OAuthService,
)


class BaseOAuthSerializer(
    serializers.Serializer,
):
    """
    Base OAuth authentication serializer.

    Provider specific serializers inherit
    from this class.
    """

    token = serializers.CharField(
        write_only=True,
        trim_whitespace=True,
        min_length=10,
    )

    provider: OAuthProvider | None = None

    def validate_token(
        self,
        value: str,
    ) -> str:
        """
        Validate OAuth access token.
        """

        token = value.strip()

        if not token:
            raise serializers.ValidationError(
                "OAuth token is required.",
            )

        return token

    def validate(
        self,
        attrs: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Validate provider configuration.
        """

        if self.provider is None:
            raise serializers.ValidationError(
                "OAuth provider is not configured.",
            )

        return attrs

    def save(
        self,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Authenticate OAuth user.

        Returns authentication payload.
        """

        return OAuthService.login(
            provider=self.provider,
            token=self.validated_data["token"],
            ip_address=self.context.get(
                "ip_address",
                "",
            ),
            device=self.context.get(
                "device",
                "Unknown Device",
            ),
            location=self.context.get(
                "location",
                "Unknown Location",
            ),
        )


class GoogleLoginSerializer(
    BaseOAuthSerializer,
):
    """
    Google OAuth authentication.
    """

    provider = OAuthProvider.GOOGLE


class MicrosoftLoginSerializer(
    BaseOAuthSerializer,
):
    """
    Microsoft OAuth authentication.
    """

    provider = OAuthProvider.MICROSOFT


__all__ = (
    "GoogleLoginSerializer",
    "MicrosoftLoginSerializer",
)

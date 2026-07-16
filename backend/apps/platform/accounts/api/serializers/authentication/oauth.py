"""
OAuth authentication serializers.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.platform.accounts.constants import OAuthProvider
from apps.platform.accounts.models import User
from apps.platform.accounts.services import OAuthService


class BaseOAuthSerializer(serializers.Serializer):
    """
    Base serializer for OAuth authentication.
    """

    token = serializers.CharField()

    provider: OAuthProvider

    def save(
        self,
        **kwargs,
    ) -> User:
        """
        Authenticate using the configured OAuth provider.
        """

        return OAuthService.login(
            provider=self.provider,
            token=self.validated_data["token"],
        )


class GoogleLoginSerializer(BaseOAuthSerializer):
    """
    Google OAuth login serializer.
    """

    provider = OAuthProvider.GOOGLE


class MicrosoftLoginSerializer(BaseOAuthSerializer):
    """
    Microsoft OAuth login serializer.
    """

    provider = OAuthProvider.MICROSOFT


__all__ = [
    "GoogleLoginSerializer",
    "MicrosoftLoginSerializer",
]

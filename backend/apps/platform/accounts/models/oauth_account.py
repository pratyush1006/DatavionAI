"""
OAuth account model for the Accounts application.
"""

from __future__ import annotations

from django.conf import settings
from django.db import models

from apps.core.models import (
    TimeStampedModel,
    UUIDModel,
)
from apps.platform.accounts.constants import OAuthProvider


class OAuthAccount(
    UUIDModel,
    TimeStampedModel,
):
    """
    OAuth identity linked to a Datavion AI user.

    This model stores provider identity information only.

    Access tokens and refresh tokens should never be permanently
    stored in this model. Authentication services are responsible
    for securely managing provider credentials when required.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="oauth_accounts",
        help_text="User associated with this OAuth account.",
    )

    provider = models.CharField(
        max_length=20,
        choices=OAuthProvider.choices,
        db_index=True,
        help_text="OAuth provider.",
    )

    provider_user_id = models.CharField(
        max_length=255,
        db_index=True,
        help_text="Unique user identifier provided by the OAuth provider.",
    )

    provider_username = models.CharField(
        max_length=255,
        blank=True,
        help_text="Display name returned by the OAuth provider.",
    )

    email = models.EmailField(
        db_index=True,
        help_text="Email address received from the OAuth provider.",
    )

    avatar_url = models.URLField(
        blank=True,
        help_text="Provider profile image URL.",
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text="Additional provider-specific profile information.",
    )

    token_metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text=(
            "Non-sensitive OAuth token information such as scopes "
            "and expiration metadata."
        ),
    )

    last_login_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Last successful OAuth login.",
    )

    last_synced_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Last profile synchronization with the provider.",
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Whether this OAuth account is currently active.",
    )

    class Meta:
        verbose_name = "OAuth Account"
        verbose_name_plural = "OAuth Accounts"

        ordering = ("-created_at",)

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "provider",
                    "provider_user_id",
                ],
                name="unique_oauth_provider_user",
            ),
        ]

        indexes = [
            models.Index(
                fields=[
                    "provider",
                ],
            ),
            models.Index(
                fields=[
                    "provider_user_id",
                ],
            ),
            models.Index(
                fields=[
                    "email",
                ],
            ),
            models.Index(
                fields=[
                    "user",
                ],
            ),
            models.Index(
                fields=[
                    "is_active",
                ],
            ),
        ]

    @property
    def is_google(self) -> bool:
        """
        Return whether the provider is Google.
        """

        return self.provider == OAuthProvider.GOOGLE

    @property
    def is_microsoft(self) -> bool:
        """
        Return whether the provider is Microsoft.
        """

        return self.provider == OAuthProvider.MICROSOFT

    def __str__(self) -> str:
        """
        Return a human-readable representation.
        """

        return f"{self.provider}: {self.email}"


__all__ = [
    "OAuthAccount",
]

"""
Authentication services.
"""

from __future__ import annotations

from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import User


def generate_tokens(
    *,
    user: User,
) -> dict[str, str]:
    """
    Generate JWT access and refresh tokens.
    """

    refresh = RefreshToken.for_user(
        user,
    )

    return {
        "access": str(
            refresh.access_token,
        ),
        "refresh": str(
            refresh,
        ),
    }


__all__ = [
    "generate_tokens",
]

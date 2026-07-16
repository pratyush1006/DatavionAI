"""
Authentication services.
"""

from __future__ import annotations

from typing import Any

from django.contrib.auth import authenticate
from django.db import transaction
from django.utils import timezone
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.common.exceptions import AuthenticationException
from apps.platform.accounts.constants import OTPPurpose
from apps.platform.accounts.models import User
from apps.platform.accounts.services.otp import OTPService
from apps.platform.accounts.services.user import UserService
from apps.platform.notifications.services import (
    NotificationService,
)


class AuthenticationService:
    """
    Business service responsible for user authentication.

    Responsibilities:

    - Register users
    - Authenticate users
    - Login users
    - Logout users
    - Refresh JWT tokens
    - Issue JWT tokens

    This service contains business logic only.
    """

    @staticmethod
    @transaction.atomic
    def register(
        **validated_data: Any,
    ) -> User:
        """
        Register a new user.

        A verification OTP is generated immediately.
        The verification email is sent only after the
        transaction commits successfully.
        """

        user = UserService.create(
            **validated_data,
        )

        otp = OTPService.create(
            user=user,
            purpose=OTPPurpose.EMAIL_VERIFICATION,
            recipient=user.email,
        )

        transaction.on_commit(
            lambda: NotificationService.send_verification_otp(
                user=user,
                email=user.email,
                name=user.get_full_name() or user.email,
                otp=otp.code,
            ),
        )

        return user

    @staticmethod
    def authenticate_user(
        *,
        email: str,
        password: str,
    ) -> User:
        """
        Authenticate a user using email and password.
        """

        user = authenticate(
            username=email,
            password=password,
        )

        if user is None:
            raise AuthenticationException(
                message="Invalid email or password.",
            )

        if not user.is_active:
            raise AuthenticationException(
                message="User account is inactive.",
            )

        if not user.is_verified:
            raise AuthenticationException(
                message="Please verify your email before logging in.",
            )

        return user

    @classmethod
    @transaction.atomic
    def login(
        cls,
        *,
        email: str,
        password: str,
        ip_address: str = "",
        device: str = "Unknown Device",
        location: str = "Unknown Location",
    ) -> dict[str, str]:
        """
        Authenticate a user and issue JWT tokens.
        """

        user = cls.authenticate_user(
            email=email,
            password=password,
        )

        user.last_login = timezone.now()

        user.save(
            update_fields=[
                "last_login",
                "updated_at",
            ],
        )

        transaction.on_commit(
            lambda: NotificationService.send_login_alert(
                user=user,
                email=user.email,
                name=user.get_full_name() or user.email,
                ip_address=ip_address,
                device=device,
                location=location,
            ),
        )

        return cls.issue_tokens(
            user=user,
        )

    @staticmethod
    def logout(
        *,
        refresh_token: str,
    ) -> None:
        """
        Blacklist a refresh token.
        """

        try:
            RefreshToken(
                refresh_token,
            ).blacklist()

        except TokenError as exc:
            raise AuthenticationException(
                message="Invalid refresh token.",
            ) from exc

    @staticmethod
    def refresh(
        *,
        refresh_token: str,
    ) -> dict[str, str]:
        """
        Rotate a refresh token.
        """

        try:
            current_refresh = RefreshToken(
                refresh_token,
            )

            user = User.objects.get(
                pk=current_refresh["user_id"],
            )

            current_refresh.blacklist()

            new_refresh = RefreshToken.for_user(
                user,
            )

            return {
                "access": str(
                    new_refresh.access_token,
                ),
                "refresh": str(
                    new_refresh,
                ),
            }

        except (
            TokenError,
            User.DoesNotExist,
        ) as exc:
            raise AuthenticationException(
                message="Invalid or expired refresh token.",
            ) from exc

    @staticmethod
    def issue_tokens(
        *,
        user: User,
    ) -> dict[str, str]:
        """
        Issue JWT access and refresh tokens.
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
    "AuthenticationService",
]

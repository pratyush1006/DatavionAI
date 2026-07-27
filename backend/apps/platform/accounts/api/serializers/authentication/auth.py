"""
Authentication serializers.

Handles:

- Registration
- Password login
- Login OTP verification
- JWT refresh
- Logout
"""

from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
)

from django.contrib.auth.password_validation import (
    validate_password,
)
from rest_framework import serializers

from apps.platform.accounts.selectors import (
    get_user_by_email,
)
from apps.platform.accounts.services import (
    AuthenticationService,
)
from apps.platform.tenancy.constants import (
    TenantType,
)

if TYPE_CHECKING:
    from apps.platform.accounts.models import User


class RegisterSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for SaaS user registration.

    Creates:

    - User
    - Tenant
    - Tenant owner membership
    - Email verification OTP
    """

    password = serializers.CharField(
        write_only=True,
        style={
            "input_type": "password",
        },
        validators=[
            validate_password,
        ],
    )

    organization_name = serializers.CharField(
        write_only=True,
        required=True,
        max_length=255,
    )

    organization_type = serializers.ChoiceField(
        choices=TenantType.choices,
        default=TenantType.CLINIC,
        write_only=True,
    )

    class Meta:
        from apps.platform.accounts.models import User

        model = User

        fields = (
            "email",
            "password",
            "first_name",
            "last_name",
            "organization_name",
            "organization_type",
        )

        extra_kwargs = {
            "email": {
                "required": True,
            },
            "first_name": {
                "required": True,
            },
            "last_name": {
                "required": True,
            },
        }

    def validate_email(
        self,
        value: str,
    ) -> str:
        """
        Normalize email.
        """

        email = value.strip().lower()

        if (
            get_user_by_email(
                email=email,
            )
            is not None
        ):
            raise serializers.ValidationError(
                "A user with this email already exists.",
            )

        return email

    def validate_organization_name(
        self,
        value: str,
    ) -> str:
        """
        Normalize organization name.
        """

        return value.strip()

    def create(
        self,
        validated_data: dict[str, Any],
    ) -> User:
        """
        Register SaaS user.
        """

        return AuthenticationService.register(
            **validated_data,
        )


class LoginSerializer(
    serializers.Serializer,
):
    """
    Request login OTP.

    First step of OTP based authentication.
    """

    email = serializers.EmailField()

    password = serializers.CharField(
        write_only=True,
        style={
            "input_type": "password",
        },
    )

    def validate_email(
        self,
        value: str,
    ) -> str:
        """
        Normalize email.
        """

        return value.strip().lower()

    def save(
        self,
        **kwargs: Any,
    ) -> dict[str, str]:
        """
        Generate login OTP.
        """

        return AuthenticationService.request_login_otp(
            email=self.validated_data["email"],
            password=self.validated_data["password"],
        )


class VerifyLoginOTPSerializer(
    serializers.Serializer,
):
    """
    Verify login OTP and issue JWT tokens.
    """

    otp_id = serializers.UUIDField()

    otp = serializers.CharField(
        max_length=10,
    )

    def save(
        self,
        **kwargs: Any,
    ) -> dict[str, str]:
        """
        Verify OTP.
        """

        return AuthenticationService.verify_login_otp(
            otp_id=self.validated_data["otp_id"],
            code=self.validated_data["otp"],
            ip_address=kwargs.get(
                "ip_address",
                "",
            ),
            device=kwargs.get(
                "device",
                "Unknown Device",
            ),
            location=kwargs.get(
                "location",
                "Unknown Location",
            ),
        )


class LogoutSerializer(
    serializers.Serializer,
):
    """
    Logout serializer.
    """

    refresh = serializers.CharField()

    def save(
        self,
        **kwargs: Any,
    ) -> None:
        """
        Logout user.
        """

        AuthenticationService.logout(
            refresh_token=self.validated_data["refresh"],
        )


class RefreshSerializer(
    serializers.Serializer,
):
    """
    Refresh token serializer.
    """

    refresh = serializers.CharField()

    def validate(
        self,
        attrs: dict[str, Any],
    ) -> dict[str, str]:
        """
        Refresh JWT token.
        """

        return AuthenticationService.refresh(
            refresh_token=attrs["refresh"],
        )


__all__ = (
    "LoginSerializer",
    "LogoutSerializer",
    "RefreshSerializer",
    "RegisterSerializer",
    "VerifyLoginOTPSerializer",
)

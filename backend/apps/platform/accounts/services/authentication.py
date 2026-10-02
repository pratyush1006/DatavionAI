"""
Authentication services.

Handles:

- Registration
- Authentication
- Login OTP workflow
- Login OTP resend workflow
- JWT token lifecycle
- Login security events

Notification delivery is delegated to the
DatavionOS common notification framework.
"""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from django.contrib.auth import authenticate
from django.db import transaction
from django.utils import timezone
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.common.exceptions import AuthenticationException
from apps.common.notifications.constants import CHANNEL_EMAIL
from apps.common.notifications.models import Notification, NotificationRecipient
from apps.common.notifications.services import notification_service
from apps.platform.accounts.constants import (
    OTP_MAX_RESEND_PER_HOUR,
    OTP_RESEND_INTERVAL_SECONDS,
    OTPChannel,
    OTPPurpose,
)
from apps.platform.accounts.models import OTP, LoginAttemptStatus, User
from apps.platform.accounts.services.otp import OTPService
from apps.platform.accounts.services.security import SecurityService
from apps.platform.accounts.services.user import UserService
from apps.platform.tenancy.services import TenantService

logger = logging.getLogger(__name__)


class AuthenticationService:
    """
    Business authentication service.
    """

    @staticmethod
    def _send_verification_otp(*, user: User, code: str) -> None:
        """
        Send email verification OTP safely.
        """
        try:
            notification_service.send(
                Notification(
                    name="EMAIL_VERIFICATION_OTP",
                    channel=CHANNEL_EMAIL,
                    recipient=NotificationRecipient(
                        recipient_id=str(user.id),
                        address=user.email,
                        name=user.get_full_name() or user.email,
                    ),
                    template="verification_otp",
                    payload={"otp": code, "email": user.email},
                )
            )
        except Exception:
            logger.exception("Failed sending verification OTP")

    @staticmethod
    def _send_login_otp(*, user: User, code: str) -> None:
        """
        Send login OTP safely.
        """
        try:
            notification_service.send(
                Notification(
                    name="LOGIN_OTP",
                    channel=CHANNEL_EMAIL,
                    recipient=NotificationRecipient(
                        recipient_id=str(user.id),
                        address=user.email,
                        name=user.get_full_name() or user.email,
                    ),
                    template="login_otp",
                    payload={"otp": code, "email": user.email},
                )
            )
        except Exception:
            logger.exception("Failed sending login OTP")

    @staticmethod
    def _format_login_location(location: object) -> str:
        """Format the existing Geography result for customer-facing email."""
        if location is None:
            return "Unavailable"
        if isinstance(location, str):
            value = location.strip()
            if not value or value.startswith("GeoLocation("):
                return "Unavailable"
            return value
        parts = []
        for attribute in ("city", "region", "country"):
            part = getattr(location, attribute, None)
            if part:
                part = str(part).strip()
                if part and part not in parts:
                    parts.append(part)
        return ", ".join(parts) if parts else "Unavailable"

    @staticmethod
    def _send_login_alert(
        *,
        user: User,
        ip_address: str,
        device: str,
        location: str,
        latitude: float | None = None,
        longitude: float | None = None,
    ) -> None:
        """
        Send login security alert safely.
        """
        try:
            notification_service.send(
                Notification(
                    name="LOGIN_ALERT",
                    channel=CHANNEL_EMAIL,
                    recipient=NotificationRecipient(
                        recipient_id=str(user.id),
                        address=user.email,
                        name=user.get_full_name() or user.email,
                    ),
                    template="login_alert",
                    payload={
                        "ip_address": ip_address,
                        "device": device,
                        "location": AuthenticationService._format_login_location(
                            location
                        ),
                        "timestamp": timezone.now(),
                        "latitude": latitude,
                        "longitude": longitude,
                        "login_time": timezone.now(),
                    },
                )
            )
        except Exception:
            logger.exception("Failed sending login alert")

    @staticmethod
    @transaction.atomic
    def register(**validated_data: Any) -> User:
        """
        Register a SaaS user.
        """
        organization_name = validated_data.pop("organization_name", None)
        organization_type = validated_data.pop("organization_type", None)
        user = UserService.create(**validated_data)
        if organization_name:
            TenantService.create_tenant(
                name=organization_name,
                slug=organization_name.lower().replace(" ", "-"),
                tenant_type=organization_type,
                owner=user,
            )
        result = OTPService.create(
            user=user,
            purpose=OTPPurpose.EMAIL_VERIFICATION,
            recipient=user.email,
            channel=OTPChannel.EMAIL,
        )
        transaction.on_commit(
            lambda: AuthenticationService._send_verification_otp(
                user=user, code=result.code
            )
        )
        return user

    @staticmethod
    def authenticate_user(*, email: str, password: str) -> User:
        """
        Authenticate user credentials.
        """
        user = authenticate(username=email, password=password)
        if user is None:
            raise AuthenticationException(message="Invalid email or password.")
        if not user.is_active:
            raise AuthenticationException(message="User account is inactive.")
        if not user.is_verified:
            raise AuthenticationException(
                message="Please verify your email before logging in."
            )
        return user

    @classmethod
    @transaction.atomic
    def request_login_otp(cls, *, email: str, password: str) -> dict[str, str | bool]:
        """
        Validate credentials and create login OTP.
        """
        user = cls.authenticate_user(email=email, password=password)
        result = OTPService.create(
            user=user,
            purpose=OTPPurpose.LOGIN,
            recipient=user.email,
            channel=OTPChannel.EMAIL,
        )
        transaction.on_commit(lambda: cls._send_login_otp(user=user, code=result.code))
        return {
            "otp_id": str(result.otp.id),
            "requires_otp": True,
            "expires_at": result.otp.expires_at.isoformat(),
        }

    @classmethod
    @transaction.atomic
    def resend_login_otp(
        cls, *, otp_id: str, ip_address: str | None = None, user_agent: str = ""
    ) -> dict[str, str | bool]:
        """
        Resend the active login OTP.

        Security policy:

        - OTP must belong to the LOGIN purpose.
        - User must still be active.
        - Resend cooldown is enforced server-side.
        - Hourly resend limit is enforced server-side.
        - Previous OTP is invalidated atomically.
        - A new OTP ID is returned.
        """
        try:
            otp = (
                OTP.objects.select_for_update()
                .select_related("user")
                .get(id=otp_id, purpose=OTPPurpose.LOGIN)
            )
        except OTP.DoesNotExist as exc:
            raise AuthenticationException(
                message="Invalid or expired login verification request."
            ) from exc
        user = otp.user
        if not user.is_active:
            raise AuthenticationException(message="User account is inactive.")
        now = timezone.now()
        next_allowed_at = otp.created_at + timedelta(
            seconds=OTP_RESEND_INTERVAL_SECONDS
        )
        if now < next_allowed_at:
            remaining_seconds = max(1, int((next_allowed_at - now).total_seconds()))
            raise AuthenticationException(
                message=f"Please wait {remaining_seconds} seconds before requesting another verification code."
            )
        hourly_window_start = now - timedelta(hours=1)
        resend_count = (
            OTP.objects.filter(
                user=user, purpose=OTPPurpose.LOGIN, created_at__gte=hourly_window_start
            ).count()
            - 1
        )
        if resend_count >= OTP_MAX_RESEND_PER_HOUR:
            raise AuthenticationException(
                message="You have reached the maximum number of verification code resends. Please try again later."
            )
        result = OTPService.resend(otp=otp)
        transaction.on_commit(lambda: cls._send_login_otp(user=user, code=result.code))
        return {
            "otp_id": str(result.otp.id),
            "requires_otp": True,
            "expires_at": result.otp.expires_at.isoformat(),
            "resend_available_at": (
                result.otp.created_at + timedelta(seconds=OTP_RESEND_INTERVAL_SECONDS)
            ).isoformat(),
        }

    @classmethod
    @transaction.atomic
    def verify_login_otp(
        cls,
        *,
        otp_id: str,
        code: str,
        ip_address: str = "",
        device: str = "Unknown Device",
        location: str = "Unknown Location",
    ) -> dict[str, str]:
        """
        Verify login OTP and issue JWT tokens.
        """
        try:
            otp = OTP.objects.select_related("user").get(
                id=otp_id, purpose=OTPPurpose.LOGIN
            )
        except OTP.DoesNotExist as exc:
            raise AuthenticationException(
                message="Invalid login verification request."
            ) from exc
        if not OTPService.verify(otp=otp, code=code):
            raise AuthenticationException(message="Invalid login OTP.")
        user = otp.user
        if not user.is_active:
            raise AuthenticationException(message="User account is inactive.")
        SecurityService.record_login_attempt(
            email=user.email,
            user=user,
            status=LoginAttemptStatus.SUCCESS,
            ip_address=ip_address,
            device=device,
            location=location,
        )
        user.last_login = timezone.now()
        user.save(update_fields=["last_login", "updated_at"])
        transaction.on_commit(
            lambda: cls._send_login_alert(
                user=user,
                ip_address=ip_address,
                device=device,
                location=location,
                latitude=getattr(location, "latitude", None),
                longitude=getattr(location, "longitude", None),
            )
        )
        return cls.issue_tokens(user=user)

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
        Existing direct JWT login flow.
        """
        user = cls.authenticate_user(email=email, password=password)
        SecurityService.record_login_attempt(
            email=email,
            user=user,
            status=LoginAttemptStatus.SUCCESS,
            ip_address=ip_address,
            device=device,
            location=location,
        )
        user.last_login = timezone.now()
        user.save(update_fields=["last_login", "updated_at"])
        transaction.on_commit(
            lambda: cls._send_login_alert(
                user=user,
                ip_address=ip_address,
                device=device,
                location=location,
                latitude=getattr(location, "latitude", None),
                longitude=getattr(location, "longitude", None),
            )
        )
        return cls.issue_tokens(user=user)

    @staticmethod
    def logout(*, refresh_token: str) -> None:
        """
        Blacklist refresh token.
        """
        try:
            token = RefreshToken(
                refresh_token  # type: ignore[arg-type]  # Runtime API accepts JWT strings.
            )
            SecurityService.revoke_session(refresh_token_id=str(token["jti"]))
            token.blacklist()
        except TokenError as exc:
            raise AuthenticationException(message="Invalid refresh token.") from exc

    @staticmethod
    def refresh(*, refresh_token: str) -> dict[str, str]:
        """
        Rotate refresh token.
        """
        try:
            current_refresh = RefreshToken(
                refresh_token  # type: ignore[arg-type]  # Runtime API accepts JWT strings.
            )
            user = User.objects.get(pk=current_refresh["user_id"])
            if not user.is_active:
                raise AuthenticationException(message="User account is inactive.")
            current_refresh.blacklist()
            new_refresh = RefreshToken.for_user(user)
            return {
                "access": str(new_refresh.access_token),
                "refresh": str(new_refresh),
            }
        except User.DoesNotExist as exc:
            raise AuthenticationException(message="User account not found.") from exc
        except TokenError as exc:
            raise AuthenticationException(
                message="Invalid or expired refresh token."
            ) from exc

    @staticmethod
    def issue_tokens(*, user: User) -> dict[str, str]:
        """
        Issue JWT tokens and create session record.
        """
        refresh = RefreshToken.for_user(user)
        SecurityService.create_session(user=user, refresh_token_id=str(refresh["jti"]))
        return {"access": str(refresh.access_token), "refresh": str(refresh)}


__all__ = ("AuthenticationService",)

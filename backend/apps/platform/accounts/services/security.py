"""
Authentication security services.

Responsible for:

- Login attempt tracking
- Session lifecycle management
- Security audit support
"""

from __future__ import annotations

from django.utils import timezone

from apps.platform.accounts.models import (
    LoginAttempt,
    LoginAttemptStatus,
    User,
    UserSession,
    UserSessionStatus,
)


class SecurityService:
    """
    Security operations for authentication workflows.
    """

    @staticmethod
    def record_login_attempt(
        *,
        email: str,
        user: User | None,
        status: LoginAttemptStatus,
        failure_reason: str = "",
        ip_address: str = "",
        device: str = "",
        location: str = "",
        user_agent: str = "",
    ) -> LoginAttempt:
        """
        Store authentication attempt.
        """

        return LoginAttempt.objects.create(
            user=user,
            email=email,
            status=status,
            failure_reason=failure_reason,
            ip_address=(ip_address if ip_address else None),
            device=device,
            location=location,
            user_agent=user_agent,
        )

    @staticmethod
    def create_session(
        *,
        user: User,
        refresh_token_id: str,
        ip_address: str = "",
        device: str = "",
        location: str = "",
        user_agent: str = "",
    ) -> UserSession:
        """
        Create authenticated user session.
        """

        return UserSession.objects.create(
            user=user,
            refresh_token_id=refresh_token_id,
            status=UserSessionStatus.ACTIVE,
            ip_address=(ip_address if ip_address else None),
            device=device,
            location=location,
            user_agent=user_agent,
        )

    @staticmethod
    def revoke_session(
        *,
        refresh_token_id: str,
    ) -> None:
        """
        Revoke active session.
        """

        session = UserSession.objects.filter(
            refresh_token_id=refresh_token_id,
            status=UserSessionStatus.ACTIVE,
        ).first()

        if session is None:
            return

        session.status = UserSessionStatus.REVOKED

        session.revoked_at = timezone.now()

        session.save(
            update_fields=[
                "status",
                "revoked_at",
                "updated_at",
            ],
        )

    @staticmethod
    def revoke_all_sessions(
        *,
        user: User,
    ) -> int:
        """
        Revoke all active sessions.
        """

        return UserSession.objects.filter(
            user=user,
            status=UserSessionStatus.ACTIVE,
        ).update(
            status=UserSessionStatus.REVOKED,
            revoked_at=timezone.now(),
            updated_at=timezone.now(),
        )


__all__ = ("SecurityService",)

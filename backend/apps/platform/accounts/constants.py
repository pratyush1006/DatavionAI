"""
Accounts application constants.
"""

from __future__ import annotations

from django.db.models import TextChoices

# ==============================================================================
# Profile Defaults
# ==============================================================================

DEFAULT_LANGUAGE = "en"

DEFAULT_TIMEZONE = "Asia/Kolkata"

# ==============================================================================
# OTP
# ==============================================================================


class OTPChannel(TextChoices):
    """
    OTP delivery channel choices.
    """

    EMAIL = (
        "EMAIL",
        "Email",
    )

    SMS = (
        "SMS",
        "SMS",
    )

    WHATSAPP = (
        "WHATSAPP",
        "WhatsApp",
    )

    AUTHENTICATOR = (
        "AUTHENTICATOR",
        "Authenticator App",
    )


class OTPPurpose(TextChoices):
    """
    OTP purpose choices.
    """

    EMAIL_VERIFICATION = (
        "EMAIL_VERIFICATION",
        "Email Verification",
    )

    PASSWORD_RESET = (
        "PASSWORD_RESET",
        "Password Reset",
    )

    LOGIN = (
        "LOGIN",
        "Login",
    )

    MFA = (
        "MFA",
        "Multi-Factor Authentication",
    )


# ==============================================================================
# OTP Configuration
# ==============================================================================

OTP_LENGTH = 6

OTP_EXPIRY_MINUTES = 10

OTP_RESEND_INTERVAL_SECONDS = 30

OTP_MAX_ATTEMPTS = 5

OTP_MAX_RESEND_PER_HOUR = 5

OTP_MAX_ACTIVE_CODES = 1

OTP_LOCKOUT_MINUTES = 30

PASSWORD_RESET_EXPIRY_MINUTES = 30

# ==============================================================================
# OAuth
# ==============================================================================


class OAuthProvider(TextChoices):
    """
    OAuth provider choices.
    """

    GOOGLE = (
        "GOOGLE",
        "Google",
    )

    MICROSOFT = (
        "MICROSOFT",
        "Microsoft",
    )


__all__ = [
    "DEFAULT_LANGUAGE",
    "DEFAULT_TIMEZONE",
    "OAuthProvider",
    "OTPChannel",
    "OTPPurpose",
    "OTP_EXPIRY_MINUTES",
    "OTP_LENGTH",
    "OTP_LOCKOUT_MINUTES",
    "OTP_MAX_ACTIVE_CODES",
    "OTP_MAX_ATTEMPTS",
    "OTP_MAX_RESEND_PER_HOUR",
    "OTP_RESEND_INTERVAL_SECONDS",
    "PASSWORD_RESET_EXPIRY_MINUTES",
]

"""
Notification application constants.
"""

from __future__ import annotations

from django.db.models import (
    IntegerChoices,
    TextChoices,
)

# ==============================================================================
# Notification Channels
# ==============================================================================


class NotificationChannel(TextChoices):
    """
    Supported notification delivery channels.
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

    PUSH = (
        "PUSH",
        "Push Notification",
    )

    IN_APP = (
        "IN_APP",
        "In-App Notification",
    )


# ==============================================================================
# Notification Status
# ==============================================================================


class NotificationStatus(TextChoices):
    """
    Notification lifecycle states.
    """

    PENDING = (
        "PENDING",
        "Pending",
    )

    QUEUED = (
        "QUEUED",
        "Queued",
    )

    SENDING = (
        "SENDING",
        "Sending",
    )

    SENT = (
        "SENT",
        "Sent",
    )

    DELIVERED = (
        "DELIVERED",
        "Delivered",
    )

    FAILED = (
        "FAILED",
        "Failed",
    )

    CANCELLED = (
        "CANCELLED",
        "Cancelled",
    )


# ==============================================================================
# Notification Priority
# ==============================================================================


class NotificationPriority(IntegerChoices):
    """
    Notification priority.
    """

    LOW = (
        10,
        "Low",
    )

    NORMAL = (
        20,
        "Normal",
    )

    HIGH = (
        30,
        "High",
    )

    CRITICAL = (
        40,
        "Critical",
    )


# ==============================================================================
# Notification Providers
# ==============================================================================


class NotificationProvider(TextChoices):
    """
    Supported notification providers.
    """

    SMTP = (
        "SMTP",
        "SMTP",
    )

    AWS_SES = (
        "AWS_SES",
        "AWS SES",
    )

    SENDGRID = (
        "SENDGRID",
        "SendGrid",
    )

    TWILIO = (
        "TWILIO",
        "Twilio",
    )

    WHATSAPP = (
        "WHATSAPP",
        "WhatsApp",
    )

    FIREBASE = (
        "FIREBASE",
        "Firebase Cloud Messaging",
    )


# ==============================================================================
# Email Templates
# ==============================================================================


class EmailTemplate(TextChoices):
    """
    Email template identifiers.
    """

    VERIFICATION_OTP = (
        "verification_otp",
        "Verification OTP",
    )

    PASSWORD_RESET_OTP = (
        "password_reset_otp",
        "Password Reset OTP",
    )

    LOGIN_OTP = (
        "login_otp",
        "Login OTP",
    )

    WELCOME = (
        "welcome",
        "Welcome",
    )

    PASSWORD_CHANGED = (
        "password_changed",
        "Password Changed",
    )

    LOGIN_ALERT = (
        "login_alert",
        "Login Alert",
    )

    ACCOUNT_LOCKED = (
        "account_locked",
        "Account Locked",
    )

    ORGANIZATION_INVITATION = (
        "organization_invitation",
        "Organization Invitation",
    )


# ==============================================================================
# Defaults
# ==============================================================================

DEFAULT_FROM_NAME = "DatavionAI"

DEFAULT_REPLY_TO = "support@datavion.ai"

DEFAULT_PROVIDER = NotificationProvider.SMTP

DEFAULT_CHANNEL = NotificationChannel.EMAIL

DEFAULT_PRIORITY = NotificationPriority.NORMAL

DEFAULT_MAX_RETRIES = 3

DEFAULT_RETRY_DELAY_SECONDS = 60


# ==============================================================================
# Email Subjects
# ==============================================================================

OTP_EMAIL_SUBJECT = "Verify your DatavionAI account"

PASSWORD_RESET_SUBJECT = "Reset your DatavionAI password"

LOGIN_OTP_SUBJECT = "Your DatavionAI login verification code"

WELCOME_SUBJECT = "Welcome to DatavionAI"

PASSWORD_CHANGED_SUBJECT = "Your password has been changed"

LOGIN_ALERT_SUBJECT = "New login detected"

ACCOUNT_LOCKED_SUBJECT = "Your account has been locked"

ORGANIZATION_INVITATION_SUBJECT = "You're invited to join DatavionAI"


__all__ = [
    "ACCOUNT_LOCKED_SUBJECT",
    "DEFAULT_CHANNEL",
    "DEFAULT_FROM_NAME",
    "DEFAULT_MAX_RETRIES",
    "DEFAULT_PRIORITY",
    "DEFAULT_PROVIDER",
    "DEFAULT_REPLY_TO",
    "DEFAULT_RETRY_DELAY_SECONDS",
    "EmailTemplate",
    "LOGIN_ALERT_SUBJECT",
    "LOGIN_OTP_SUBJECT",
    "NotificationChannel",
    "NotificationPriority",
    "NotificationProvider",
    "NotificationStatus",
    "ORGANIZATION_INVITATION_SUBJECT",
    "OTP_EMAIL_SUBJECT",
    "PASSWORD_CHANGED_SUBJECT",
    "PASSWORD_RESET_SUBJECT",
    "WELCOME_SUBJECT",
]
